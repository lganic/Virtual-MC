#include "varlong.hpp"
#include <stdexcept>
#include <cmath>

constexpr uint8_t SEGMENT_BITS = 0x7F;
constexpr uint8_t CONTINUE_BIT = 0x80;
constexpr uint64_t LONG_SIGN_FLAG = 0x8000000000000000;
constexpr uint64_t SIGNAL_FLAG = 0xFFFFFFFFFFFFFF80;

int64_t read_var_long(const std::vector<uint8_t>& data) {
    uint64_t value = 0;
    int shift = 0;

    for (uint8_t byte : data) {
        value |= (uint64_t)(byte & SEGMENT_BITS) << shift;
        if ((byte & CONTINUE_BIT) == 0) break;
        shift += 7;
        if (shift >= 64) throw std::runtime_error("VarLong too big!");
    }

    if (value & LONG_SIGN_FLAG) value = LONG_SIGN_FLAG - value;
    return static_cast<int64_t>(value);
}

std::vector<uint8_t> write_var_long(int64_t value) {
    std::vector<uint8_t> out;
    uint64_t abs_val = static_cast<uint64_t>(std::abs(value));

    if (value < 0) abs_val |= LONG_SIGN_FLAG;

    while (true) {
        if ((abs_val & SIGNAL_FLAG) == 0) {
            out.push_back(abs_val);
            return out;
        }

        out.push_back((abs_val & SEGMENT_BITS) | CONTINUE_BIT);
        abs_val >>= 7;

        if (out.size() > 10) throw std::runtime_error("VarLong too big!");
    }
}
