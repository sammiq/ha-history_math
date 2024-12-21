"""The history_math component constants."""

from homeassistant.const import Platform

DOMAIN = "history_math"
PLATFORMS = [Platform.SENSOR]

CONF_START = "start"
CONF_END = "end"
CONF_DURATION = "duration"
CONF_PERIOD_KEYS = [CONF_START, CONF_END, CONF_DURATION]

CONF_TYPE_MAX = "max"
CONF_TYPE_MEAN = "mean"
CONF_TYPE_MIN = "min"
CONF_TYPE_KEYS = [CONF_TYPE_MAX, CONF_TYPE_MEAN, CONF_TYPE_MIN]

DEFAULT_NAME = "unnamed calculation"
