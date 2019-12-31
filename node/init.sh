#!/bin/bash

set -e

python3 $ENV_PREFIX/bin/make_config.py

exec "$@"