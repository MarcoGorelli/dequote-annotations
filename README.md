[![Build Status](https://github.com/MarcoGorelli/no-string-hints/workflows/tox/badge.svg)](https://github.com/MarcoGorelli/no-string-hints/actions?workflow=tox)
[![Coverage](https://codecov.io/gh/MarcoGorelli/no-string-hints/branch/main/graph/badge.svg)](https://codecov.io/gh/MarcoGorelli/no-string-hints)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/MarcoGorelli/no-string-hints/main.svg)](https://results.pre-commit.ci/latest/github/MarcoGorelli/no-string-hints/main)

no-string-hints
================

A pre-commit hook to automatically remove string literals as type hints from argument, return, and class variable type annotations.

## Installation

`pip install no_string_hints`
## As a pre-commit hook

See [pre-commit](https://github.com/pre-commit/pre-commit) for instructions

Sample `.pre-commit-config.yaml`:

```yaml
-   repo: https://github.com/MarcoGorelli/no-string-hints
    rev: v0.1.6
    hooks:
    -   id: no-string-hints
```

## See also

Check out [pyupgrade](https://github.com/asottile/pyupgrade), which I learned a lot from when writing this.
