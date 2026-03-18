# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Essential Commands

### Testing
```bash
# Run all tests
poetry run pytest

# Run specific test file
poetry run pytest tests/test_user_agent_parser.py

# Run a single test by name
poetry run pytest -k "test_function_name"

# Run tests with coverage report (matches CI)
poetry run pytest -q --cov=user_agent_parser --cov-report=xml
```

### Code Quality
```bash
# Lint and format
poetry run ruff check && poetry run ruff format
```

### Development Setup
```bash
poetry install
```

## High-Level Architecture

### Dual API Surface
The library exposes two parsing APIs through `__init__.py`:

1. **Legacy API** — `parse()` and `Parser` class in `parser.py`. Returns a 7-tuple: `(browser, browser_version, os, os_version, device_type, device_name, device_host)`. `parse()` wraps `_cached_parse_user_agent()` with LRU caching for high throughput.

2. **Advanced API** — `analyze()`, `batch_analyze()`, `generate_analytics()` backed by `advanced_engine.py` and `analytics.py`. Returns `AdvancedResult` dataclasses with confidence scoring, device categorization, browser capabilities, and security fingerprinting.

### Core Parser (`parser.py`)
- Single `Parser` class with **lazy initialization** — parsing occurs only when properties are accessed or `__call__()` is invoked
- **Platform-specific device handlers** via dynamic method dispatch (`_get_{platform}_device`)
- **Browser detection** uses ordered `browser_rules` tuple — earlier rules take precedence, regex patterns with cached compiled patterns

### User Agent Parsing Flow
1. **Platform Extraction**: `get_str_from_long_text_under_bract()` extracts content within first parentheses
2. **Device Detection**: Routes to specialized handlers based on platform token (iPhone, Android, Windows, etc.)
3. **Browser Identification**: Applies regex rules from `browser_rules` with cached compiled patterns

### Advanced Engine (`advanced_engine.py`)
- `AdvancedUserAgentEngine` with ML-inspired pattern matching and confidence scoring
- `DeviceCategory` enum for fine-grained classification (smartphone, tablet, smart_tv, gaming_console, etc.)
- `BrowserCapabilities` and `SecurityFingerprint` dataclasses for rich metadata
- Batch processing via `ThreadPoolExecutor`

### Analytics (`analytics.py`)
- `UserAgentAnalytics` generates `AnalyticsReport` with browser/OS/device distributions
- `BatchProcessor` for parallel processing of large UA datasets
- Export to JSON/CSV formats

### Key Data Files
- **`constants.py`**: `OS`, `DeviceType`, `DeviceName` constants and `MOBILE_DEVICE_CODE_NAME` dictionary mapping model codes to readable names
- **`modern_devices.py`**: `DeviceSpec` dataclass and database of 2024-2025 device specs (iPhone 15, Galaxy S24, etc.)

## Extension Points

### Adding New Device Support
1. **Known Devices**: Add entries to `MOBILE_DEVICE_CODE_NAME` in `constants.py`
2. **New Device Families**: Extend prefix mapping in `_get_device_name_from_code()`
3. **Platform Support**: Add new `_get_{platform}_device()` method in `parser.py`
4. **Modern Devices**: Add `DeviceSpec` entries in `modern_devices.py`

### Adding Browser Detection
- Extend `browser_rules` tuple in `Parser` class — earlier entries have higher priority
- Use regex patterns compatible with `_browser_version_re` template

## Development Notes

- **Poetry** for dependency management
- **Ruff** for linting and formatting: 120 char line length, `"double"` quote style
- **Python 3.8+** compatibility required
- CI runs against Python 3.8–3.15 matrix with **Codecov** integration (3.15 is allow-failure)
- Tests use `@pytest.mark.parametrize` with real UA strings in `test_utils.py`