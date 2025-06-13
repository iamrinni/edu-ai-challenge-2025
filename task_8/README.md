# Python Validation Library

A robust, type-safe validation library for Python that lets you define schemas and validate complex data structures. Inspired by modern schema validation libraries, this tool ensures your data is correct, safe, and easy to work with.

---

## Features

- **Type-safe validation** for primitive types: `string`, `number`, `boolean`, `date`
- **Complex types**: arrays and objects
- **Optional field support** (tested both when omitted and when provided)
- **Custom validation rules** and error messages
- **Nested schema validation**
- **Comprehensive test coverage** (99%)

---

## Installation

1. Make sure you have **Python 3.7+** installed
2. Clone this repository
3. Navigate to the `task_8` directory
4. Install dependencies:
   ```bash
   python3 -m pip install -r requirements.txt
   ```
 
---

## Usage Examples

### 1. Basic Object Validation

```python
from validator import Schema

user_schema = Schema.object({
    "name": Schema.string().min_length(2).max_length(50),
    "age": Schema.number().min(0).max(150),
    "email": Schema.string().pattern(r'^[^\s@]+@[^\s@]+\.[^\s@]+$')
})

data = {
    "name": "John Doe",
    "age": 30,
    "email": "john@example.com"
}

try:
    user_schema.validate(data)
    print("Data is valid!")
except ValidationError as e:
    print(f"Validation error: {e}")
```

### 2. String Validation

```python
validator = Schema.string()
validator.validate("test")  # Valid

validator = Schema.string().min_length(2).max_length(5)
validator.validate("test")  # Valid

validator = Schema.string().pattern(r'^\d{5}$')
validator.validate("12345")  # Valid
```


### 3. Number Validation

```python
validator = Schema.number()
validator.validate(123)     # Valid

validator = Schema.number().min(0).max(100)
validator.validate(50)  # Valid
```

### 4. Array Validation

```python
validator = Schema.array(Schema.string())
validator.validate(["a", "b", "c"])  # Valid

validator = Schema.array(Schema.number().min(0).max(100))
validator.validate([1, 50, 99])  # Valid
```

### 5. Optional Fields

```python
validator = Schema.string().optional()
validator.validate(None)     # Valid
validator.validate("test")   # Valid

schema = Schema.object({
    "name": Schema.string(),
    "age": Schema.number().optional()
})

schema.validate({"name": "John"})             # age omitted
schema.validate({"name": "John", "age": 30})  # age provided
```
## Running Tests

To run the test suite:

```bash
python3 -m unittest test_validator.py
```

To run tests with coverage:

```bash
python3 -m coverage run -m unittest test_validator.py
python3 -m coverage report > test_report.txt
```

The test coverage report will be saved to `test_report.txt`.
**Current coverage:** 99% with 10 passing tests and 222 statements checked.

## Error Handling

The library raises `ValidationError` exceptions when validation fails. You can catch these exceptions to handle validation errors:

```python
from validator import Schema, ValidationError

try:
    schema.validate(data)
except ValidationError as e:
    print(f"Validation failed: {e}")
```

## Custom Error Messages

You can provide custom error messages for validation failures:

```python
validator = Schema.string().with_message("Custom error message")
try:
    validator.validate(123)
except ValidationError as e:
    print(e)  # Outputs: "Custom error message"
```

## Contributing

Feel free to submit issues and enhancement requests! 
