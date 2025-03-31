#include "chunk_compression.h"
#include <pybind11/numpy.h>
#include <unordered_map>
#include <vector>
#include <stdexcept>
#include <iostream>
#include <iomanip>

namespace py = pybind11;
constexpr int SIZE = 16;

static unsigned int fast_ceil_log_2(unsigned int value)
{
    if (value == 0)
        return 0;

    value = (value - 1) << 1; // Hacky floor -> ceil conversion

    unsigned int v_compare = 1 << 31;

    for (unsigned short k = 0; k < 31; k += 1)
    {

        if ((value & v_compare) != 0)
            return (31 - k);

        v_compare >>= 1;
    }

    return 0;
}

py::bytes compress_chunk(pybind11::array_t<int, 16> input_array)
{
    auto buf = input_array.request();

    if (buf.ndim != 3 || buf.shape[0] != SIZE || buf.shape[1] != SIZE || buf.shape[2] != SIZE)
    {
        throw std::runtime_error("Input array must be a 16x16x16 integer array");
    }

    auto ptr = static_cast<int *>(buf.ptr);
    std::unordered_map<int, int> block_to_palette;
    int palette_index = 0;

    // Generate the lookup table and count unique elements
    for (int i = 0; i < buf.size; ++i)
    {
        int block_id = ptr[i];
        if (block_to_palette.find(block_id) == block_to_palette.end())
        {
            block_to_palette[block_id] = palette_index++;
        }
    }

    size_t num_elements = block_to_palette.size();

    // std::cout << "Number of elements: " << num_elements << std::endl;

    int bits_per_entry = fast_ceil_log_2(num_elements);

    // std::cout << "Bits per entry: " << bits_per_entry << std::endl;

    // Assuming padding (i.e. Minecraft version >1.16)
    int entries_per_long = 64 / bits_per_entry;
    int num_longs = buf.size / entries_per_long;

    // std::cout << "Entries per long: " << entries_per_long << std::endl;

    std::vector<uint64_t> compressed_data(num_longs, 0);
    int idx = 0;                // Index to track the position in the flattened array
    int long_index = num_longs; // Index to track the position in the output array (initialize to array end, for big endian)

    int bitshift_amount = 0;

    uint64_t working_long = 0;
    bool long_in_waiting = false;

    for (unsigned int k = 0; k < buf.size; k++)
    {

        long_in_waiting = true;

        int block_id = *ptr;
        ++ptr;

        uint64_t palette_idx = block_to_palette[block_id];
        palette_idx <<= bitshift_amount;
        bitshift_amount += bits_per_entry;
        working_long += palette_idx;

        if (bitshift_amount + bits_per_entry > 64)
        {
            compressed_data[--long_index] = working_long;
            // compressed_data[long_index] = 2863311530;

            long_in_waiting = false;
            bitshift_amount = 0;
            working_long = 0;
        }
    }

    for (unsigned int k = 0; k < num_longs; k++)
    {
        std::cout << compressed_data[k] << std::endl;
    }

    // // Cast to a raw byte array
    return py::bytes(reinterpret_cast<const char *>(compressed_data.data()), compressed_data.size() * sizeof(uint64_t));
}
