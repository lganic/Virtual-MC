#ifndef CHUNK_COMPRESSION_H
#define CHUNK_COMPRESSION_H

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>


pybind11::bytes compress_chunk(pybind11::array_t<int> block_ids, pybind11::array_t<int> biome_ids);

#endif // CHUNK_COMPRESSION_H
