from typing import Optional, Iterable, Any
import re

from api_builder.schema.exceptions import ValidationError


class Range:
    """ Is >= min and <= max """

    def __init__(self, min: Optional[int] = None, max: Optional[int] = None):
        self.min = min
        self.max = max

    def __call__(self, value):
        if self.min is not None and value < self.min:
            raise ValidationError(f"Should be >= {self.min}")
        if self.max is not None and value > self.max:
            raise ValidationError(f"Should be <= {self.max}")


class Length:
    """ Length is >= min and <= max """

    def __init__(self, min: Optional[int] = None, max: Optional[int] = None):
        self.min = min
        self.max = max

    def __call__(self, value):
        if self.min is not None and len(value) < self.min:
            raise ValidationError(f"Length should be >= {self.min}")
        if self.max is not None and len(value) > self.max:
            raise ValidationError(f"Length should be <= {self.max}")


class OneOf:
    """ Is one of values """

    def __init__(self, values: Iterable[Any] = ()):
        self.values = values

    def __call__(self, value: Any):
        if value not in self.values:
            raise ValidationError(f"Should be one of {self.values}")


class NoneOf:
    """ Is none of values """

    def __init__(self, values: Iterable[Any] = ()):
        self.values = values

    def __call__(self, value: Any):
        if value in self.values:
            raise ValidationError(f"Should not be one of {self.values}")


class Equal:
    """ Is equal to value """

    def __init__(self, value: Any):
        self.value = value

    def __call__(self, value: Any):
        if value != self.value:
            raise ValidationError(f"Should be equal to {self.value}")


class Regexp:
    """ Is match to regex """

    def __init__(self, regexp: str):
        self.regexp = re.compile(regexp)

    def __call__(self, value: str):
        if self.regexp.match(value) is None:
            raise ValidationError(f"Should match to '{self.regexp}' regexp")
