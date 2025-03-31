#pragma once
#include <vector>
#include <cstdint>

int64_t read_var_long(const std::vector<uint8_t>& data);
std::vector<uint8_t> write_var_long(int64_t value);
