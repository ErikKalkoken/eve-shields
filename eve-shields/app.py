from bottle import route, run, response, request, default_app
from json import dumps
import requests
import logging

logging.basicConfig(
    filename='app.log',
    level=logging.WARN,
    format='%(levelname)s %(asctime)s %(message)s'
)

logger = logging.getLogger()


class Shield:
    """Defines a shield"""
    
    # define formats for output
    FORMAT_ISK = 'isk'    
    FORMATS_DEF = [
        FORMAT_ISK
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
            'message': self._formatValue(self.message, self.format)
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
        
        return str(round(v / (10**p), 1)) + ext

def _get_nested_dict_value(property: str, stats: dict):
    """returns the value in nested dict specified by p1 or p1-p2"""
    path = property.split('-')    
    if len(path) <= 2:
        if path[0] not in stats:
            raise KeyError('property:{} not found'. format(path[0]))
        if len(path) == 1:
            value = stats[path[0]]
        elif len(path) == 2:
            if path[1] not in stats[path[0]]:
                raise KeyError('property:{} not found'.format(path[1]))
            else:
                value = stats[path[0]][path[1]]
    else:
        raise ValueError('Too many keys:{}'.format(property))
        
    return value


@route('/zkb-stats/<entity_type>/<entity_id>/<key>')
def zkb_stats(entity_type, entity_id, key):
    """endpoint for providing zkb stats related shields"""
    try:
        logger.debug('Starting...')
        
        logger.debug('Requesting stats from ZKB API')
        url = 'https://zkillboard.com/api/stats/{}/{}/'.format(entity_type, entity_id)
        res = requests.get(url)
        res.raise_for_status()
        stats = res.json()

        logger.debug('Stats received from ZKB')

        shield = Shield(
            label=request.query.label if 'label' in request.query else key,
            message=_get_nested_dict_value(key, stats), 
            color=request.query.color if 'color' in request.query else None,
            format=request.query.format if 'format' in request.query else None
        )        
    except:
        logging.exception("exception ocurred")
        raise
    else:
        response.content_type = 'application/json'
        logger.info("Sending response...")
        return dumps(shield.get_api_dict())

app = default_app()

if __name__ == '__main__':
    run(host='localhost', port=8000)