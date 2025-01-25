import aiohttp
import logging

_LOGGER = logging.getLogger(__name__)

class ICAShoppingListAPI:
    """Handles interactions with the ICA API for shopping lists."""

    def __init__(self, username: str, password: str):
        self.base_url = "https://handla.api.ica.se/api"
        self.username = username
        self.password = password
        self.auth_ticket = None

    async def login(self):
        """Authenticate with the ICA API and retrieve an authentication ticket."""
        import base64
        auth = f"{self.username}:{self.password}"
        auth_base64 = base64.b64encode(auth.encode()).decode()
        headers = {"Authorization": f"Basic {auth_base64}"}

        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/login", headers=headers) as response:
                if response.status == 200:
                    self.auth_ticket = response.headers.get("AuthenticationTicket")
                    _LOGGER.info("Successfully authenticated with ICA API.")
                else:
                    _LOGGER.error(f"Failed to authenticate: {response.status}")

    async def get_shopping_lists(self):
        """Fetch all shopping lists from ICA."""
        headers = {"AuthenticationTicket": self.auth_ticket}
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/user/offlineshoppinglists", headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("ShoppingLists", [])
                else:
                    _LOGGER.error(f"Failed to fetch shopping lists: {response.status}")
                    return []

    async def sync_shopping_list(self, offline_id, items):
        """Sync a shopping list back to ICA."""
        headers = {"AuthenticationTicket": self.auth_ticket}
        payload = {"Rows": items}
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/user/offlineshoppinglists/{offline_id}/sync",
                headers=headers,
                json=payload,
            ) as response:
                if response.status == 200:
                    _LOGGER.info("Successfully synced shopping list with ICA.")
                else:
                    _LOGGER.error(f"Failed to sync shopping list: {response.status}")

