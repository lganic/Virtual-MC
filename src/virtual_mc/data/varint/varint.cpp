#include "varint.hpp"
#include <stdexcept>

constexpr uint8_t SEGMENT_BITS = 0x7F;
constexpr uint8_t CONTINUE_BIT = 0x80;
constexpr uint32_t INT_SIGN_FLAG = 0x80000000;
constexpr uint64_t SIGNAL_FLAG = 0xFFFFFFFFFFFFFF80;

int32_t get_length_var_int(const std::vector<uint8_t>& data){

    int32_t count = 1;

    for (uint8_t byte : data) {
        if ((byte & CONTINUE_BIT) == 0) break;
        count += 1;
    }

    return count;
}

int32_t read_var_int(const std::vector<uint8_t>& data) {
    uint32_t value = 0;
    int shift = 0;

    for (uint8_t byte : data) {
        value |= (byte & SEGMENT_BITS) << shift;
        if ((byte & CONTINUE_BIT) == 0) break;
        shift += 7;
        if (shift >= 32) throw std::overflow_error("VarInt too big!");
    }

    if (value & INT_SIGN_FLAG) value = INT_SIGN_FLAG - value;
    return static_cast<int32_t>(value);
}

std::vector<uint8_t> write_var_int(int32_t value) {
    std::vector<uint8_t> out;
    uint32_t abs_val = static_cast<uint32_t>(std::abs(value));

    if (value < 0) abs_val |= INT_SIGN_FLAG;

    while (true) {
        if ((abs_val & SIGNAL_FLAG) == 0) {
            out.push_back(abs_val);
            return out;
        }

        out.push_back((abs_val & SEGMENT_BITS) | CONTINUE_BIT);
        abs_val >>= 7;

        if (out.size() > 5) throw std::overflow_error("VarInt too big!");
    }
}
