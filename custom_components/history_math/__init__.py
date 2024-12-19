"""The history_math component."""

from __future__ import annotations

from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ENTITY_ID
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device import (
    async_remove_stale_devices_links_keep_entity_device,
)
from homeassistant.helpers.template import Template

from .const import CONF_DURATION, CONF_END, CONF_START, PLATFORMS
from .coordinator import HistoryMathUpdateCoordinator
from .data import HistoryMath

type HistoryMathConfigEntry = ConfigEntry[HistoryMathUpdateCoordinator]


async def async_setup_entry(
    hass: HomeAssistant, entry: HistoryMathConfigEntry
) -> bool:
    """Set up History stats from a config entry."""

    entity_id: str = entry.options[CONF_ENTITY_ID]
    start: str | None = entry.options.get(CONF_START)
    end: str | None = entry.options.get(CONF_END)

    duration: timedelta | None = None
    if duration_dict := entry.options.get(CONF_DURATION):
        duration = timedelta(**duration_dict)

    history_math = HistoryMath(
        hass,
        entity_id,
        Template(start, hass) if start else None,
        Template(end, hass) if end else None,
        duration,
    )
    coordinator = HistoryMathUpdateCoordinator(hass, history_math, entry, entry.title)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator

    async_remove_stale_devices_links_keep_entity_device(
        hass,
        entry.entry_id,
        entry.options[CONF_ENTITY_ID],
    )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(update_listener))

    return True


async def async_unload_entry(
    hass: HomeAssistant, entry: HistoryMathConfigEntry
) -> bool:
    """Unload History stats config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update."""
    await hass.config_entries.async_reload(entry.entry_id)