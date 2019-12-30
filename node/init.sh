#!bin/bash

set -e

wget ${CONFIG}
wget ${GENESIS}

exec "$@"