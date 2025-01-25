# ICA Shopping List

A custom integration to sync your ICA shopping lists with Home Assistant.

## Features
- Fetch shopping lists from ICA.
- Sync updates between Home Assistant's shopping list and ICA.
- Authenticate securely via the Home Assistant UI.

## Installation
1. Install via [HACS](https://hacs.xyz/):
   - Add this repository as a custom repository.
   - Search for "ICA Shopping List" in HACS and install it.

2. Restart Home Assistant.

3. Add the integration:
   - Go to **Settings -> Devices & Services -> Add Integration**.
   - Search for **ICA Shopping List** and follow the setup process.

## Configuration
During setup, you'll need to provide your ICA username and password. These credentials are stored securely.

## Credits
This integration is based on the [ica-api](https://github.com/svendahlstrand/ica-api/tree/master) project by [svendahlstrand](https://github.com/svendahlstrand).