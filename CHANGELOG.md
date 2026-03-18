# Changelog

All notable changes to this project will be documented in this file.

## [0.1.7] - 2026-03-18
### Fixed
- `parser.py`: Fixed `_get_compatible_device` where `_token[2]` always overwrote `_token[3]` for `device_host`.
- `parser.py`: Fixed `_handle_oneplus` IndexError on device codes shorter than 2 characters.
- `parser.py`: Fixed `_handle_samsung` IndexError on device codes shorter than 4 characters.
- `parser.py`: Fixed legacy parser not recognizing iPhone model identifiers like `iPhone16,3`.
- `advanced_engine.py`: Fixed mutable cached result aliasing — `lru_cache` results are now copied with `dataclasses.replace()` before mutation.
- `advanced_engine.py`: Fixed `BrowserCapabilities` missing `vr_support` and `webxr_support` fields causing OculusBrowser parsing to crash.
- `advanced_engine.py`: Fixed Chrome iOS (`CriOS`) not being recognized by the advanced browser detection engine.

### Added
- Python 3.14 and 3.15 support in CI matrix and PyPI classifiers.

### Changed
- Bumped `ruff` dependency from `^0.1.8` to `>=0.4` for Python 3.14+ compatibility.

## [0.1.5] - 2025-05-19
### Added
- SEO refresh: README now includes project badges and a star prompt.
- Rich project metadata (description & keywords) added to pyproject for better PyPI search ranking.

### Changed
- Version bumped to 0.1.5.

## [0.1.1]
### Added
- Docs added.

## [0.1.0]
### Added
- Initial release.
