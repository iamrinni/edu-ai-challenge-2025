from typing import Any, Dict, List, Optional, TypeVar, Union, Callable
from datetime import datetime
import re

T = TypeVar('T')

class ValidationError(Exception):
    """Custom exception for validation errors"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class Validator:
    """Base validator class"""
    def __init__(self):
        self._custom_message = None
        self._validators: List[Callable[[Any], bool]] = []
        self._is_optional = False

    def with_message(self, message: str) -> 'Validator':
        """Set a custom error message for validation failures"""
        self._custom_message = message
        return self

    def optional(self) -> 'Validator':
        """Mark this field as optional"""
        self._is_optional = True
        return self

    def validate(self, value: Any) -> bool:
        """Validate the value against all registered validators"""
        if self._is_optional and value is None:
            return True

        for validator in self._validators:
            if not validator(value):
                raise ValidationError(self._custom_message or f"Validation failed for value: {value}")
        return True

class StringValidator(Validator):
    """Validator for string values"""
    def __init__(self):
        super().__init__()
        self._validators.append(lambda x: isinstance(x, str))

    def min_length(self, length: int) -> 'StringValidator':
        """Add minimum length validation"""
        self._validators.append(lambda x: len(x) >= length)
        return self

    def max_length(self, length: int) -> 'StringValidator':
        """Add maximum length validation"""
        self._validators.append(lambda x: len(x) <= length)
        return self

    def pattern(self, pattern: str) -> 'StringValidator':
        """Add regex pattern validation"""
        regex = re.compile(pattern)
        self._validators.append(lambda x: bool(regex.match(x)))
        return self

class NumberValidator(Validator):
    """Validator for numeric values"""
    def __init__(self):
        super().__init__()
        self._validators.append(lambda x: isinstance(x, (int, float)))

    def min(self, value: Union[int, float]) -> 'NumberValidator':
        """Add minimum value validation"""
        self._validators.append(lambda x: x >= value)
        return self

    def max(self, value: Union[int, float]) -> 'NumberValidator':
        """Add maximum value validation"""
        self._validators.append(lambda x: x <= value)
        return self

class BooleanValidator(Validator):
    """Validator for boolean values"""
    def __init__(self):
        super().__init__()
        self._validators.append(lambda x: isinstance(x, bool))

class DateValidator(Validator):
    """Validator for date values"""
    def __init__(self):
        super().__init__()
        self._validators.append(lambda x: isinstance(x, datetime))

class ObjectValidator(Validator):
    """Validator for object/dictionary values"""
    def __init__(self, schema: Dict[str, Validator]):
        super().__init__()
        self.schema = schema

    def validate(self, value: Dict[str, Any]) -> bool:
        """Validate an object against its schema"""
        if not isinstance(value, dict):
            raise ValidationError(f"Expected dict, got {type(value)}")

        for key, validator in self.schema.items():
            if key not in value:
                if not validator._is_optional:
                    raise ValidationError(f"Missing required field: {key}")
            else:
                validator.validate(value[key])
        return True

class ArrayValidator(Validator):
    """Validator for array/list values"""
    def __init__(self, item_validator: Validator):
        super().__init__()
        self.item_validator = item_validator
        self._validators.append(lambda x: isinstance(x, list))

    def validate(self, value: List[Any]) -> bool:
        """Validate all items in the array"""
        if self._is_optional and value is None:
            return True
            
        super().validate(value)
        for item in value:
            self.item_validator.validate(item)
        return True

class Schema:
    """Schema builder class"""
    @staticmethod
    def string() -> StringValidator:
        """Create a string validator"""
        return StringValidator()

    @staticmethod
    def number() -> NumberValidator:
        """Create a number validator"""
        return NumberValidator()

    @staticmethod
    def boolean() -> BooleanValidator:
        """Create a boolean validator"""
        return BooleanValidator()

    @staticmethod
    def date() -> DateValidator:
        """Create a date validator"""
        return DateValidator()

    @staticmethod
    def object(schema: Dict[str, Validator]) -> ObjectValidator:
        """Create an object validator with the given schema"""
        return ObjectValidator(schema)

    @staticmethod
    def array(item_validator: Validator) -> ArrayValidator:
        """Create an array validator with the given item validator"""
        return ArrayValidator(item_validator) 