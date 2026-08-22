BASE_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

mkdir -p "$BASE_DIR/build"
g++ -Wall -O2 "$BASE_DIR/cpp/sha256sum.cpp" -o "$BASE_DIR/build/sha256sum"
