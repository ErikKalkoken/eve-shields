"""Bottle app for Eve Shields."""

import json
import logging

import requests
from bottle import abort, default_app, response, route, run

from .shields import Shield

logging.basicConfig(
    filename="app.log",
    level=logging.WARN,
    format="%(levelname)s %(asctime)s %(message)s",
)

logger = logging.getLogger()

app = default_app()


def _dict_safe_get(dct: dict, *keys):
    """safely get properties in a nested dict. Raises 404 if key not found"""
    for key in keys:
        try:
            dct = dct[key]
        except KeyError:
            abort(404, f"Invalid key: {key}")
    return dct


@route("/zkb-stats/<entity_type>/<entity_id:int>/<topic>")
def zkb_stats(entity_type, entity_id, topic):
    """endpoint for providing zkb stats related shields"""
    logger.debug("Starting...")

    # input validation
    entity_type_map = {
        "character": "characterID",
        "corporation": "corporationID",
        "alliance": "allianceID",
        "faction": "factionID",
        "shipType": "shipTypeID",
        "shipGroup": "groupID",
        "solarSystem": "solarSystemID",
        "region": "regionID",
    }
    if entity_type not in entity_type_map:
        abort(404, f"invalid entity type: {entity_type}")
    else:
        entity_type_zkb = entity_type_map[entity_type]

    stats = _fetch_zkb_stats(entity_id, entity_type_zkb)

    # generating requested shield
    if topic == "activePvpChars":
        label = "Active PVP chars"
        value = _dict_safe_get(stats, "activepvp", "characters", "count")
        color = "informational"
        shield_format = Shield.FORMAT_NUMBER

    elif topic == "corpCount":
        label = "Corporations"
        value = _dict_safe_get(stats, "info", "corpCount")
        color = "informational"
        shield_format = Shield.FORMAT_NUMBER

    elif topic == "dangerRatio":
        danger_ratio = _dict_safe_get(stats, "dangerRatio")
        label = "Danger"
        shield_format = None
        if danger_ratio > 50:
            value = f"Dangerous {danger_ratio}%"
            color = "red"
        else:
            value = f"Snuggly {100 - danger_ratio}%"
            color = "green"

    elif topic == "iskDestroyed":
        label = "ISK Destroyed"
        value = _dict_safe_get(stats, "iskDestroyed")
        color = "success"
        shield_format = Shield.FORMAT_ISK

    elif topic == "iskLost":
        label = "ISK Lost"
        value = _dict_safe_get(stats, "iskLost")
        color = "critical"
        shield_format = Shield.FORMAT_ISK

    elif topic == "iskEff":
        destroyed = _dict_safe_get(stats, "iskDestroyed")
        lost = _dict_safe_get(stats, "iskLost")
        label = "ISK Efficiency"
        if destroyed + lost > 0:
            value = destroyed / (destroyed + lost) * 100
        else:
            value = 0
        if value < 50:
            color = "critical"
        else:
            color = "success"
        shield_format = Shield.FORMAT_PERCENT

    elif topic == "memberCount":
        label = "Members"
        value = _dict_safe_get(stats, "info", "memberCount")
        color = "informational"
        shield_format = Shield.FORMAT_NUMBER

    elif topic == "shipsDestroyed":
        label = "Ships Destroyed"
        value = _dict_safe_get(stats, "shipsDestroyed")
        color = "success"
        shield_format = Shield.FORMAT_NUMBER

    elif topic == "shipsLost":
        label = "Ships Lost"
        value = _dict_safe_get(stats, "shipsLost")
        color = "critical"
        shield_format = Shield.FORMAT_NUMBER

    elif topic == "shipsEff":
        destroyed = _dict_safe_get(stats, "shipsDestroyed")
        lost = _dict_safe_get(stats, "shipsLost")
        label = "Ships Efficiency"
        if destroyed + lost > 0:
            value = destroyed / (destroyed + lost) * 100
        else:
            value = 0
        if value < 50:
            color = "critical"
        else:
            color = "success"
        shield_format = shield_format = Shield.FORMAT_PERCENT

    else:
        abort(404, f"Invalid property: {topic}")

    shield = Shield(
        label=label, message=value, color=color, shield_format=shield_format
    )

    response.content_type = "application/json"
    response.add_header("Cache-Control", f"max-age={Shield.CACHE_SECONDS}")
    response.add_header("Access-Control-Allow-Origin", "*")
    response.add_header("Access-Control-Allow-Methods", "GET")
    logger.info("Sending response...")
    return json.dumps(shield.get_api_dict())


def _fetch_zkb_stats(entity_id, entity_type_zkb):
    logger.debug("Requesting stats from ZKB API")
    url = f"https://zkillboard.com/api/stats/{entity_type_zkb}/{entity_id}/"
    headers = {
        "Cache-Control": f"max-age={Shield.CACHE_SECONDS}",
        "Accept": "application/json",
    }
    res = requests.get(url, headers=headers, timeout=10)
    res.raise_for_status()
    stats = res.json()
    logger.debug("Stats received from ZKB")
    return stats


if __name__ == "__main__":
    run(host="localhost", port=8000)
