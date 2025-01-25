from homeassistant import config_entries
import voluptuous as vol
import aiohttp
import logging

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class ICAConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for the ICA integration."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step where the user enters credentials."""
        errors = {}

        if user_input is not None:
            username = user_input.get("username")
            password = user_input.get("password")

            # Test the credentials with the ICA API
            try:
                auth = aiohttp.BasicAuth(username, password)
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        "https://handla.api.ica.se/api/login",
                        auth=auth,
                    ) as resp:
                        if resp.status == 200:
                            _LOGGER.info("Successfully authenticated with the ICA API.")
                            return self.async_create_entry(title="ICA", data=user_input)
                        elif resp.status == 401:
                            errors["base"] = "invalid_auth"
                        else:
                            errors["base"] = "unknown"
                            _LOGGER.error(
                                f"Unexpected response from ICA API: {resp.status} - {await resp.text()}"
                            )
            except aiohttp.ClientError as e:
                _LOGGER.error(f"Network error while authenticating with ICA API: {e}")
                errors["base"] = "cannot_connect"
            except Exception as e:
                _LOGGER.error(f"Unexpected error: {e}")
                errors["base"] = "unknown"

        # Show the input form
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("username"): str,
                vol.Required("password"): str,
            }),
            errors=errors,
        )
