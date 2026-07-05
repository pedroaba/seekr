from dataclasses import asdict, is_dataclass
from inspect import isclass, getattr_static


class InternalJsonEncoder:
    @staticmethod
    def encode(obj):
        has_to_json_fn = hasattr(obj, "to_json")

        if has_to_json_fn:
            json_value = {}

            is_callable_fn = callable(getattr(obj, "to_json", None))
            if is_callable_fn:
                json_value = obj.to_json()
                if not isinstance(json_value, dict):
                    raise TypeError("to_json method must return a dict")

            is_property_fn = isinstance(getattr_static(obj, "to_json", None), property)
            if is_property_fn:
                json_value = obj.to_json

            return json_value

        if is_dataclass(obj) and not isclass(obj):
            return asdict(obj)

        if not is_dataclass(obj) and isclass(obj):
            return vars(obj)

        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
