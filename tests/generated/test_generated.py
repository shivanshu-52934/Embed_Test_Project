
import pytest
import ctypes
import os
from pathlib import Path

# Load the shared library
LIB_PATH = os.path.abspath("c_modules/libsensor.so")
lib = ctypes.CDLL(LIB_PATH)

# Define function signatures
compute_checksum = lib.compute_checksum
compute_checksum.argtypes = [ctypes.POINTER(ctypes.c_uint8), ctypes.c_size_t]
compute_checksum.restype = ctypes.c_uint8

validate_checksum = lib.validate_checksum
validate_checksum.argtypes = [ctypes.POINTER(ctypes.c_uint8), ctypes.c_size_t]
validate_checksum.restype = ctypes.c_int


class TestComputeChecksum:
    """Test cases for compute_checksum function"""
    
    def test_empty_buffer(self):
        """Test with empty buffer"""
        buf = (ctypes.c_uint8 * 0)()
        result = compute_checksum(buf, 0)
        assert isinstance(result, int)
        assert 0 <= result <= 255
    
    def test_single_byte(self):
        """Test with single byte buffer"""
        buf = (ctypes.c_uint8 * 1)(42)
        result = compute_checksum(buf, 1)
        assert isinstance(result, int)
        assert result == 42
    
    def test_two_bytes(self):
        """Test with two bytes"""
        buf = (ctypes.c_uint8 * 2)(100, 50)
        result = compute_checksum(buf, 2)
        assert isinstance(result, int)
        assert result == (100 ^ 50)
    
    def test_all_zeros(self):
        """Test with buffer of all zeros"""
        buf = (ctypes.c_uint8 * 5)(0, 0, 0, 0, 0)
        result = compute_checksum(buf, 5)
        assert result == 0
    
    def test_all_ones(self):
        """Test with buffer of all ones"""
        buf = (ctypes.c_uint8 * 5)(1, 1, 1, 1, 1)
        result = compute_checksum(buf, 5)
        assert result == 1
    
    def test_all_max_value(self):
        """Test with buffer of max uint8 values"""
        buf = (ctypes.c_uint8 * 3)(255, 255, 255)
        result = compute_checksum(buf, 3)
        assert isinstance(result, int)
        assert 0 <= result <= 255
    
    def test_mixed_values(self):
        """Test with mixed values"""
        buf = (ctypes.c_uint8 * 4)(10, 20, 30, 40)
        result = compute_checksum(buf, 4)
        expected = 10 ^ 20 ^ 30 ^ 40
        assert result == expected
    
    def test_large_buffer(self):
        """Test with larger buffer"""
        data = list(range(0, 256))
        buf = (ctypes.c_uint8 * len(data))(*data)
        result = compute_checksum(buf, len(data))
        assert isinstance(result, int)
        assert 0 <= result <= 255
    
    def test_partial_length(self):
        """Test when length is less than buffer size"""
        buf = (ctypes.c_uint8 * 5)(10, 20, 30, 40, 50)
        result = compute_checksum(buf, 3)
        expected = 10 ^ 20 ^ 30
        assert result == expected
    
    def test_checksum_overflow(self):
        """Test checksum calculation with overflow"""
        buf = (ctypes.c_uint8 * 2)(200, 100)
        result = compute_checksum(buf, 2)
        expected = 200 ^ 100
        assert result == expected
    
    def test_return_type_is_uint8(self):
        """Test that return value is within uint8 range"""
        buf = (ctypes.c_uint8 * 3)(255, 255, 255)
        result = compute_checksum(buf, 3)
        assert 0 <= result <= 255


class TestValidateChecksum:
    """Test cases for validate_checksum function"""
    
    def test_empty_buffer(self):
        """Test validation with empty buffer"""
        buf = (ctypes.c_uint8 * 0)()
        result = validate_checksum(buf, 0)
        assert isinstance(result, int)
