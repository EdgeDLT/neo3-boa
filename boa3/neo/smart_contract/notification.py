from typing import Any, Dict, Tuple

from boa3.neo.utils import stack_item_from_json


class Notification:
    def __init__(self, event_name: str, script_hash: bytes, *value: Any):
        self._event_name: str = event_name
        self._script_hash: bytes = script_hash
        self._value: Tuple[Any] = value

    @property
    def name(self) -> str:
        return self._event_name

    @property
    def origin(self) -> bytes:
        return self._script_hash

    @property
    def arguments(self) -> tuple:
        return self._value

    @classmethod
    def from_json(cls, json: Dict[str, Any]):
        """
        Creates a Notification object from a json.

        :param json: json that contains the notification data
        :return: a Notification object
        :rtype: Notification
        """
        keys = set(json.keys())
        if not keys.issubset(['eventName', 'scriptHash', 'value']):
            return None

        name: str = json["eventName"] if "eventName" in json else ""
        script: bytes = json["scriptHash"] if "scriptHash" in json else b''
        try:
            value: Any = stack_item_from_json(json["value"]) if "value" in json else []
        except ValueError:
            value = []

        if not isinstance(value, list):
            value = [value]

        return cls(name, script, *value)

    def __str__(self) -> str:
        return '{0}({1})'.format(self._event_name, ', '.join(self._value))
