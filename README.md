# FastLinkedList Data Structure

An INF1008 Data Structures and Algorithms project that demonstrates **Huffman coding** for lossless text compression. The application builds a Huffman tree, generates prefix-free binary codes, compresses and restores text, and visualizes the algorithm's results.

## Features

- Enter text manually or load it from a `.txt` file
- Count and display character frequencies
- Encode and decode text with Huffman coding
- Visualize the generated Huffman tree
- Plot character-frequency and compression charts
- Compare original and compressed sizes
- Save and load compressed `.huff` files
- Test empty, single-character, and general text inputs

## How Huffman Coding Works

Huffman coding assigns shorter binary codes to frequently occurring characters and longer codes to less frequent characters. The program:

1. Counts the frequency of every character.
2. inserts each character into a min-heap.
3. Repeatedly combines the two nodes with the lowest frequencies.
4. Traverses the resulting binary tree to assign `0` to left edges and `1` to right edges.
5. Replaces each character with its generated binary code.

Because no generated code is the prefix of another, the compressed bit string can be decoded without ambiguity.

## Project Structure

```text
.
├── Code/
│   ├── src/
│   │   ├── main.py          # Interactive command-line application
│   │   ├── huffman.py       # Huffman tree, encoding, and decoding
│   │   ├── visualizer.py    # Tree and chart visualizations
│   │   └── file_handler.py  # Text and compressed-file operations
│   ├── tests/
│   │   └── test_huffman.py  # Automated unit tests
│   ├── data/                # Generated charts and data files
│   └── requirements.txt     # Python dependencies
├── INF1008_P5_Team04_Report.pdf
└── README.md
```

## Requirements

- Python 3.9 or newer
- `pip`

## Installation

Clone the repository and move into the project directory:

```bash
git clone <repository-url>
cd INF_1008_DSA_FastLinkedList-Data-Structure
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r Code/requirements.txt
```

## Usage

Run the application from the `Code` directory so its data paths resolve correctly:

```bash
cd Code
python src/main.py
```

Use the interactive menu to enter or load text, inspect frequencies, view the Huffman tree, compare compression results, and save or restore `.huff` files.

## Running the Tests

From the `Code` directory, run:

```bash
pytest tests/ -v
```

The tests cover frequency counting, empty input, repeated characters, encoding and decoding round trips, the prefix property, and compression-ratio calculations.

## Technologies Used

- Python
- `heapq` and `collections.Counter`
- Matplotlib
- NetworkX
- Pytest

## Educational Purpose

This project was developed for the **INF1008 Data Structures and Algorithms** module. It illustrates how priority queues, binary trees, recursion, dictionaries, and file handling can work together in a practical compression algorithm.

## License

This repository is intended for educational use. Add a license file if you plan to redistribute or reuse the project outside its original academic context.
