# 0x03. Unittests and Integration Tests

## 📌 Description

This project covers **unit testing** and **integration testing** in Python using the `unittest` framework, `parameterized`, and mocking techniques.  

The goal is to test pure functions in isolation, simulate edge cases, and understand the difference between unit tests and integration tests.

---

## 🧪 Task: Test `utils.access_nested_map`

### File: `utils.py`

The function `access_nested_map(nested_map, path)` retrieves a value from a nested dictionary using a tuple/list of keys.

```python
def access_nested_map(nested_map, path):
    for key in path:
        nested_map = nested_map[key]
    return nested_map
# Unittest

