from setuptools import setup, Extension
import pybind11
import glob

# Glob all the cpp files inside the chunking directory
ext_modules = [
    Extension(
        "virtual_mc.data.types.chunking",  # Full module path
        sources=glob.glob("src/virtual_mc/data/types/chunking/*.cpp"),
        include_dirs=[pybind11.get_include(), "src"],  # Include src in include_dirs
        extra_compile_args=["-O3"],  # Optimize for speed
        language="c++",
    ),

    Extension(
        "virtual_mc.data.varint",
        sources=glob.glob("src/virtual_mc/data/varint/*.cpp"),
        include_dirs=[pybind11.get_include(), "src"],
        extra_compile_args=["-O3"],
        language="c++",
    )
]

setup(
    ext_modules=ext_modules,
    packages=["virtual_mc"],  # Use the correct top-level package
)
