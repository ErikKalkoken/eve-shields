class Shield:
    """Defines a shield"""

    # cache duration in seconds for a shield
    CACHE_SECONDS = 1800

    # define formats for output
    FORMAT_ISK = "isk"
    FORMAT_NUMBER = "number"
    FORMAT_PERCENT = "percent"
    FORMATS_DEF = [FORMAT_ISK, FORMAT_NUMBER, FORMAT_PERCENT]

    def __init__(self, label: str, message: str, color: str = None, format: str = None):
        self._schema_version = 1
        self.label = label
        self.message = message
        self.color = color
        self.format = format

    @property
    def schema_version(self) -> int:
        return self._schema_version

    @property
    def label(self) -> str:
        return self._label

    @label.setter
    def label(self, value: str):
        if value is None:
            raise ValueError("value can not be None")
        self._label = str(value)

    @property
    def message(self) -> str:
        return self._message

    @message.setter
    def message(self, value):
        if value is None:
            raise ValueError("value can not be None")
        if len(str(value)) == 0:
            raise ValueError("value can not be empty")
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
            raise ValueError("invalid format")
        self._format = value

    def get_api_dict(self) -> dict:
        """returns dict for shields.io API"""

        d = {
            "schemaVersion": self.schema_version,
            "label": self.label,
            "message": self._formatValue(self.message, self.format),
            "cacheSeconds": self.CACHE_SECONDS,
        }
        if self.color is not None:
            d["color"] = self.color

        return d

    def _formatValue(self, value, format: str) -> str:
        """formats the value as specified"""
        if format is not None and format not in self.FORMATS_DEF:
            raise ValueError("invalid format")
        if format == self.FORMAT_ISK:
            txt = self._format_number(value)
        elif format == self.FORMAT_NUMBER:
            txt = self._format_number(value)
        elif format == self.FORMAT_PERCENT:
            txt = "{:.0f}%".format(value)
        else:
            if isinstance(value, bool):
                txt = "yes" if value else "no"
            else:
                txt = str(value)
        return txt

    def _format_number(self, value: float) -> str:
        """shorten number for output"""
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

        return "{:,.1f}{}".format(v / (10**p), ext) if p > 0 else str(value)
