@echo off

SET GCC_PATH=C:\Users\shiva\Downloads\winlibs-x86_64-posix-seh-gcc-16.1.0-mingw-w64ucrt-14.0.0-r1\mingw64\bin\gcc.exe

cd c_modules

"%GCC_PATH%" -shared -o sensor.dll ^
    -fPIC ^
    sensor_parser.c

echo Build complete using correct GCC
pause