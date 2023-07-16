import asyncio
import voluptuous as vol
import aiohttp

from homeassistant.components.sensor import (
    PLATFORM_SCHEMA,
    SensorEntity,
)
from homeassistant.const import CONF_NAME, TEMP_CELSIUS

DEFAULT_NAME = "UK Bin Collection Sensor"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
        vol.Required("url"): str,
        vol.Required("council"): str,
    }
)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the sensor platform."""
    name = config[CONF_NAME]
    url = config["url"]
    council = config["council"]

    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        data = await response.json()

    async_add_entities([UkBinCollectionSensor(name, data, council)], True)

class UkBinCollectionSensor(SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, name, data, council):
        self._name = name
        self._data = data
        self._council = council

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def unique_id(self):
        """Return a unique, Home Assistant-friendly identifier for this entity."""
        return f"{self._name}_bin_collection_sensor"

    @property
    def state(self):
        """Return the next bin collection date."""
        return self._data.get("next_collection_date")

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return "date"

    @property
    def device_state_attributes(self):
        """Return additional attributes of the sensor."""
        return {"council": self._council}