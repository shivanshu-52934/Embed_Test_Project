#!/bin/bash

set -e

echo "Building Linux shared library..."

cd c_modules

gcc -shared -o libsensor.so -fPIC sensor_parser.c

cd ..

echo "Running pytest..."

pytest tests/manual/

echo "Tests completed successfully."