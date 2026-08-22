BASE_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="$BASE_DIR/.venv/bin/python"
PYBIND11_DIR="$("$PYTHON_BIN" -m pybind11 --cmakedir)"
INSTALL_PREFIX="$("$PYTHON_BIN" -c "import site; print(site.getsitepackages()[0])")"

cmake -S "$BASE_DIR" -B "$BASE_DIR/build" -Dpybind11_DIR="$PYBIND11_DIR" -DCMAKE_INSTALL_PREFIX="$INSTALL_PREFIX" -Wno-dev
