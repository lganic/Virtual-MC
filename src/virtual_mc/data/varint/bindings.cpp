#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/pytypes.h>

#include "varint.hpp"
#include "varlong.hpp"

namespace py = pybind11;

// Helper to convert py::bytes to vector<uint8_t>
std::vector<uint8_t> bytes_to_vec(const py::bytes& b) {
    std::string s = b;
    return std::vector<uint8_t>(s.begin(), s.end());
}

// Helper to convert vector<uint8_t> to py::bytes
py::bytes vec_to_bytes(const std::vector<uint8_t>& vec) {
    return py::bytes(reinterpret_cast<const char*>(vec.data()), vec.size());
}

PYBIND11_MODULE(varint, m) {
    m.def("read_var_int", &read_var_int);
    m.def("write_var_int", &write_var_int);
    m.def("read_var_long", &read_var_long);
    m.def("write_var_long", &write_var_long);

    // Overloads for py::bytes input/output
    m.def("read_var_int_bytes", [](py::bytes b) {
        return read_var_int(bytes_to_vec(b));
    });

    m.def("write_var_int_bytes", [](int32_t value) {
        return vec_to_bytes(write_var_int(value));
    });

    m.def("read_var_long_bytes", [](py::bytes b) {
        return read_var_long(bytes_to_vec(b));
    });

    m.def("write_var_long_bytes", [](int64_t value) {
        return vec_to_bytes(write_var_long(value));
    });
}
