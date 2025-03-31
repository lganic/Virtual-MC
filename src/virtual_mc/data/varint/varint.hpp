#pragma once
#include <vector>
#include <cstdint>

int32_t read_var_int(const std::vector<uint8_t>& data);
std::vector<uint8_t> write_var_int(int32_t value);