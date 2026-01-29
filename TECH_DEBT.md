# Technical Debt - F1 Companion

> **Last Updated:** 2026-01-29
> **Code Rating:** 5.63/10 (pylint)

---

## 📊 Summary

| Category | Count | Severity |
|----------|-------|----------|
| Code Quality | 6 | Medium |
| Dead Code | 4 | Low |
| Missing Tests | 1 | High |
| Architecture | 3 | Medium |
| Documentation | 2 | Low |

---

## 🔴 High Priority

### TD-001: No Unit Tests
**Location:** Project-wide
**Impact:** Cannot verify functionality, risky refactoring

**Current State:**
- No test files exist
- No pytest configuration
- No CI/CD pipeline

**Resolution:**
```bash
# Add to requirements.txt
pytest>=7.0.0
pytest-cov>=4.0.0

# Create tests/
tests/
├── __init__.py
├── conftest.py
├── test_csv_handler.py
├── test_data_parsing.py
```

**Estimated Time:** 2-3 hours

---

## 🟡 Medium Priority

### TD-002: Import Order Issues
**Location:** `api/csv_handler.py`
**Issue:** Standard library imports after third-party imports

```python
# Current (wrong)
import pandas as pd
from typing import Optional, Dict, List, Any, Tuple

# Should be
from typing import Optional, Dict, List, Any, Tuple
import pandas as pd
```

**Estimated Time:** 5 minutes

---

### TD-003: Unused Import
**Location:** `api/csv_handler.py:11`
**Issue:** `datetime` imported but never used

```python
from datetime import datetime  # REMOVE - unused
```

**Estimated Time:** 1 minute

---

### TD-004: Trailing Whitespace
**Location:** `api/csv_handler.py` (10 lines)
**Issue:** Lines 222, 226, 228, 236, 248, 250, 259, 274, 280, 284, 291

**Resolution:** Run formatter
```bash
black api/csv_handler.py
# or
autopep8 --in-place api/csv_handler.py
```

**Estimated Time:** 2 minutes

---

### TD-005: File Encoding Not Specified
**Location:** `api/csv_handler.py:48`
**Issue:** `open()` without encoding parameter

```python
# Current
with open(self.standings_path, 'r') as f:

# Should be
with open(self.standings_path, 'r', encoding='utf-8') as f:
```

**Estimated Time:** 1 minute

---

### TD-006: Unused Function Parameter
**Location:** `api/csv_handler.py:275`
**Issue:** `cache_dir` parameter in `ErgastAPI.__init__` is ignored

```python
def __init__(self, cache_dir: str = None):  # cache_dir unused
```

**Resolution:** Either use it or document why it's kept for compatibility

**Estimated Time:** 5 minutes

---

### TD-007: Duplicate API Handler Files
**Location:** `api/`
**Issue:** Both `api_handler.py` (391 lines) and `csv_handler.py` (299 lines) exist

**Current State:**
- `api_handler.py` - Dead code (Ergast API offline)
- `csv_handler.py` - Active code

**Options:**
1. Delete `api_handler.py` entirely
2. Keep as reference/documentation
3. Create hybrid that can switch modes

**Recommendation:** Archive to `deprecated/` folder

**Estimated Time:** 10 minutes

---

### TD-008: Hardcoded Data Paths
**Location:** `api/csv_handler.py:30-31`
**Issue:** Data file paths hardcoded relative to module

```python
self.race_data_path = os.path.join(data_dir, 'final_race_data.csv')
self.standings_path = os.path.join(data_dir, 'current_drivers_standings.json')
```

**Resolution:** Move to config file or environment variables

**Estimated Time:** 15 minutes

---

## 🟢 Low Priority

### TD-009: Experimental Code in Repo
**Location:** `experimental/`
**Issue:** 3 unused files (175 lines total)

**Files:**
- `driver_standings.py` (23 lines) - replaced by `list_builder.py`
- `test_api.py` (20 lines) - old API tests
- `turtle_sim.py` (132 lines) - never integrated

**Options:**
1. Delete entirely
2. Move to separate branch
3. Keep with clear README (current)

**Estimated Time:** 5 minutes

---

### TD-010: Race Simulation Code Unused
**Location:** `utils/last_race_sim_data.py` (225 lines)
**Issue:** Large file with experimental race simulation, never integrated into UI

**Options:**
1. Complete and integrate
2. Move to `experimental/`
3. Delete

**Estimated Time:** Varies (2-8 hours to complete, 5 min to remove)

---

### TD-011: Missing Type Hints in UI
**Location:** `ui/*.py`
**Issue:** No type annotations in UI layer

**Example:**
```python
# Current
def __init__(self, parent, api_handler, *args, **kwargs):

# Should be
def __init__(self, parent: tk.Widget, api_handler: ErgastAPI, *args, **kwargs) -> None:
```

**Estimated Time:** 1 hour

---

### TD-012: Inconsistent Naming
**Location:** Various
**Issue:** Mix of naming conventions

**Examples:**
- `Driver_standings` vs `NextRaceView` (class names)
- `top_Bar.py` vs `list_builder.py` (file names)
- `get_driver_standings` vs `get_constructors_championship` (method names)

**Estimated Time:** 30 minutes

---

## 📋 Action Plan

### Sprint 1: Quick Wins (30 min)
- [ ] TD-002: Fix import order
- [ ] TD-003: Remove unused import
- [ ] TD-004: Fix trailing whitespace
- [ ] TD-005: Add encoding to open()
- [ ] TD-006: Document unused parameter

### Sprint 2: Cleanup (1 hour)
- [ ] TD-007: Archive deprecated API handler
- [ ] TD-008: Move paths to config
- [ ] TD-009: Clean experimental folder

### Sprint 3: Tests (3 hours)
- [ ] TD-001: Add pytest setup
- [ ] TD-001: Write tests for csv_handler
- [ ] TD-001: Add GitHub Actions CI

### Sprint 4: Polish (2 hours)
- [ ] TD-011: Add type hints to UI
- [ ] TD-012: Standardize naming
- [ ] TD-010: Decide on race simulation feature

---

## 🔧 Quick Fix Commands

```bash
# Fix formatting issues
cd ~/projects/f1companion
pip install black isort
black api/csv_handler.py
isort api/csv_handler.py

# Run linter
pylint api/csv_handler.py --max-line-length=120

# Run tests (after creating them)
pytest tests/ -v --cov=api
```

---

## 📈 Target Metrics

| Metric | Current | Target |
|--------|---------|--------|
| Pylint Score | 5.63/10 | 8.0/10 |
| Test Coverage | 0% | 70% |
| Type Coverage | ~30% | 80% |
| Dead Code | ~400 lines | 0 |

---

*Document generated by Jarvis*
