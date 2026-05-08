// CI/CD automation demo
#include "sensor_parser.h"

uint8_t compute_checksum(const uint8_t* buf, size_t len) {
    if (!buf) return 0;

    uint8_t checksum = 0;
    for (size_t i = 0; i < len; i++) {
        checksum ^= buf[i];
    }
    return checksum;
}

int validate_checksum(const uint8_t* buf, size_t len) {
    if (!buf || len == 0) return 0;

    uint8_t expected = compute_checksum(buf, len - 1);
    return expected == buf[len - 1];
}