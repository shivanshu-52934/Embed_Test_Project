#!/bin/bash

echo "Cleaning old coverage files..."

rm -f c_modules/*.gcda
rm -f c_modules/*.gcno
rm -f c_modules/*.gcov
rm -f c_modules/*.o

echo "Building with coverage instrumentation..."

gcc -fprofile-arcs -ftest-coverage \
    -fPIC -c c_modules/sensor_parser.c \
    -o c_modules/sensor_parser.o

gcc -shared -fprofile-arcs -ftest-coverage \
    c_modules/sensor_parser.o \
    -o c_modules/libsensor.so

echo "Running GENERATED tests..."

pytest tests/generated/

echo "Capturing coverage with lcov..."

mkdir -p coverage_reports

lcov --capture \
     --directory c_modules \
     --output-file coverage_reports/coverage.info

echo "Generating HTML report..."

genhtml coverage_reports/coverage.info \
        --output-directory coverage_reports/html

echo "HTML coverage report generated."

echo "Open:"
echo "coverage_reports/html/index.html"