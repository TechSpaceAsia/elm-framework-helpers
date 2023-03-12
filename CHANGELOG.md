# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.6] - 2023-03-012

### Added

- Add `log_file_to_observable` to map a log file in _correct_ format to a list of `on_next` messages
- Add `setup_logger` that creates a logger/formatter for the above _correct_ format
- Add logging to `retry_with_delay`
- Add `assert_equal_messages` for testing Recorded correctly (pending a fix for this: https://github.com/ReactiveX/RxPY/issues/691)