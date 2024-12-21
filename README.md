# History Math

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

![Project Maintenance][maintenance-shield]
[![Community Forum][forum-shield]][forum]

_Integration to perform mathematical operations on a time period._

History Math takes an entity and performs operations on a given time period.

Some examples:
  - Measure the Mean temperature over the middle of the day,
  - Measure the Maximum humidity yesterday,
  - Measure the Minimum dew point overnight.

  While you can track these manually with a template, this integration can use data from the [history][history] integration,
  and operates in a similar manner to the [History Stats][history_stats] integration.

## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
1. If you do not have a `custom_components` directory (folder) there, you need to create it.
1. In the `custom_components` directory (folder) create a new folder called `history_math`.
1. Download _all_ the files from the `custom_components/history_math/` directory (folder) in this repository.
1. Place the files you downloaded in the new directory (folder) you created.
1. Restart Home Assistant
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "History Math"

## Configuration is done in the UI

<!---->

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***
[history]: https://www.home-assistant.io/integrations/history
[history_stats]: https://www.home-assistant.io/integrations/history_stats
[commits-shield]: https://img.shields.io/github/commit-activity/y/sammiq/ha-history_math.svg?style=for-the-badge
[commits]: https://github.com/sammiq/ha-history_math/commits/main
[exampleimg]: example.png
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/sammiq/ha-history_math.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40sammiq-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/sammiq/ha-history_math.svg?style=for-the-badge
[releases]: https://github.com/sammiq/ha-history_math/releases
