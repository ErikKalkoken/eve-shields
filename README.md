# eve-shields

This is a small web service that allows the creation of [EVE online](https://en.wikipedia.org/wiki/Eve_Online) related dynamic shields that can be used on web sites or github pages. Like the ones below that show stats for this github repo and the **eve-shields** service.

![Repo license](https://img.shields.io/github/license/ErikKalkoken/eve-shields) ![Python](https://img.shields.io/badge/python-3.5-blue) ![Build](https://api.travis-ci.org/ErikKalkoken/eve-shields.svg?branch=master) ![Uptime Robot status](https://img.shields.io/uptimerobot/status/m783377950-d030d9c007b33bdb219ac4e5)
[![Uptime Robot ratio](https://img.shields.io/uptimerobot/ratio/m783377950-d030d9c007b33bdb219ac4e5)](https://stats.uptimerobot.com/voNrrI7ooP)

## Shields

Here is an overview of all shields this service can generate for you:

Name | Description | Category | Example
--- | --- | --- | ---
activePvpChars | Active PVP characters in the last 7 days | zkb-stats | ![activePvpChars](https://img.shields.io/endpoint?url=https://eve-shields.kalkoken.net/zkb-stats/alliance/498125261/dangerRatio)
corpCount | Count of member corporations | zkb-stats| ![corpCount](https://img.shields.io/endpoint?url=https://eve-shields.kalkoken.net/zkb-stats/alliance/498125261/corpCount)
dangerRatio | Danger classification by zKillboard <br> snuggly: green, dangerous: red | zkb-stats | ![dangerRatio](https://img.shields.io/endpoint?url=https://eve-shields.kalkoken.net/zkb-stats/alliance/498125261/dangerRatio)
iskDestroyed | Total ISK destroyed | zkb-stats | ![iskDestroyed](https://img.shields.io/endpoint?url=https://eve-shields.kalkoken.net/zkb-stats/alliance/498125261/iskDestroyed)
iskLost | Total ISK lost | zkb-stats | ![iskLost](https://img.shields.io/endpoint?url=https://eve-shields.kalkoken.net/zkb-stats/alliance/498125261/iskLost)
iskEff | Total ISK efficiency in % <br> eff = destroyed / (destroyed + lost) * 100 <br> eff >= 50: green, eff < 50: red  | zkb-stats | ![iskEff](https://img.shields.io/endpoint?url=https://eve-shields.kalkoken.net/zkb-stats/alliance/498125261/iskEff)
memberCount | Count of member characters | zkb-stats| ![memberCount](https://img.shields.io/endpoint?url=https://eve-shields.kalkoken.net/zkb-stats/alliance/498125261/memberCount)
shipsDestroyed | Total ships destroyed | zkb-stats | ![shipsDestroyed](https://img.shields.io/endpoint?url=https://eve-shields.kalkoken.net/zkb-stats/alliance/498125261/shipsDestroyed)
shipsLost | Total ships lost  | zkb-stats| ![shipsLost](https://img.shields.io/endpoint?url=https://eve-shields.kalkoken.net/zkb-stats/alliance/498125261/shipsLost)
shipsEff | Total ships efficiency in % <br> = destroyed / (destroyed + lost) * 100  <br> eff >= 50: green, eff < 50: red | zkb-stats| ![shipsEff](https://img.shields.io/endpoint?url=https://eve-shields.kalkoken.net/zkb-stats/alliance/498125261/shipsEff)

All examples on this page are generated live with data from zKillboard for Test Alliance Please Ignore.

## How it works

The shield are created by a service called [shields.io](shields.io), which is providing many different shields for people to use. They also provide an API for dynamically creating shields with custom input from an endpoint.

**eve-shields** functions as such an endpoint and provides all data in the required format to shields.io for creating Eve Online related shields. Data is dynamically loaded from APIs like zKillboard API as needed.

## How to use it

I am hosting this service on a server and you are free to use it directly for your website or github pages. (see section **Service** for details)

Or you can install and run it on your own web server. There are many ways, but I recommend using PyInstaller, which is the easiest. You will need a web server (e.g. NGINX) and a WSGI server (e.g Gunicorn) to run it.

```bash
pip install git+https://github.com/ErikKalkoken/eve-shields
```

Note that if you run it yourself you need to have SSL, because shields.io only accepts https links as endpoint.

## Syntax

To create your own shield use the JSON endpoint URL from shield.io and add the endpoint URL from eve-shields for the `url` parameter.

Here is a complete example url for creating a members count shield for Test Alliance Please Ignore:

```plain
https://img.shields.io/endpoint?url=https://eve-shields.kalkoken.net/zkb-stats/alliance/498125261/memberCount
```

Let's break this down in its two parts: shields.io and **eve-shields**.

### shields.io

The syntax for [shields.io JSON endpoint](https://shields.io/endpoint) is:

```plain
https://img.shields.io/endpoint?url={url-eve-shields}&style=...
```

### eve-shields

The basic syntax for the  eve shields endpoint url is:

```plain
https://eve-shields.kalkoken.net/{source}/...
```

 `source` is the name of the data source used to create shields. Currently the only implemented source is `zkb-stats`.

Note that you still can add query parameters from shields.io to customize your shield, e.g. if you want to override the color (`color`) or label (`label`) generated by eve-shield.

### Source: zkb-stats

`zkb-stats` provides zKillboard statistics for EVE entities.  See [here](https://github.com/zKillboard/zKillboard/wiki/API-(Statistics)) for details on the API. Please note though that only a sub set is currently implemented.

#### syntax

The syntax for zkb-stats shields is as follows:

```plain
https://eve-shields.kalkoken.net/zkb-stats/{entity-type}/{entity-id}/{shield-name}
```

- `entity-type`: name of the EVE entity type. The following types are supported:
  - alliance
  - character
  - corporation  
  - faction
  - region
  - shipGroup
  - shipType  
  - solarSystem
- `entity-id`: a valid EVE ID corresponding to the entity type, e.g. `498125261` for Test Alliance Please Ignore.
- `shield-name`: name of the shield to create. Note that not all shields are available for every entity type, e.g. there is no member count for ships. See section **Shields** for a list of all shield names.

## Service

The eve-shields service on https://eve-shields.kalkoken.net is provided for free and can be used by anyone to create their own eve related shields. And while I strive to provide a reliable service it is provided "as-is" only and without any guarantees with respect to availability and reliably.

For the current service status check the shields on top of this page. A detailed service status report can be found [here](https://stats.uptimerobot.com/voNrrI7ooP).

## Contributions

Help and contributions are welcome.

## Credits

Special thanks to the guys at [shields.io](https://shields.io) for their great service and to [@cvweiss](https://github.com/cvweiss) for running [zKillboard](https://github.com/zKillboard/zKillboard) and providing all those nice APIs along with it.
