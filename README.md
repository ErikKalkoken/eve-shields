# eve-shields

This is a small web service that allows the creation of [EVE online](https://en.wikipedia.org/wiki/Eve_Online) related dynamic to be used on web sites or github pages. Like the ones below that show stats for this github repo.

![Repo license](https://img.shields.io/github/license/ErikKalkoken/eve-shields) ![Pyhton](https://img.shields.io/badge/python-3.5-blue)

## Features

Display of dynamic zKillboard statistics for an EVE entity, e.g. member count for an alliance or ISK destroyed for a corporation.

Currently supports all EVE entities and properties from the zKillboard Statistics API. See [here](https://github.com/zKillboard/zKillboard/wiki/API-(Statistics)) for details.

Can apply output formatting, e.g. for ISK values

Label and colors can be defined as needed

## Example

Shield with the current member count of the Same Great Taste alliance:

![Member Count Dummy](https://img.shields.io/endpoint?url=https://eve-shields.kalkoken.net/zkb-stats/allianceID/99009333/info-memberCount&label=Member%20Count&color=success)

Link to create this shield:

```plain
https://img.shields.io/endpoint?url=https://eve-shields.kalkoken.net/zkb-stats/allianceID/99009333/info-memberCount&label=Members&color=success
```

## How it works

The shield are created by a service called [shields.io](shields.io), which is providing many different shields for people to use. They also provide an API for dynamically creating shields with custom input from an endpoint.

**eve-shields** functions as such an endpoint and provides all data in the required format to shields.io for creating Eve Online related shields.

## How to use it

I am hosting this service on a server and you are free to use it directly for your website or github pages (at your own risk though - I can not guaranteer any kind of service level).

Or you can install and run it on your own web server. There are many ways, but I recommend using PyInstaller, which is the easiest. You will need a web server (e.g. NGINX) and a WGSI server (e.g Gunicorn) to run it.

```bash
pip install git+https://github.com/ErikKalkoken/eve-shields
```

Note that if you run it yourself you need to have SSL, because shields.io only accepts https links as endpoint.

## Syntax

To create your own shield just define the url to eve-shields as described in this section.

Basic syntax is:

```plain
https://eve-shields.kalkoken.net/zkb-stats/{entity-type}/{entity-id}/{property}[?...]
```

- `entity-type`: type of the entity as defined by the ZKB API, e.g. `allianceID` for alliance
- `entity-id`: a valid EVE ID corresponding to the entity type, e.g. `99009333` for the "Same Great Taste" alliance
- `property`: name of the property to be shown as the value of the shield. For nested properties use `-` as separator. Examples: `iskDestroyed`, `info-memberCount`.

Optional URL parameters:

- `label`: label text to be shown instead of {property}
- `color`: color to be used (must be a valid value as defined on shields.io)
- `format`: format value with an formatter:
  - `isk` : ISK formatter

## Contributions

Help and contributions are welcome

## Credits

Special thanks to the guys at [shields.io](https://shields.io) for their great service.
