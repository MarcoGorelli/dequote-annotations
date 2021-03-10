[![Build Status](https://github.com/MarcoGorelli/no-string-hints/workflows/tox/badge.svg)](https://github.com/MarcoGorelli/no-string-hints/actions?workflow=tox)
[![Coverage](https://codecov.io/gh/MarcoGorelli/no-string-hints/branch/main/graph/badge.svg)](https://codecov.io/gh/MarcoGorelli/no-string-hints)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/MarcoGorelli/no-string-hints/main.svg)](https://results.pre-commit.ci/latest/github/MarcoGorelli/no-string-hints/main)

no-string-hints
================

A pre-commit hook to automatically remove string literals as type hints from argument, return, and class variable type annotations. Will only make the replacement if your file contains `from __future__ import annotations`.

## Installation

`pip install no-string-hints`
## As a pre-commit hook

See [pre-commit](https://github.com/pre-commit/pre-commit) for instructions

Sample `.pre-commit-config.yaml`:

```yaml
-   repo: https://github.com/MarcoGorelli/no-string-hints
    rev: v0.2.0
    hooks:
    -   id: no-string-hints
```

## Command-line example

```console
$ cat myfile.py
myvar: 'str'
$ no_string_hints myfile.py
$ cat myfile.py
myvar: str
```

## See also

Check out [pyupgrade](https://github.com/asottile/pyupgrade), which I learned a lot from when writing this.
