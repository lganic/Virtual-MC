#include "chunk_compression.h"
#include <pybind11/numpy.h>
#include <unordered_map>
#include <vector>
#include <string>
#include <stdexcept>
#include <iostream>
#include <iomanip>

//Include varint stuff from varint library. 
#include "../../varint/varint.cpp"

namespace py = pybind11;
constexpr int SIZE = 16;
constexpr int DIRECT_BPE_BLOCKS = 15;

static uint64_t fast_ceil_log_2(uint64_t value)
{
    if (value == 0)
        return 0;

    value = (value - 1) << 1; // Hacky floor -> ceil conversion

    uint64_t v_compare = 1 << 31;

    for (unsigned short k = 0; k < 31; k += 1)
    {

        if ((value & v_compare) != 0)
            return (31 - k);

        v_compare >>= 1;
    }

    return 0;
}

std::string varint_string(int value){
    std::vector<uint8_t> varint_bytes = write_var_int(value);
    std::string varint_str(reinterpret_cast<const char*>(varint_bytes.data()), varint_bytes.size());

    return varint_str;
}

py::bytes compress_chunk(pybind11::array_t<int, 16> input_array)
{
    // Parse input ndarray buffer
    auto buf = input_array.request();

    // Check sizing
    if (buf.ndim != 3 || buf.shape[0] != SIZE || buf.shape[1] != SIZE || buf.shape[2] != SIZE)
    {
        throw std::runtime_error("Input array must be a 16x16x16 integer array");
    }

    // Initialize the pallette map
    auto ptr = static_cast<int *>(buf.ptr);
    std::unordered_map<int, int> block_to_palette;
    int palette_index = 0;

    // Generate the lookup table and count unique elements
    for (int i = 0; i < buf.size; i++)
    {
        int block_id = ptr[i];
        if (block_to_palette.find(block_id) == block_to_palette.end())
        {
            block_to_palette[block_id] = palette_index++;
        }
    }

    uint64_t num_elements = block_to_palette.size();

    int bits_per_entry = fast_ceil_log_2(num_elements);

    // This is the single, dumbest, most moronic, stupid decision ever made by mojang.
    // There is no justifiable reason for the nonsense that is contained in these if statements.
    if (bits_per_entry > 0 && bits_per_entry < 4){
        bits_per_entry = 4; // WHY
    }

    if (bits_per_entry > 8){
        bits_per_entry = 15; // WHY
    }

    // Initialize the output string by creating an output string containing the bits per entry byte. 
    uint8_t bpe_byte = static_cast<uint8_t>(bits_per_entry);
    std::string output_string(1, static_cast<char>(bpe_byte));

    if (num_elements == 1){
        // Create entry for chunk with only one type of block in it. I.e. this is gonna be an overengineered function which is designed to compress only air lmao.

        auto ptr = static_cast<int*>(buf.ptr);
        int buffer_content = ptr[0];

        output_string.append(varint_string(buffer_content)); // Create, and add the pallette

        output_string.append(varint_string(0)); // Data array length (always zero in this case)

        return py::bytes(output_string);
        // No data array is required, since the value is inferred from the pallette
    }

    if (bits_per_entry < DIRECT_BPE_BLOCKS){
        // bit per entry is less than the direct flag, we need to encode the pallette. 

        // Build reverse palette: index -> block_id
        std::vector<int> reverse_palette(num_elements); // size = number of unique block types
        for (const auto& pair : block_to_palette) {
            reverse_palette[pair.second] = pair.first;
        }

        // Add number of elements
        output_string.append(varint_string(num_elements));

        // Append palette entries in correct order: palette[0], palette[1], ...
        for (int id : reverse_palette) {
            output_string.append(varint_string(id));
        }
        
    }

    else{
        // Convert pallette to a direct mapping, i.e. ignore pallette, but still use pallette code. 
        for (const auto& pair : block_to_palette) {
            output_string.append(varint_string(pair.first));
        }
    }

    // Assuming padding (i.e. Minecraft version >1.16)
    int entries_per_long = 64 / bits_per_entry;
    int num_longs = buf.size / entries_per_long;

    std::vector<uint64_t> compressed_data(num_longs, 0);
    int idx = 0;                // Index to track the position in the flattened array
    int long_index = num_longs; // Index to track the position in the output array (initialize to array end, for big endian)

    int bitshift_amount = 0;

    uint64_t working_long = 0;
    bool long_in_waiting = false;

    // Loop over all elements in the chunk
    for (uint64_t k = 0; k < buf.size; k++)
    {

        long_in_waiting = true;

        int block_id = *ptr;
        ++ptr;

        // Lookup block index in the pallette
        uint64_t palette_idx = block_to_palette[block_id];

        // Bitshift the index value to fit in the current long we are making.
        palette_idx <<= bitshift_amount;
        bitshift_amount += bits_per_entry;

        // Add the index value to the current long
        working_long += palette_idx;

        // Long is complete, add it to the output array.
        // Note that since we assume >1.16, we don't need to worry about overlapping longs. 
        if (bitshift_amount + bits_per_entry > 64)
        {
            compressed_data[--long_index] = working_long;

            long_in_waiting = false;
            bitshift_amount = 0;
            working_long = 0;
        }
    }

    // Pack the residual long that might not have been packed for certain BPE values. 
    if (long_in_waiting){
        compressed_data[--long_index] = working_long;
    }

    int data_array_length = compressed_data.size();

    output_string.append(varint_string(data_array_length));

    // // Cast to a raw byte array
    std::string compressed_bytes(reinterpret_cast<const char *>(compressed_data.data()),
        compressed_data.size() * sizeof(uint64_t));

    output_string.append(compressed_bytes);

    return py::bytes(output_string);
}
