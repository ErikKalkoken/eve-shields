# eve-shields

This is a web service that allows the creation of EVE online related dynamic shields through [shields.io](shields.io) that can be used on web sites or github pages.

## Features

Display of dynamic zKillboard statistics for an EVE entity, e.g. member count for an alliance or ISK destroyed for a corporation.

Currently supports all EVE entities and properties from the zKillboard Statistics API. See [here](https://github.com/zKillboard/zKillboard/wiki/API-(Statistics)) for details.

Can apply output formatting, e.g. for ISK values

Label and colors can be defined as needed

## Example

Shield with the current member count of the Same Great Taste alliance:

![Member Count Dummy](https://img.shields.io/badge/Member%20Count-79-success)

Link:

```plain
https://img.shields.io/endpoint?url=https://.../zkb-stats/allianceID/99009333/info-memberCount&label=Members&color=success
```

## How it works

The shield are created by shields.io. Those guys also provide an API for dynamically creating shields with input from an endpoint.

eve-shields functions as such an endpoint and provides all data in the required format to shields.io for creating the resulting shield.

To create your own shield just define the url to eve-shields accordingly.

## Syntax

Basic syntax is:

```plain
https://{base-url}/zkb-stats/{entity-type}/{entity-id}/{property}[?...]
```

- `entity-type`: type of the entity as defined by the ZKB API, e.g. `allianceID` for alliance
- `entity-id`: a valid EVE ID corresponding to the entity type, e.g. `99009333` for the "Same Great Taste" alliance
- `property`: name of the property to be shown as the value of the shield. For nested properties use `-` as separator. Examples: `iskDestroyed`, `info-memberCount`.

Optional URL parameters:

- `label`: label text to be shown instead of {property}
- `color`: color to be used (must be a valid value as defined on shields.io)
- `format`: format value with an formatter:
  - `isk` : ISK formatter
