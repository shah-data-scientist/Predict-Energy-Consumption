# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added
- **Global Policy Enforcement**: Set up `scripts/global_policy/` with validation scripts ([validate_changed_files.py](scripts/global_policy/validate_changed_files.py), [validate_file_locations.py](scripts/global_policy/validate_file_locations.py), [check_orphaned_files.py](scripts/global_policy/check_orphaned_files.py), [mirror_modify_check.py](scripts/global_policy/mirror_modify_check.py))
- **Pre-commit hooks**: Added [.pre-commit-config.yaml](.pre-commit-config.yaml) for automated validation
- **Project tracking**: Added [PROJECT_MEMORY.md](PROJECT_MEMORY.md) and [CHANGELOG.md](CHANGELOG.md)
- **Gitignore**: Updated [.gitignore](.gitignore) with mandatory exclusions from GLOBAL_POLICY.md
