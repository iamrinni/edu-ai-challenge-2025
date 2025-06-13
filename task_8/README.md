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
