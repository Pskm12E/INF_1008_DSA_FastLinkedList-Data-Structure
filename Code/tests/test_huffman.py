"""
Unit tests for Huffman coding implementation
Run with: pytest tests/ -v
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.huffman import HuffmanCoding, HuffmanNode
import pytest
"""
Unit tests for Huffman coding implementation
Run with: pytest tests/ -v
"""

import pytest

from src.huffman import HuffmanCoding


class TestHuffmanCoding:

    def setup_method(self):
        """Setup before each test"""
        self.h = HuffmanCoding()

    def test_frequency_counter(self):
        """Test frequency counting"""
        text = "hello"
        freq = self.h.build_frequency_dict(text)

        assert freq["h"] == 1
        assert freq["e"] == 1
        assert freq["l"] == 2
        assert freq["o"] == 1
        assert len(freq) == 4

    def test_empty_string(self):
        """Test empty string handling"""
        text = ""
        encoded, freq = self.h.compress(text)

        assert encoded == ""
        assert freq == {}

    def test_single_character(self):
        """Test single character repeated"""
        text = "aaaaa"
        encoded, _ = self.h.compress(text)
        decoded = self.h.decode_text(encoded)

        assert decoded == text
        assert len(self.h.codes) == 1

    def test_two_characters(self):
        """Test with two characters"""
        text = "ab"
        encoded, _ = self.h.compress(text)
        decoded = self.h.decode_text(encoded)

        assert decoded == text
        assert len(self.h.codes) == 2
        assert set(self.h.codes.values()) == {"0", "1"}

    def test_round_trip(self):
        """Test encoding and decoding"""
        test_strings = [
            "hello world",
            "The quick brown fox jumps over the lazy dog",
            "ABC123!@#",
            "a" * 100,
            "multi byte chars",
        ]

        for text in test_strings:
            self.setup_method()
            encoded, _ = self.h.compress(text)
            decoded = self.h.decode_text(encoded)
            assert decoded == text, f"Failed for: {text}"

    def test_prefix_property(self):
        """Verify prefix property (no code is prefix of another)"""
        text = "this is a test"
        self.h.compress(text)

        codes = list(self.h.codes.values())

        for i, left_code in enumerate(codes):
            for j, right_code in enumerate(codes):
                if i != j:
                    assert not right_code.startswith(left_code), (
                        f"Prefix property violated: {left_code} is prefix of {right_code}"
                    )

    def test_compression_ratio(self):
        """Test compression ratio calculation"""
        text = "aaaaa"
        encoded, _ = self.h.compress(text)
        ratio = self.h.get_compression_ratio(text, encoded)

        assert ratio > 50

        text2 = "abcdefghijklmnopqrstuvwxyz"
        encoded2, _ = self.h.compress(text2)
        ratio2 = self.h.get_compression_ratio(text2, encoded2)

        assert 0 < ratio2 < 50