"""
Main application for Huffman Coding Visualizer
INF1008 Assignment 2
"""

import os
import sys
from typing import Optional

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.huffman import HuffmanCoding, HuffmanNode
from src.visualizer import HuffmanVisualizer
from src.file_handler import FileHandler


class HuffmanApp:
    """Main application class with interactive menu"""
    
    def __init__(self):
        self.huffman = HuffmanCoding()
        self.visualizer = HuffmanVisualizer()
        self.file_handler = FileHandler()
        self.current_text = ""
        self.current_encoded = ""
        self.current_freq = {}
        
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Print application header"""
        print("=" * 60)
        print("    HUFFMAN CODING VISUALIZER - INF1008 Assignment 2")
        print("=" * 60)
        print()
    
    def print_menu(self):
        """Print main menu"""
        print("\n📋 MAIN MENU")
        print("-" * 40)
        print("1. 📝 Enter text manually")
        print("2. 📂 Load text from file")
        print("3. 🔍 Show character frequencies")
        print("4. 🌳 Visualize Huffman tree")
        print("5. 📊 Show compression results")
        print("6. 💾 Save compressed data")
        print("7. 📁 Load compressed data")
        print("8. 🎨 Show all visualizations")
        print("9. ❌ Exit")
        print("-" * 40)
    
    def run(self):
        """Main application loop"""
        while True:
            self.clear_screen()
            self.print_header()
            
            # Show current text status
            if self.current_text:
                print(f"📄 Current text: '{self.current_text[:50]}'")
                if len(self.current_text) > 50:
                    print("... (truncated)")
                print(f"📏 Length: {len(self.current_text)} characters")
                if self.current_encoded:
                    ratio = self.huffman.get_compression_ratio(
                        self.current_text, self.current_encoded
                    )
                    print(f"💾 Compression: {ratio:.1f}% saved")
            else:
                print("📄 No text loaded")
            
            self.print_menu()
            
            choice = input("\n🔹 Enter your choice (1-9): ")
            
            if choice == '1':
                self.enter_text_manual()
            elif choice == '2':
                self.load_from_file()
            elif choice == '3':
                self.show_frequencies()
            elif choice == '4':
                self.visualize_tree()
            elif choice == '5':
                self.show_compression()
            elif choice == '6':
                self.save_compressed()
            elif choice == '7':
                self.load_compressed()
            elif choice == '8':
                self.show_all_visualizations()
            elif choice == '9':
                print("\n👋 Goodbye!")
                break
            else:
                print("\n❌ Invalid choice. Press Enter to continue...")
                input()
    
    def enter_text_manual(self):
        """Option 1: Enter text manually"""
        self.clear_screen()
        self.print_header()
        print("📝 Enter your text below:")
        print("-" * 40)
        
        text = input()
        
        if text:
            self.current_text = text
            self.current_encoded, self.current_freq = self.huffman.compress(text)
            print(f"\n✅ Text loaded! {len(text)} characters")
            print(f"✅ Compressed to {len(self.current_encoded)} bits")
        else:
            print("\n❌ No text entered")
        
        print("\nPress Enter to continue...")
        input()
    
    def load_from_file(self):
        """Option 2: Load text from file"""
        self.clear_screen()
        self.print_header()
        
        # Show available text files
        files = self.file_handler.list_text_files()
        
        if files:
            print("📂 Available text files:")
            for i, f in enumerate(files, 1):
                size = self.file_handler.get_file_size(f)
                print(f"   {i}. {f} ({size} bytes)")
            
            print("\nEnter filename (or path): ", end='')
            filename = input()
            
            text = self.file_handler.read_text_file(filename)
            if text:
                self.current_text = text
                self.current_encoded, self.current_freq = self.huffman.compress(text)
                print(f"\n✅ Loaded {len(text)} characters from {filename}")
                print(f"✅ Compressed to {len(self.current_encoded)} bits")
            else:
                print(f"\n❌ Could not read {filename}")
        else:
            print("📂 No .txt files found in current directory")
            print("   Please create a text file or use manual entry")
        
        print("\nPress Enter to continue...")
        input()
    
    def show_frequencies(self):
        """Option 3: Show character frequencies"""
        if not self.current_text:
            print("\n❌ No text loaded. Please enter text first.")
            print("\nPress Enter to continue...")
            input()
            return
        
        self.clear_screen()
        self.print_header()
        
        print("📊 Character Frequencies:")
        print("-" * 40)
        
        # Sort by frequency
        sorted_freq = sorted(self.current_freq.items(), 
                           key=lambda x: x[1], reverse=True)
        
        for char, freq in sorted_freq:
            if char == ' ':
                display = "' ' (space)"
            elif char == '\n':
                display = "'\\n' (newline)"
            elif char == '\t':
                display = "'\\t' (tab)"
            else:
                display = f"'{char}'"
            
            # Show visual bar
            bar = "█" * min(freq, 20)
            print(f"{display:15} : {freq:3} {bar}")
        
        # Show in matplotlib
        print("\n📈 Opening frequency chart...")
        self.visualizer.plot_frequency_bar(self.current_freq)
        
        print("\nPress Enter to continue...")
        input()
    
    def visualize_tree(self):
        """Option 4: Visualize Huffman tree"""
        if not self.current_text:
            print("\n❌ No text loaded. Please enter text first.")
            print("\nPress Enter to continue...")
            input()
            return
        
        self.clear_screen()
        self.print_header()
        
        print("🌳 Generating Huffman tree visualization...")
        print("\n📌 Legend:")
        print("   - Green nodes: Characters (leaf nodes)")
        print("   - Blue nodes: Internal nodes")
        print("   - Edges labeled: 0 (left) and 1 (right)")
        
        # Show tree
        self.visualizer.plot_tree(self.huffman.tree_root)
        
        print("\n✅ Tree visualization complete!")
        print("\nPress Enter to continue...")
        input()
    
    def show_compression(self):
        """Option 5: Show compression results"""
        if not self.current_text or not self.current_encoded:
            print("\n❌ No compressed data available.")
            print("\nPress Enter to continue...")
            input()
            return
        
        self.clear_screen()
        self.print_header()
        
        original_size = len(self.current_text) * 8
        compressed_size = len(self.current_encoded)
        ratio = self.huffman.get_compression_ratio(
            self.current_text, self.current_encoded
        )
        
        print("📊 COMPRESSION RESULTS")
        print("=" * 40)
        print(f"Original text:    '{self.current_text[:50]}'")
        if len(self.current_text) > 50:
            print("                    ...")
        print(f"Original length:   {len(self.current_text)} characters")
        print(f"Original size:     {original_size} bits")
        print(f"Compressed size:   {compressed_size} bits")
        print(f"Space saved:       {original_size - compressed_size} bits")
        print(f"Compression ratio: {ratio:.2f}%")
        print("=" * 40)
        
        # Show Huffman codes
        print("\n🔤 Huffman Codes:")
        print("-" * 40)
        for char, code in sorted(self.huffman.codes.items()):
            if char == ' ':
                display = 'space'
            else:
                display = char
            print(f"  '{display}': {code}")
        
        # Show visualization
        print("\n📈 Opening compression comparison...")
        self.visualizer.plot_compression_comparison(
            self.current_text, self.current_encoded
        )
        
        print("\nPress Enter to continue...")
        input()
    
    def save_compressed(self):
        """Option 6: Save compressed data"""
        if not self.current_text:
            print("\n❌ No text to save.")
            print("\nPress Enter to continue...")
            input()
            return
        
        self.clear_screen()
        self.print_header()
        
        print("💾 Save compressed data")
        print("-" * 40)
        filename = input("Enter filename (e.g., output.huff): ")
        
        success = self.file_handler.save_compressed(
            filename, 
            self.current_encoded,
            self.huffman.codes,
            self.current_text
        )
        
        if success:
            print(f"\n✅ Data saved to {filename}")
        else:
            print(f"\n❌ Failed to save to {filename}")
        
        print("\nPress Enter to continue...")
        input()
    
    def load_compressed(self):
        """Option 7: Load compressed data"""
        self.clear_screen()
        self.print_header()
        
        print("📁 Load compressed data")
        print("-" * 40)
        filename = input("Enter filename (e.g., output.huff): ")
        
        data = self.file_handler.load_compressed(filename)
        
        if data:
            self.current_encoded = data['encoded']
            self.huffman.codes = data['codes']
            self.current_text = data['original']
            
            # Rebuild reverse mapping
            self.huffman.reverse_mapping = {
                v: k for k, v in self.huffman.codes.items()
            }
            
            # Rebuild tree from codes (simplified)
            self.huffman.tree_root = HuffmanNode(None, 0)
            # (Tree reconstruction logic would go here)
            
            print(f"\n✅ Loaded data from {filename}")
            print(f"📄 Text: '{self.current_text[:50]}'")
            if len(self.current_text) > 50:
                print("   ...")
            print(f"📏 Length: {len(self.current_text)} characters")
        else:
            print(f"\n❌ Failed to load from {filename}")
        
        print("\nPress Enter to continue...")
        input()
    
    def show_all_visualizations(self):
        """Option 8: Show all visualizations at once"""
        if not self.current_text:
            print("\n❌ No text loaded. Please enter text first.")
            print("\nPress Enter to continue...")
            input()
            return
        
        self.clear_screen()
        self.print_header()
        
        print("🎨 Generating all visualizations...")
        print("\n1. Frequency bar chart")
        print("2. Huffman tree")
        print("3. Compression comparison")
        
        # Show all
        self.visualizer.plot_frequency_bar(self.current_freq)
        self.visualizer.plot_tree(self.huffman.tree_root)
        self.visualizer.plot_compression_comparison(
            self.current_text, self.current_encoded
        )
        
        print("\n✅ All visualizations complete!")
        print("\nPress Enter to continue...")
        input()


if __name__ == "__main__":
    app = HuffmanApp()
    app.run()