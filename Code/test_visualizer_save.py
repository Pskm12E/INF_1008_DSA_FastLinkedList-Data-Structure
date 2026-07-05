"""Non-interactive test script for visualizer - saves images instead of showing."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.huffman import HuffmanCoding
from src.visualizer import print_tree_ascii, display_codes_table, visualize_tree
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt

def test_visualization_save():
    """Test visualization features by saving to files."""
    print("=" * 60)
    print("TESTING HUFFMAN VISUALIZER (Non-Interactive)")
    print("=" * 60)
    
    # Create Huffman coding instance
    huffman = HuffmanCoding()
    test_text = "hello world! this is a test of huffman coding algorithm"
    
    print(f"\n1. Encoding text: '{test_text}'")
    encoded, freq = huffman.compress(test_text)
    
    print(f"\n2. Encoded result length: {len(encoded)} bits")
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
    
    # Create output directory if needed
    os.makedirs("data", exist_ok=True)
    
    print("\n6. Saving frequency bar chart...")
    try:
        items = sorted(freq.items(), key=lambda item: item[1], reverse=True)
        labels = [ch if ch not in [" ", "\n", "\t"] else repr(ch) for ch, _ in items]
        values = [count for _, count in items]
        
        plt.figure(figsize=(12, 6))
        plt.bar(labels, values, color='steelblue')
        plt.title("Character Frequency Distribution", fontsize=14, fontweight='bold')
        plt.xlabel("Character")
        plt.ylabel("Frequency")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig("data/frequency_chart.png", dpi=150, bbox_inches="tight")
        plt.close()
        print("   ✓ Saved to data/frequency_chart.png")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print("\n7. Saving tree visualization...")
    try:
        visualize_tree(huffman.tree_root, save_path="data/huffman_tree.png")
        print("   ✓ Saved to data/huffman_tree.png")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print("\n8. Saving compression comparison...")
    try:
        original_bits = len(test_text) * 8
        compressed_bits = len(encoded)
        
        plt.figure(figsize=(8, 5))
        bars = plt.bar(
            ["Original (8-bit ASCII)", "Huffman Compressed"],
            [original_bits, compressed_bits],
            color=["#e74c3c", "#27ae60"],
            width=0.6
        )
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)} bits',
                    ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        plt.title("Compression Comparison", fontsize=14, fontweight='bold')
        plt.ylabel("Size (bits)")
        
        saved_percentage = huffman.get_compression_ratio(test_text, encoded)
        plt.text(0.5, 0.95, f"Space Saved: {saved_percentage:.1f}%",
                transform=plt.gca().transAxes,
                ha='center', va='top', fontsize=12,
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        plt.savefig("data/compression_comparison.png", dpi=150, bbox_inches="tight")
        plt.close()
        print("   ✓ Saved to data/compression_comparison.png")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ ALL VISUALIZATION TESTS COMPLETED!")
    print("=" * 60)
    print("\nGenerated files:")
    print("  - data/frequency_chart.png")
    print("  - data/huffman_tree.png")
    print("  - data/compression_comparison.png")

if __name__ == "__main__":
    test_visualization_save()
