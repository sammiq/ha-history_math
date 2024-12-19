"""The history_math component constants."""

from homeassistant.const import Platform

DOMAIN = "history_math"
PLATFORMS = [Platform.SENSOR]

CONF_START = "start"
CONF_END = "end"
CONF_DURATION = "duration"
CONF_PERIOD_KEYS = [CONF_START, CONF_END, CONF_DURATION]

DEFAULT_NAME = "unnamed statistics"
