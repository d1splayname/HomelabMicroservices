#include <string>
#include <bitset>
#include <cmath>
#include <cstdint>
#include <array>
#include <iomanip>
#include <sstream>

#include <iostream>

uint32_t rrot (uint32_t x, unsigned int n) {
    return (x >> n) | (x << (32 - n));
}

std::string sha256sum(std::string input) {
    // convert input string to binary
    std::string binaryString = "";

    for (char c : input) {
        binaryString += std::bitset<8>(c).to_string();
    }

    const int BIN_STR_LEN = binaryString.length();

    // append a 1
    binaryString += '1';

    // pad with 0's until length = 512*c - 64 for some constant c
    int zeroCount = (447 - (BIN_STR_LEN % 512) + 512) % 512;
    binaryString.append(zeroCount, '0');

    std::bitset<64> lengthBinary(BIN_STR_LEN);
    binaryString += lengthBinary.to_string();

    // starting hash values
    std::array<std::uint32_t, 8> startingHash = {
        0x6a09e667,
        0xbb67ae85,
        0x3c6ef372,
        0xa54ff53a,
        0x510e527f,
        0x9b05688c,
        0x1f83d9ab,
        0x5be0cd19
    };

    const std::array<std::uint32_t, 64> K = {
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
    };
    
    std::array<std::uint32_t, 64> w{};

    for(int i = 0; i < binaryString.length(); i += 512) { // extract 512 bit chunks
        std::string bStringSubset = binaryString.substr(i, 512);

        for (int j = 0; j < 16; j++)
        {
            std::string wordString = bStringSubset.substr(j * 32, 32);
            std::uint32_t word = static_cast<std::uint32_t>(std::stoul(wordString, nullptr, 2));

            w[j] = word;
        }

        // modify rest of w
        for (int i = 16; i < 64; i++) {
            const uint32_t S0 = rrot(w[i - 15], 7) ^ rrot(w[i - 15], 18) ^ (w[i - 15] >> 3);
            const uint32_t S1 = rrot(w[i - 2], 17) ^ rrot(w[i - 2], 19) ^ (w[i - 2] >> 10);
            w[i] = w[i-16] + S0 + w[i-7] + S1;
        }

        // compression
        uint32_t a = startingHash[0];
        uint32_t b = startingHash[1];
        uint32_t c = startingHash[2];
        uint32_t d = startingHash[3];
        uint32_t e = startingHash[4];
        uint32_t f = startingHash[5];
        uint32_t g = startingHash[6];
        uint32_t h = startingHash[7];

        for (int i = 0; i < 64; i++ ) {
            const uint32_t S1 = rrot(e, 6) ^ rrot(e, 11) ^ rrot(e, 25);
            const uint32_t CH = (e & f) ^ ((~ e) & g);
            const uint32_t TEMP1 = h + S1 + CH + K[i] + w[i];
            const uint32_t S0 = rrot(a, 2) ^ rrot(a, 13) ^ rrot(a, 22);
            const uint32_t MAJ = (a & b) ^ (a & c) ^ (b & c);
            const uint32_t TEMP2 = S0 + MAJ;
            
            h = g;
            g = f;
            f = e;
            e = d + TEMP1;
            d = c;
            c = b;
            b = a;
            a = TEMP1 + TEMP2;
        }

        // put back into starting hashes
        startingHash[0] += a;
        startingHash[1] += b;
        startingHash[2] += c;
        startingHash[3] += d;
        startingHash[4] += e;
        startingHash[5] += f;
        startingHash[6] += g;
        startingHash[7] += h;
    }

    std::ostringstream oss;

    for (uint32_t hash : startingHash) {
        oss << std::hex
            << std::setw(8)
            << std::setfill('0')
            << hash;
    }

    const std::string finalHash = oss.str();

    return finalHash;
}

int main() {
    std::string text = "sha256sum";
    std::cout << "input:" << text << std::endl;

    std::string sha256hash = sha256sum(text);
    std::cout << "final: " << sha256hash << std::endl;
}