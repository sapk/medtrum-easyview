[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://img.shields.io/badge/HACS-Repository-41BDF5.svg)](https://my.home-assistant.io/redirect/hacs_repository/?category=integration&repository=medtrum-easyview&owner=sapk)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![Validate with Hassfest/HACS](https://github.com/sapk/medtrum-easyview/actions/workflows/validate.yml/badge.svg)](https://github.com/sapk/medtrum-easyview/actions/workflows/validate.yml)

# Medtrum EasyView Integration for Home Assistant

[integration_medtrum-easyview]: https://github.com/sapk/medtrum-easyview.git

**This integration will set up the following platforms for each patient linked to the Medtrum EasyView account.**

Platform | Description
-- | --

`sensor` | Show info from Medtrum EasyView API.
- Pump Status
- Pump Remaining time
- Pump Remaining dose
- Pump Last update
- Blood Glucose Target
- Basal Daily Volume
- Bolus Daily Volume
- Basal Rate
- Last Bolus Delivered Time
- Last Bolus Delivered Volume
- Active Insulin

`binary_sensor` | Show binary states from Medtrum EasyView API.
- Basal Active
- Pump (connectivity status)
    - Serial number: The serial number of the device (in hexadecimal, uppercase)
    - User ID: The Medtrum EasyView user ID
    - Patient: The patient name associated with the account
- Sensor (connectivity status)

## Installation

1. Add this repository URL as a custom repository in HACS
2. Restart Home Assistant
3. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Medtrum EasyView"

## Configuration is done in the UI

You need a Medtrum EasyView account to use this integration

- Use username (mail) and password of the Medtrum EasyView account.
- A token will be retreived for the duration of the HA session.


## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)


This project is heavily inspired from [librelink integration](https://github.com/gillesvs/librelink.git)
***
