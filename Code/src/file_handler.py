"""
File I/O handler for Huffman Coding
"""
import json
import os
from typing import Any, Dict, Optional, Tuple


class FileHandler:
    """
    Handle file operations for Huffman coding
    """
    
    def read_file(self, filepath: str) -> str:
        """
        Read text from file
        
        Args:
            filepath: Path to the file
            
        Returns:
            Text content of the file
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()

    def read_text_file(self, filepath: str) -> str:
        """Read text file safely. Returns empty string on failure."""
        candidate_paths = [filepath]

        # If a bare filename is provided, also try inside data/.
        if not os.path.isabs(filepath):
            candidate_paths.append(os.path.join('data', filepath))

        for candidate in candidate_paths:
            try:
                with open(candidate, 'r', encoding='utf-8') as f:
                    return f.read()
            except (OSError, UnicodeDecodeError):
                continue

        return ""
    
    def write_file(self, filepath: str, content: str):
        """
        Write text to file
        
        Args:
            filepath: Path to the file
            content: Text content to write
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    def list_text_files(self, directory: str = '.') -> list[str]:
        """List .txt files in a directory (and data/ when scanning project root)."""
        files: list[str] = []

        search_dirs = [directory]
        if directory == '.':
            search_dirs.append('data')

        for folder in search_dirs:
            try:
                for name in os.listdir(folder):
                    full_path = os.path.join(folder, name)
                    if os.path.isfile(full_path) and name.lower().endswith('.txt'):
                        files.append(full_path if folder != '.' else name)
            except OSError:
                continue

        return sorted(set(files))

    def get_file_size(self, filepath: str) -> int:
        """Get file size in bytes. Returns 0 if path does not exist."""
        try:
            return os.path.getsize(filepath)
        except OSError:
            return 0
    
    def save_encoded(self, base_filename: str, encoded: str, codes: Dict[str, str]):
        """
        Save encoded data and codes to files
        
        Args:
            base_filename: Base filename (without extension)
            encoded: Encoded binary string
            codes: Dictionary of Huffman codes
        """
        # Save encoded data
        encoded_path = f"{base_filename}.huff"
        with open(encoded_path, 'w') as f:
            f.write(encoded)
        
        # Save codes as JSON
        codes_path = f"{base_filename}_codes.json"
        with open(codes_path, 'w') as f:
            json.dump(codes, f, indent=2)

    def save_compressed(
        self,
        filepath: str,
        encoded: str,
        codes: Dict[str, str],
        original: str,
    ) -> bool:
        """Save compressed payload (encoded bits + codes + original text) to one .huff JSON file."""
        try:
            if not filepath.lower().endswith('.huff'):
                filepath = f"{filepath}.huff"

            payload = {
                'encoded': encoded,
                'codes': codes,
                'original': original,
            }
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(payload, f, indent=2, ensure_ascii=False)
            return True
        except OSError:
            return False

    def load_compressed(self, filepath: str) -> Optional[Dict[str, Any]]:
        """Load compressed payload created by save_compressed()."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if not isinstance(data, dict):
                return None

            required_keys = {'encoded', 'codes', 'original'}
            if not required_keys.issubset(data.keys()):
                return None

            return {
                'encoded': str(data['encoded']),
                'codes': dict(data['codes']),
                'original': str(data['original']),
            }
        except (OSError, json.JSONDecodeError, TypeError, ValueError):
            return None
    
    def load_encoded(self, encoded_path: str, codes_path: str) -> Tuple[str, Dict[str, str]]:
        """
        Load encoded data and codes from files
        
        Args:
            encoded_path: Path to encoded data file
            codes_path: Path to codes JSON file
            
        Returns:
            Tuple of (encoded string, codes dictionary)
        """
        # Load encoded data
        with open(encoded_path, 'r') as f:
            encoded = f.read()
        
        # Load codes
        with open(codes_path, 'r') as f:
            codes = json.load(f)
        
        return encoded, codes
    
    def save_binary(self, filepath: str, encoded: str):
        """
        Save encoded data as actual binary file
        
        Args:
            filepath: Path to save binary file
            encoded: Binary string (0s and 1s)
        """
        # Convert binary string to bytes
        # Pad to make it multiple of 8
        padding = 8 - len(encoded) % 8
        if padding != 8:
            encoded = encoded + '0' * padding
        
        # Convert to bytes
        byte_array = bytearray()
        for i in range(0, len(encoded), 8):
            byte = encoded[i:i+8]
            byte_array.append(int(byte, 2))
        
        # Write binary file
        with open(filepath, 'wb') as f:
            # Write padding info as first byte
            f.write(bytes([padding]))
            f.write(bytes(byte_array))
    
    def load_binary(self, filepath: str) -> str:
        """
        Load binary file and convert to binary string
        
        Args:
            filepath: Path to binary file
            
        Returns:
            Binary string (0s and 1s)
        """
        with open(filepath, 'rb') as f:
            # Read padding info
            padding = f.read(1)[0]
            
            # Read remaining bytes
            byte_data = f.read()
        
        # Convert bytes to binary string
        binary_string = ''.join(format(byte, '08b') for byte in byte_data)
        
        # Remove padding
        if padding != 8:
            binary_string = binary_string[:-padding]
        
        return binary_string
