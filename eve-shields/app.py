from bottle import route, run, response, request, default_app, abort
from json import dumps
import requests
import logging

logging.basicConfig(
    filename='app.log',
    level=logging.WARN,
    format='%(levelname)s %(asctime)s %(message)s'
)

logger = logging.getLogger()

app = default_app()

class Shield:
    """Defines a shield"""
    # cache duration in seconds for a shield
    CACHE_SECONDS = 1800

    # define formats for output
    FORMAT_ISK = 'isk'
    FORMAT_NUMBER = 'number'
    FORMAT_PERCENT = 'percent'
    FORMATS_DEF = [
        FORMAT_ISK,
        FORMAT_NUMBER,
        FORMAT_PERCENT
    ]

    def __init__(
            self, 
            label: str, 
            message: str, 
            color:str = None,
            format:str = None):
        self._schema_version = "1"
        self.label = label
        self.message = message
        self.color = color
        self.format = format
        
    @property
    def schema_version(self) -> str:
        return self._schema_version

    @property
    def label(self) -> str:
        return self._label

    @label.setter
    def label(self, value: str):        
        if value is None:
            raise ValueError('value can not be None')
        self._label = str(value)

    @property
    def message(self) -> str:
        return self._message

    @message.setter
    def message(self, value):
        if value is None:
            raise ValueError('value can not be None')
        if len(str(value)) == 0:
            raise ValueError('value can not be empty')
        self._message = value

    @property
    def color(self) -> str:
        return self._color

    @color.setter
    def color(self, value: str):
        self._color = str(value) if value is not None else None

    @property
    def format(self) -> str:
        return self._format

    @format.setter
    def format(self, value: str):
        if value is not None and value not in self.FORMATS_DEF:
            raise ValueError('invalid format')
        self._format = value

    def get_api_dict(self) -> dict:
        """returns dict for shields.io API"""
       
        d = {
            'schemaVersion': self.schema_version,
            'label': self.label,
            'message': self._formatValue(self.message, self.format),
            'cacheSeconds': self.CACHE_SECONDS
        }
        if self.color is not None:
            d['color'] = self.color
        
        return d   

    def _formatValue(self, value, format: str) -> str:
        """formats the value as specified"""
        if format is not None and format not in self.FORMATS_DEF:
            raise ValueError('invalid format')
        if format == self.FORMAT_ISK:
            txt = self._format_isk(value)
        elif format == self.FORMAT_NUMBER:
            txt = '{:,}'.format(value)
        elif format == self.FORMAT_PERCENT:
            txt = '{:.0f}%'.format(value)
        else:
            if isinstance(value, bool):
                txt = 'yes' if value else 'no'
            else:
                txt = str(value)
        return txt
    
    def _format_isk(self, value: float) -> str:
        """convert a value to an ISK string"""
        v = float(value)
        if v > 10**12:
            p = 12
            ext = "t"
        elif v > 10**9:
            p = 9
            ext = "b"
        elif v > 10**6:
            p = 6
            ext = "m"
        elif v > 10**3:
            p = 3
            ext = "k"
        else:
            p = 0
            ext = ""
        
        return '{:,.1f}{}'.format(v / (10**p), ext)


def _dict_safe_get(dct: dict, *keys):
    """safely get properties in a nested dict. Raises 404 if key not found"""
    for key in keys:
        try:
            dct = dct[key]
        except KeyError:            
            abort(404, 'Invalid key: {}'.format(key))            
    return dct


@route('/zkb-stats/<entity_type>/<entity_id:int>/<property>')
def zkb_stats(entity_type, entity_id, property):
    """endpoint for providing zkb stats related shields"""
    try:
        logger.debug('Starting...')
        
        # input validation
        entity_type_map = {            
            'character': 'characterID',
            'corporation': 'corporationID',
            'alliance': 'allianceID',
            'faction': 'factionID',
            'shipType': 'shipTypeID',
            'shipGroup': 'groupID',
            'solarSystem': 'solarSystemID',
            'region': 'regionID'
        }
        if entity_type not in entity_type_map:
            abort(404, "invalid entity type: {}".format(entity_type))
        else:
            entity_type_zkb = entity_type_map[entity_type]

        logger.debug('Requesting stats from ZKB API')
        url = 'https://zkillboard.com/api/stats/{}/{}/'.format(
            entity_type_zkb, 
            entity_id
            )
        headers = {
            'Cache-Control': 'max-age={}'.format(Shield.CACHE_SECONDS),
            'Accept': 'application/json'
        }
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        stats = res.json()

        logger.debug('Stats received from ZKB')   

        # generating requested shield
        if property == 'activePvpChars':
            label = "Active PVP chars"
            value = _dict_safe_get(stats, 'activepvp', 'characters', 'count')
            color = "informational"
            format = Shield.FORMAT_NUMBER

        elif property == 'corpCount':
            label = "Corporations"
            value = _dict_safe_get(stats, 'info', 'corpCount')            
            color = "informational"
            format = Shield.FORMAT_NUMBER

        elif property == "dangerRatio":
            dangerRatio = _dict_safe_get(stats, 'dangerRatio')
            label = "Danger"
            format = None
            if dangerRatio > 50:
                value = "Dangerous {}%".format(dangerRatio)
                color = "red"                
            else:                
                value = "Snuggly {}%".format(100 - dangerRatio)
                color = "green"       

        elif property == 'iskDestroyed':
            label = "ISK Destroyed"
            value = _dict_safe_get(stats, 'iskDestroyed')
            color = "success"
            format = Shield.FORMAT_ISK

        elif property == 'iskLost':
            label = "ISK Lost"
            value = _dict_safe_get(stats, 'iskLost')
            color = "critical"
            format = Shield.FORMAT_ISK

        elif property == 'iskEff':
            destroyed = _dict_safe_get(stats, 'iskDestroyed')
            lost = _dict_safe_get(stats, 'iskLost')            
            label = "ISK Efficiency"
            if destroyed + lost > 0:
                value = destroyed / (destroyed + lost) * 100
            else:
                value = 0
            if value < 50:
                color = "critical"
            else:
                color = "success"
            format = Shield.FORMAT_PERCENT

        elif property == 'memberCount':
            label = "Members"
            value = _dict_safe_get(stats, 'info', 'memberCount')            
            color = "informational"
            format = Shield.FORMAT_NUMBER
            
        elif property == 'shipsDestroyed':
            label = "Ships Destroyed"
            value = _dict_safe_get(stats, 'shipsDestroyed')            
            color = "success"
            format = Shield.FORMAT_NUMBER

        elif property == 'shipsLost':
            label = "Ships Lost"
            value = _dict_safe_get(stats, 'shipsLost')            
            color = "critical"
            format = Shield.FORMAT_NUMBER

        elif property == 'shipsEff':
            destroyed = _dict_safe_get(stats, 'shipsDestroyed')
            lost = _dict_safe_get(stats, 'shipsLost')            
            label = "Ships Efficiency"
            if destroyed + lost > 0:
                value = destroyed / (destroyed + lost) * 100
            else:
                value = 0                
            if value < 50:
                color = "critical"
            else:
                color = "success"
            format = format = Shield.FORMAT_PERCENT
        
        else:
            abort(404, "Invalid property: {}".format(property))

        shield = Shield(
            label=label,
            message=value,
            color=color,
            format=format
        )        
    except:
        logging.exception("exception ocurred")
        raise
    else:
        response.content_type = 'application/json'
        response.add_header(
            'Cache-Control', 
            'max-age={}'.format(Shield.CACHE_SECONDS)
            )
        response.add_header('Access-Control-Allow-Origin', '*')        
        logger.info("Sending response...")
        return dumps(shield.get_api_dict())

if __name__ == '__main__':
    run(host='localhost', port=8000)