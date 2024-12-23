"""Component to make instant statistics about your history."""

from __future__ import annotations

import datetime
from abc import abstractmethod
from typing import Any

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.sensor import (
    PLATFORM_SCHEMA as SENSOR_PLATFORM_SCHEMA,
)
from homeassistant.components.sensor import (
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import (
    CONF_ENTITY_ID,
    CONF_NAME,
    CONF_TYPE,
    CONF_UNIQUE_ID,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import PlatformNotReady
from homeassistant.helpers.device import async_device_info_to_link_from_entity
from homeassistant.helpers.entity import get_unit_of_measurement
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.reload import async_setup_reload_service
from homeassistant.helpers.template import Template
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import HistoryMathConfigEntry
from .const import (
    CONF_DURATION,
    CONF_END,
    CONF_PERIOD_KEYS,
    CONF_START,
    CONF_TYPE_KEYS,
    CONF_TYPE_MAX,
    DEFAULT_NAME,
    DOMAIN,
    PLATFORMS,
)
from .coordinator import HistoryMathUpdateCoordinator
from .data import HistoryMath

ICON = "mdi:chart-line"


def exactly_two_period_keys[_T: dict[str, Any]](conf: _T) -> _T:
    """Ensure exactly 2 of CONF_PERIOD_KEYS are provided."""
    if sum(param in conf for param in CONF_PERIOD_KEYS) != 2:
        raise vol.Invalid(
            "You must provide exactly 2 of the following: start, end, duration"
        )
    return conf


PLATFORM_SCHEMA = vol.All(
    SENSOR_PLATFORM_SCHEMA.extend(
        {
            vol.Required(CONF_ENTITY_ID): cv.entity_id,
            vol.Optional(CONF_START): cv.template,
            vol.Optional(CONF_END): cv.template,
            vol.Optional(CONF_DURATION): cv.time_period,
            vol.Optional(CONF_TYPE, default=CONF_TYPE_MAX): vol.In(CONF_TYPE_KEYS),
            vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
            vol.Optional(CONF_UNIQUE_ID): cv.string,
        }
    ),
    exactly_two_period_keys,
)


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    _: DiscoveryInfoType | None = None,
) -> None:
    """Set up the History Stats sensor."""
    await async_setup_reload_service(hass, DOMAIN, PLATFORMS)

    entity_id: str = config[CONF_ENTITY_ID]
    start: Template | None = config.get(CONF_START)
    end: Template | None = config.get(CONF_END)
    duration: datetime.timedelta | None = config.get(CONF_DURATION)
    name: str = config[CONF_NAME]
    unique_id: str | None = config.get(CONF_UNIQUE_ID)
    sensor_type: str = config[CONF_TYPE]

    history_math = HistoryMath(hass, entity_id, start, end, duration, sensor_type)
    coordinator = HistoryMathUpdateCoordinator(hass, history_math, name)
    await coordinator.async_refresh()
    if not coordinator.last_update_success:
        raise PlatformNotReady from coordinator.last_exception
    async_add_entities(
        [HistoryMathSensor(hass, coordinator, name, unique_id, entity_id)]
    )


async def async_setup_entry(
    hass: HomeAssistant,
    entry: HistoryMathConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the History stats sensor entry."""
    coordinator = entry.runtime_data
    entity_id: str = entry.options[CONF_ENTITY_ID]
    async_add_entities(
        [HistoryMathSensor(hass, coordinator, entry.title, entry.entry_id, entity_id)]
    )


class HistoryMathSensorBase(
    CoordinatorEntity[HistoryMathUpdateCoordinator], SensorEntity
):
    """Base class for a HistoryMath sensor."""

    _attr_icon = ICON

    def __init__(
        self,
        coordinator: HistoryMathUpdateCoordinator,
        name: str,
    ) -> None:
        """Initialize the HistoryMath sensor base class."""
        super().__init__(coordinator)
        self._attr_name = name

    async def async_added_to_hass(self) -> None:
        """Entity has been added to hass."""
        await super().async_added_to_hass()
        self.async_on_remove(self.coordinator.async_setup_state_listener())

    def _handle_coordinator_update(self) -> None:
        """Set attrs from value and count."""
        self._process_update()
        super()._handle_coordinator_update()

    @callback
    @abstractmethod
    def _process_update(self) -> None:
        """Process an update from the coordinator."""


class HistoryMathSensor(HistoryMathSensorBase):
    """A HistoryMath sensor."""

    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(
        self,
        hass: HomeAssistant,
        coordinator: HistoryMathUpdateCoordinator,
        name: str,
        unique_id: str | None,
        source_entity_id: str,
    ) -> None:
        """Initialize the HistoryMath sensor."""
        super().__init__(coordinator, name)
        self._attr_native_unit_of_measurement = get_unit_of_measurement(
            hass,
            source_entity_id,
        )
        self._attr_unique_id = unique_id
        self._attr_device_info = async_device_info_to_link_from_entity(
            hass,
            source_entity_id,
        )
        self._process_update()

    @callback
    def _process_update(self) -> None:
        """Process an update from the coordinator."""
        state = self.coordinator.data
        self._attr_native_value = state.calc_value
