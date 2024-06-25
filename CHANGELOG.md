# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
[markdownlint](https://dlaa.me/markdownlint/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.5.6] - 2024-06-24

### Changed in 1.5.6

- In `Dockerfile`, updated FROM instruction to `senzing/senzingapi-runtime:3.10.3`

## [1.5.5] - 2024-05-22

### Changed in 1.5.5

- In `Dockerfile`, updated FROM instruction to `senzing/senzingapi-runtime:3.7.1`
- In `requirements.txt`, updated:
  - Flask==3.0.3

## [1.5.4] - 2023-09-29

### Changed in 1.5.4

- In `Dockerfile`, updated FROM instruction to `senzing/senzingapi-runtime:3.7.1`
- In `requirements.txt`, updated:
  - Flask==2.3.3

## [1.5.3] - 2023-06-15

### Changed in 1.5.3

- In `Dockerfile`, updated FROM instruction to `senzing/senzingapi-runtime:3.5.3`
- In `requirements.txt`, updated:
  - Flask==2.3.2

## [1.5.2] - 2023-04-04

### Changed in 1.5.2

- In `Dockerfile`, updated FROM instruction to `senzing/senzingapi-runtime:3.5.0`
- In `requirements.txt`, updated:
  - Flask==2.2.3

## [1.5.1] - 2022-09-29

### Changed in 1.5.1

- In `Dockerfile`, updated FROM instruction to `senzing/senzingapi-runtime:3.3.0`

## [1.5.0] - 2022-09-07

### Changed in 1.5.0

- Migrated to `senzing/senzingapi-runtime` as Docker base images

### Added to 1.5.0

## [1.4.4] - 2022-03-22

### Added to 1.4.4

- Support for enhanced v3 python package styles
- Support for `libcrypto` and `libssl`
- Upgrade to senzing/senzing-base:1.6.5

## [1.4.3] - 2021-10-11

### Added to 1.4.3

- Upgrade to senzing/senzing-base:1.6.2

## [1.4.2] - 2021-08-05

### Added to 1.4.2

- Upgrade to senzing/senzing-base:1.6.1

## [1.4.1] - 2020-07-23

### Changed in 1.4.1

- Upgrade to senzing/senzing-base:1.5.2

## [1.4.0] - 2020-01-29

### Changed in 1.4.0

- Update to senzing/senzing-base:1.4.0

## [1.3.0] - 2019-11-15

### Added in 1.3.0

- Added MSSQL support
- Update to senzing/senzing-base:1.3.0

## [1.2.0] - 2019-09-01

### Changed in 1.2.0

- RPM based installation

## [1.1.0] - 2019-07-24

### Added in 1.1.0

- Now a non-root, immutable container
- Based on `senzing/senzing-base:1.1.0`, a non-root, immutable container

## [1.0.1] - 2019-07-11

### Added in 1.0.1

- Support for Python3

## [1.0.0] - 2019-06-24

### Added in 1.0.0

- Simple Python Flask app showing Senzing integration
  - Version, License, Config, Summary
- Dockerized using `FROM senzing/senzing-base`
