"""Shield class for Eve Shields."""


# pylint: disable = too-many-instance-attributes
class Shield:
    """Defines a shield"""

    # cache duration in seconds for a shield
    CACHE_SECONDS = 1800

    # define formats for output
    FORMAT_ISK = "isk"
    FORMAT_NUMBER = "number"
    FORMAT_PERCENT = "percent"
    FORMATS_DEF = [FORMAT_ISK, FORMAT_NUMBER, FORMAT_PERCENT]

    def __init__(
        self, label: str, message: str, color: str = None, shield_format: str = None
    ):
        self._schema_version = 1
        self.label = label
        self.message = message
        self.color = color
        self.shield_format = shield_format

    @property
    def schema_version(self) -> int:
        """Return schema version."""
        return self._schema_version

    @property
    def label(self) -> str:
        """Return label."""
        return self._label

    @label.setter
    def label(self, value: str):
        """Set label."""
        if value is None:
            raise ValueError("value can not be None")
        self._label = str(value)

    @property
    def message(self) -> str:
        """Return message."""
        return self._message

    @message.setter
    def message(self, value):
        """Set message."""
        if value is None:
            raise ValueError("value can not be None")
        if len(str(value)) == 0:
            raise ValueError("value can not be empty")
        self._message = value

    @property
    def color(self) -> str:
        """Return color."""
        return self._color

    @color.setter
    def color(self, value: str):
        """Set color."""
        self._color = str(value) if value is not None else None

    @property
    def shield_format(self) -> str:
        """Return shield format."""
        return self._format

    @shield_format.setter
    def shield_format(self, value: str):
        """Set shield format."""
        if value is not None and value not in self.FORMATS_DEF:
            raise ValueError("invalid format")
        self._format = value

    def get_api_dict(self) -> dict:
        """Return dict for shields.io API."""

        api_dict = {
            "schemaVersion": self.schema_version,
            "label": self.label,
            "message": self._format_value(self.message, self.shield_format),
            "cacheSeconds": self.CACHE_SECONDS,
        }
        if self.color is not None:
            api_dict["color"] = self.color

        return api_dict

    def _format_value(self, value, shield_format: str) -> str:
        """Return formatted value."""
        if shield_format is not None and shield_format not in self.FORMATS_DEF:
            raise ValueError("invalid format")
        if shield_format == self.FORMAT_ISK:
            txt = self._humanize_amount(value)
        elif shield_format == self.FORMAT_NUMBER:
            txt = self._humanize_amount(value)
        elif shield_format == self.FORMAT_PERCENT:
            txt = f"{value:.0f}%"
        else:
            if isinstance(value, bool):
                txt = "yes" if value else "no"
            else:
                txt = str(value)
        return txt

    def _humanize_amount(self, value: float) -> str:
        """Humanize amount number for output."""
        my_value = float(value)
        if my_value > 10**12:
            power = 12
            suffix = "t"
        elif my_value > 10**9:
            power = 9
            suffix = "b"
        elif my_value > 10**6:
            power = 6
            suffix = "m"
        elif my_value > 10**3:
            power = 3
            suffix = "k"
        else:
            power = 0
            suffix = ""

        if power > 0:
            result = my_value / (10**power)
            return f"{result:,.1f}{suffix}"

        return str(value)
