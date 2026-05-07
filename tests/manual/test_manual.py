import ctypes
import os

LIB_PATH = os.path.abspath("c_modules/libsensor.so")
lib = ctypes.CDLL(LIB_PATH)

compute_checksum = lib.compute_checksum
compute_checksum.argtypes = [ctypes.POINTER(ctypes.c_uint8), ctypes.c_size_t]
compute_checksum.restype = ctypes.c_uint8

validate_checksum = lib.validate_checksum
validate_checksum.argtypes = [ctypes.POINTER(ctypes.c_uint8), ctypes.c_size_t]
validate_checksum.restype = ctypes.c_int


def test_checksum_basic():
    data = (ctypes.c_uint8 * 3)(1, 2, 3)
    result = compute_checksum(data, 3)
    assert result == (1 ^ 2 ^ 3)


def test_validate_checksum_valid():
    checksum = 1 ^ 2 ^ 3
    data = (ctypes.c_uint8 * 4)(1, 2, 3, checksum)
    result = validate_checksum(data, 4)
    assert result == 1


def test_validate_checksum_invalid():
    data = (ctypes.c_uint8 * 4)(1, 2, 3, 99)
    result = validate_checksum(data, 4)
    assert result == 0