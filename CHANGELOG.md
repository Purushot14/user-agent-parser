# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0] - 2026-03-18

### Added
- `AdvancedUserAgentEngine` with ML-inspired pattern matching and confidence scoring.
- `DeviceCategory` enum: smartphone, tablet, desktop, laptop, smart_tv, gaming_console, smart_watch, iot_device, bot.
- `BrowserCapabilities` dataclass: WebGL, WebRTC, Service Worker, PWA, touch, VR/XR support flags.
- `SecurityFingerprint` dataclass: privacy mode, ad-blocker, tracking protection detection.
- `AdvancedResult` dataclass with confidence score, detection level, browser engine, device brand/model.
- `analyze()` — single UA advanced analysis.
- `batch_analyze()` — parallel batch processing via `ThreadPoolExecutor`.
- `generate_analytics()` — `AnalyticsReport` with browser/OS/device distributions, export to JSON/CSV.
- `UserAgentAnalytics` and `BatchProcessor` for large-scale UA dataset processing.
- Modern device database (`modern_devices.py`) covering 2024–2025 devices.
- `CLAUDE.md` project guidance for Claude Code.
- Benchmark scripts (`benchmark.py`, `advanced_benchmark.py`).

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
