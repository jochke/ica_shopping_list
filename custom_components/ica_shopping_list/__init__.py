from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the ICA integration using YAML (not used)."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up ICA from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    # Start the ICA shopping list integration
    from .ica_shopping_list import ICAShoppingListAPI, ICAShoppingListIntegration

    api_client = ICAShoppingListAPI(
        username=entry.data["username"], password=entry.data["password"]
    )
    await api_client.login()

    ica_integration = ICAShoppingListIntegration(hass, api_client)
    await ica_integration.initialize()

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload an ICA config entry."""
    hass.data[DOMAIN].pop(entry.entry_id)
    return True
