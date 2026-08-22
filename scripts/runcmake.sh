BASE_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

mkdir -p "$BASE_DIR/build/"
cmake --build "$BASE_DIR/build"
cmake --install "$BASE_DIR/build"
