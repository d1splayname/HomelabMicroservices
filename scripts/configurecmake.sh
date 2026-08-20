cmake -S . -B build \
    -Dpybind11_DIR=$(python3 -m pybind11 --cmakedir) \
    -DCMAKE_INSTALL_PREFIX=$(python3 -c "import site; print(site.getsitepackages()[0])")
