# F1 Companion Tests

## Running Tests

### Setup
```bash
# Install test dependencies
pip install -r requirements-dev.txt
```

### Run All Tests
```bash
pytest tests/ -v
```

### Run Only Unit Tests
```bash
pytest tests/ -m unit -v
```

### Run Only Integration Tests
```bash
pytest tests/ -m integration -v
```

### With Coverage
```bash
pytest tests/ --cov=api --cov-report=html
# Open htmlcov/index.html to view detailed coverage
```

## Test Structure

```
tests/
├── conftest.py                        # Shared fixtures
├── test_csv_handler.py                # Unit tests (basic functionality)
└── test_csv_handler_integration.py   # Integration tests (real data)
```

### Unit Tests
- Test basic functionality with minimal fixtures
- Fast, isolated, no external dependencies
- Ideal for TDD and rapid iteration

### Integration Tests
- Test with real project data files
- Verify actual behavior with production data
- Automatically skip if data files not present

## Coverage

Current coverage for `api/csv_handler.py`: **85%**

Uncovered lines are mostly:
- Dead code branches (old API handlers)
- Error handling for edge cases
- Experimental features

## CI/CD Integration

The pytest config is CI-ready. Add to GitHub Actions:

```yaml
- name: Install dependencies
  run: |
    pip install -r requirements.txt
    pip install -r requirements-dev.txt

- name: Run tests
  run: pytest tests/ -v --cov=api --cov-report=xml

- name: Upload coverage
  uses: codecov/codecov-action@v3
```

## Adding New Tests

1. **Unit tests:** Add to `test_csv_handler.py` with `@pytest.mark.unit`
2. **Integration tests:** Add to `test_csv_handler_integration.py` with `@pytest.mark.integration`
3. **New fixtures:** Add to `conftest.py`

Example:
```python
@pytest.mark.unit
def test_my_feature(csv_handler):
    result = csv_handler.my_method()
    assert result is not None
```
