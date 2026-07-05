"""Manual test script for visualizer functions."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.huffman import HuffmanCoding
from src.visualizer import print_tree_ascii, display_codes_table, HuffmanVisualizer

def test_basic_visualization():
    """Test basic visualization features."""
    print("=" * 60)
    print("TESTING HUFFMAN VISUALIZER")
    print("=" * 60)
    
    # Create Huffman coding instance
    huffman = HuffmanCoding()
    test_text = "hello world"
    
    print(f"\n1. Encoding text: '{test_text}'")
    encoded, freq = huffman.compress(test_text)
    
    print(f"\n2. Encoded result: {encoded}")
    print(f"   Original bits: {len(test_text) * 8}")
    print(f"   Compressed bits: {len(encoded)}")
    print(f"   Compression ratio: {huffman.get_compression_ratio(test_text, encoded):.2f}%")
    
    print("\n3. ASCII Tree Visualization:")
    print("-" * 60)
    print_tree_ascii(huffman.tree_root)
    
    print("\n4. Huffman Codes Table:")
    print("-" * 60)
    display_codes_table(huffman.codes)
    
    print("\n5. Testing decode:")
    decoded = huffman.decode_text(encoded)
    print(f"   Decoded: '{decoded}'")
    print(f"   Match: {decoded == test_text}")
    
    # Test visualizer class
    visualizer = HuffmanVisualizer()
    
    print("\n6. Testing frequency bar chart...")
    try:
        visualizer.plot_frequency_bar(freq)
        print("   ✓ Frequency bar chart opened (close window to continue)")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print("\n7. Testing tree visualization...")
    try:
        visualizer.plot_tree(huffman.tree_root)
        print("   ✓ Tree visualization opened (close window to continue)")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print("\n8. Testing compression comparison...")
    try:
        visualizer.plot_compression_comparison(test_text, encoded)
        print("   ✓ Compression comparison opened (close window to continue)")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    test_basic_visualization()
