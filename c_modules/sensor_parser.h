#ifndef SENSOR_PARSER_H
#define SENSOR_PARSER_H

#include <stdint.h>
#include <stddef.h>

uint8_t compute_checksum(const uint8_t* buf, size_t len);
int validate_checksum(const uint8_t* buf, size_t len);

#endif