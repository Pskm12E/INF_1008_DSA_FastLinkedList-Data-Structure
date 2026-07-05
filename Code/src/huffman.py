"""
Huffman Coding Implementation
INF1008 Assignment 2
Team: [Your Team Name]
"""

import heapq
from collections import Counter
from typing import Dict, Optional, Tuple


class HuffmanNode:
    """Node in the Huffman tree"""
    
    def __init__(self, char: Optional[str], freq: int):
        self.char = char
        self.freq = freq
        self.left: Optional[HuffmanNode] = None
        self.right: Optional[HuffmanNode] = None
        
    def __lt__(self, other: 'HuffmanNode') -> bool:
        """For heap comparison"""
        return self.freq < other.freq
    
    def is_leaf(self) -> bool:
        """Check if node is a leaf (has a character)"""
        return self.char is not None


class HuffmanCoding:
    """Main Huffman encoding/decoding class"""
    
    def __init__(self):
        self.heap: list[HuffmanNode] = []
        self.codes: Dict[str, str] = {}
        self.reverse_mapping: Dict[str, str] = {}
        self.tree_root: Optional[HuffmanNode] = None
        self.steps: list[dict[str, object]] = []  # For visualization of tree building steps
        
    def build_frequency_dict(self, text: str) -> Dict[str, int]:
        """Count frequency of each character in text"""
        return dict(Counter(text))
    
    def build_heap(self, frequency: Dict[str, int]) -> None:
        """Create a min-heap from frequency dictionary"""
        for char, freq in frequency.items():
            node = HuffmanNode(char, freq)
            heapq.heappush(self.heap, node)
    
    def merge_nodes(self) -> None:
        """Build Huffman tree by repeatedly merging two smallest nodes"""
        while len(self.heap) > 1:
            # Pop two smallest nodes
            left = heapq.heappop(self.heap)
            right = heapq.heappop(self.heap)
            
            # Create internal node with combined frequency
            internal = HuffmanNode(None, left.freq + right.freq)
            internal.left = left
            internal.right = right
            
            # Push back to heap
            heapq.heappush(self.heap, internal)
            
            # Save step for visualization
            self.steps.append({
                'merged': (left.char if left.is_leaf() else '●', 
                          right.char if right.is_leaf() else '●'),
                'freq': left.freq + right.freq
            })
        
        # Root is the last node in heap
        self.tree_root = self.heap[0] if self.heap else None
    
    def generate_codes_helper(self, node: Optional[HuffmanNode], 
                             current_code: str) -> None:
        """Recursively traverse tree to generate codes"""
        if node is None:
            return
        
        if node.is_leaf():
            # Single-character inputs produce an empty traversal code, map as "0".
            code = current_code if current_code else "0"
            char = node.char
            if char is None:
                return
            self.codes[char] = code
            self.reverse_mapping[code] = char
            return
        
        self.generate_codes_helper(node.left, current_code + "0")
        self.generate_codes_helper(node.right, current_code + "1")
    
    def generate_codes(self) -> None:
        """Generate Huffman codes from the tree"""
        if self.tree_root:
            self.generate_codes_helper(self.tree_root, "")
    
    def encode_text(self, text: str) -> str:
        """Encode text using Huffman codes"""
        encoded = ""
        for char in text:
            encoded += self.codes[char]
        return encoded
    
    def decode_text(self, encoded_text: str) -> str:
        """Decode encoded text using Huffman tree"""
        if self.tree_root is None or not encoded_text:
            return ""

        # Special case for a tree with one unique character.
        if self.tree_root.is_leaf():
            char = self.tree_root.char
            return (char or "") * len(encoded_text)

        decoded = ""
        current = self.tree_root
        
        for bit in encoded_text:
            if bit == "0":
                if current is None:
                    return ""
                current = current.left
            else:
                if current is None:
                    return ""
                current = current.right
            
            if current is not None and current.is_leaf():
                char = current.char
                if char is None:
                    return ""
                decoded += char
                current = self.tree_root
        
        return decoded
    
    def compress(self, text: str) -> Tuple[str, Dict]:
        """Complete compression pipeline"""
        # Reset state for repeat calls on the same instance.
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}
        self.tree_root = None
        self.steps = []

        if not text:
            return "", {}
        
        # Build frequency dictionary
        freq = self.build_frequency_dict(text)
        
        # Build heap and tree
        self.build_heap(freq)
        self.merge_nodes()
        
        # Generate codes
        self.generate_codes()
        
        # Encode
        encoded = self.encode_text(text)
        
        return encoded, freq
    
    def get_compression_ratio(self, original: str, encoded: str) -> float:
        """Calculate compression ratio"""
        original_bits = len(original) * 8  # ASCII uses 8 bits per char
        compressed_bits = len(encoded)
        
        if original_bits == 0:
            return 0
        
        return (1 - compressed_bits / original_bits) * 100


# In VS Code, you can run this file to test
if __name__ == "__main__":
    # Simple test
    h = HuffmanCoding()
    test_text = "hello world"
    encoded, freq = h.compress(test_text)
    decoded = h.decode_text(encoded)
    
    print(f"Original: {test_text}")
    print(f"Encoded: {encoded}")
    print(f"Decoded: {decoded}")
    print(f"Compression ratio: {h.get_compression_ratio(test_text, encoded):.2f}%")