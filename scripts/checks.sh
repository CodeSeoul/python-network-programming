#!/bin/sh -e
set -x

ruff format .
black . --line-length=120
mypy --check-untyped-defs -p src