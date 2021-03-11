[![Build Status](https://github.com/MarcoGorelli/dequote-annotations/workflows/tox/badge.svg)](https://github.com/MarcoGorelli/dequote-annotations/actions?workflow=tox)
[![Coverage](https://codecov.io/gh/MarcoGorelli/dequote-annotations/branch/main/graph/badge.svg)](https://codecov.io/gh/MarcoGorelli/dequote-annotations)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/MarcoGorelli/dequote-annotations/main.svg)](https://results.pre-commit.ci/latest/github/MarcoGorelli/dequote-annotations/main)

dequote-annotations
================

A pre-commit hook to automatically remove string literals as type hints from argument, return, and class variable type annotations. Will only make the replacement if your file contains `from __future__ import annotations`.

## Installation

`pip install dequote-annotations`
## As a pre-commit hook

See [pre-commit](https://github.com/pre-commit/pre-commit) for instructions

Sample `.pre-commit-config.yaml`:

```yaml
-   repo: https://github.com/MarcoGorelli/dequote-annotations
    rev: v0.2.3
    hooks:
    -   id: dequote-annotations
```

## Command-line example

```console
$ cat myfile.py
myvar: 'str'
$ dequote-annotations myfile.py
$ cat myfile.py
myvar: str
```

## See also

Check out [pyupgrade](https://github.com/asottile/pyupgrade), which I learned a lot from when writing this.
