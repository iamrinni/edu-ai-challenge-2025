import unittest
from datetime import datetime
from validator import Schema, ValidationError

class TestValidator(unittest.TestCase):
    def test_string_validator(self):
        # Basic string validation
        validator = Schema.string()
        self.assertTrue(validator.validate("test"))
        with self.assertRaises(ValidationError):
            validator.validate(123)

        # String length validation
        validator = Schema.string().min_length(2).max_length(5)
        self.assertTrue(validator.validate("test"))
        with self.assertRaises(ValidationError):
            validator.validate("a")
        with self.assertRaises(ValidationError):
            validator.validate("toolong")

        # Pattern validation
        validator = Schema.string().pattern(r'^\d{5}$')
        self.assertTrue(validator.validate("12345"))
        with self.assertRaises(ValidationError):
            validator.validate("1234")

    def test_number_validator(self):
        # Basic number validation
        validator = Schema.number()
        self.assertTrue(validator.validate(123))
        self.assertTrue(validator.validate(123.45))
        with self.assertRaises(ValidationError):
            validator.validate("123")

        # Range validation
        validator = Schema.number().min(0).max(100)
        self.assertTrue(validator.validate(50))
        with self.assertRaises(ValidationError):
            validator.validate(-1)
        with self.assertRaises(ValidationError):
            validator.validate(101)

    def test_boolean_validator(self):
        validator = Schema.boolean()
        self.assertTrue(validator.validate(True))
        self.assertTrue(validator.validate(False))
        with self.assertRaises(ValidationError):
            validator.validate("true")

    def test_date_validator(self):
        validator = Schema.date()
        self.assertTrue(validator.validate(datetime.now()))
        with self.assertRaises(ValidationError):
            validator.validate("2024-03-20")

    def test_object_validator(self):
        # Simple object validation
        schema = Schema.object({
            "name": Schema.string(),
            "age": Schema.number()
        })
        
        valid_data = {"name": "John", "age": 30}
        self.assertTrue(schema.validate(valid_data))

        # Missing required field
        with self.assertRaises(ValidationError):
            schema.validate({"name": "John"})

        # Invalid field type
        with self.assertRaises(ValidationError):
            schema.validate({"name": "John", "age": "30"})

    def test_array_validator(self):
        # Array of strings
        validator = Schema.array(Schema.string())
        self.assertTrue(validator.validate(["a", "b", "c"]))
        with self.assertRaises(ValidationError):
            validator.validate([1, 2, 3])

        # Array of numbers with range
        validator = Schema.array(Schema.number().min(0).max(100))
        self.assertTrue(validator.validate([1, 50, 99]))
        with self.assertRaises(ValidationError):
            validator.validate([-1, 50, 101])

    def test_optional_fields(self):
        # Test optional string
        validator = Schema.string().optional()
        self.assertTrue(validator.validate(None))
        self.assertTrue(validator.validate("test"))
        with self.assertRaises(ValidationError):
            validator.validate(123)

        # Test optional number
        validator = Schema.number().optional()
        self.assertTrue(validator.validate(None))
        self.assertTrue(validator.validate(42))
        with self.assertRaises(ValidationError):
            validator.validate("42")

        # Test optional field in object
        schema = Schema.object({
            "name": Schema.string(),
            "age": Schema.number().optional()
        })
        
        # Valid with optional field
        self.assertTrue(schema.validate({"name": "John"}))
        self.assertTrue(schema.validate({"name": "John", "age": 30}))
        
        # Invalid when optional field has wrong type
        with self.assertRaises(ValidationError):
            schema.validate({"name": "John", "age": "30"})

    def test_optional_fields_provided(self):
        """Test optional fields when they are provided with valid values"""
        # Test optional string with validation rules
        validator = Schema.string().optional().min_length(2).max_length(5)
        self.assertTrue(validator.validate(None))  # None is valid
        self.assertTrue(validator.validate("test"))  # Valid string
        with self.assertRaises(ValidationError):
            validator.validate("a")  # Too short
        with self.assertRaises(ValidationError):
            validator.validate("toolong")  # Too long

        # Test optional number with range
        validator = Schema.number().optional().min(0).max(100)
        self.assertTrue(validator.validate(None))  # None is valid
        self.assertTrue(validator.validate(50))  # Valid number
        with self.assertRaises(ValidationError):
            validator.validate(-1)  # Below min
        with self.assertRaises(ValidationError):
            validator.validate(101)  # Above max

        # Test optional nested object
        address_schema = Schema.object({
            "street": Schema.string(),
            "city": Schema.string()
        }).optional()

        user_schema = Schema.object({
            "name": Schema.string(),
            "address": address_schema
        })

        # Valid with address provided
        self.assertTrue(user_schema.validate({
            "name": "John",
            "address": {
                "street": "123 Main St",
                "city": "Anytown"
            }
        }))

        # Valid without address
        self.assertTrue(user_schema.validate({
            "name": "John"
        }))

        # Invalid when address is provided but incomplete
        with self.assertRaises(ValidationError):
            user_schema.validate({
                "name": "John",
                "address": {
                    "street": "123 Main St"
                    # Missing city
                }
            })

        # Test optional array
        validator = Schema.array(Schema.string()).optional()
        self.assertTrue(validator.validate(None))  # None is valid
        self.assertTrue(validator.validate(["a", "b", "c"]))  # Valid array
        with self.assertRaises(ValidationError):
            validator.validate([1, 2, 3])  # Invalid array items

    def test_nested_schema(self):
        # Complex nested schema matching the JavaScript example
        address_schema = Schema.object({
            "street": Schema.string(),
            "city": Schema.string(),
            "postalCode": Schema.string().pattern(r'^\d{5}$').with_message('Postal code must be 5 digits'),
            "country": Schema.string()
        })

        user_schema = Schema.object({
            "id": Schema.string().with_message('ID must be a string'),
            "name": Schema.string().min_length(2).max_length(50),
            "email": Schema.string().pattern(r'^[^\s@]+@[^\s@]+\.[^\s@]+$'),
            "age": Schema.number().optional(),
            "isActive": Schema.boolean(),
            "tags": Schema.array(Schema.string()),
            "address": address_schema.optional(),
            "metadata": Schema.object({}).optional()
        })

        valid_user = {
            "id": "12345",
            "name": "John Doe",
            "email": "john@example.com",
            "isActive": True,
            "tags": ["developer", "designer"],
            "address": {
                "street": "123 Main St",
                "city": "Anytown",
                "postalCode": "12345",
                "country": "USA"
            }
        }

        self.assertTrue(user_schema.validate(valid_user))

        # Test with optional fields omitted
        minimal_user = {
            "id": "12345",
            "name": "John Doe",
            "email": "john@example.com",
            "isActive": True,
            "tags": ["developer", "designer"]
        }
        self.assertTrue(user_schema.validate(minimal_user))

        # Test invalid nested data
        invalid_user = valid_user.copy()
        invalid_user["address"]["postalCode"] = "1234"  # Invalid postal code
        with self.assertRaises(ValidationError) as context:
            user_schema.validate(invalid_user)
        self.assertIn("Postal code must be 5 digits", str(context.exception))

    def test_custom_messages(self):
        validator = Schema.string().with_message("Custom error message")
        with self.assertRaises(ValidationError) as context:
            validator.validate(123)
        self.assertEqual(str(context.exception), "Custom error message")

if __name__ == '__main__':
    unittest.main() 