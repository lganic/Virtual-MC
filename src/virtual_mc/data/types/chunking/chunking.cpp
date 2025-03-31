#include <pybind11/pybind11.h>
#include "chunk_compression.h"

PYBIND11_MODULE(chunking, m) {
    m.def("compress_chunk", &compress_chunk, "Encodes a chunk into a bytes object based on unique elements");
}