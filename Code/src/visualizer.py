"""Visualization tools for Huffman tree and compression stats."""

from typing import Any

try:
    import matplotlib.pyplot as plt
    import networkx as nx

    VISUALIZATION_AVAILABLE = True
except ImportError:
    VISUALIZATION_AVAILABLE = False
    print("Warning: matplotlib and networkx not installed. Visualization disabled.")


def visualize_tree(root: Any, save_path: str | None = None) -> None:
    """Visualize a Huffman tree using matplotlib and networkx."""
    if not VISUALIZATION_AVAILABLE:
        print("Visualization libraries not available. Install with:")
        print("  pip install matplotlib networkx")
        return

    if root is None:
        print("Error: No tree to visualize!")
        return

    graph = nx.DiGraph()
    labels: dict[int, str] = {}
    pos: dict[int, tuple[float, float]] = {}

    def add_nodes(node: Any, x: float = 0, y: int = 0, layer: int = 1, parent: Any = None, direction: str | None = None) -> None:
        if node is None:
            return

        node_id = id(node)
        offset = 1.0 / (2**layer)
        if direction == "left":
            x -= offset
        elif direction == "right":
            x += offset

        pos[node_id] = (x, -y)
        labels[node_id] = f"'{node.char}'\n({node.freq})" if node.char is not None else f"{node.freq}"
        graph.add_node(node_id)

        if parent is not None:
            graph.add_edge(id(parent), node_id)

        add_nodes(node.left, x, y + 1, layer + 1, node, "left")
        add_nodes(node.right, x, y + 1, layer + 1, node, "right")

    add_nodes(root)

    plt.figure(figsize=(12, 8))
    nx.draw(
        graph,
        pos,
        labels=labels,
        with_labels=True,
        node_color="lightblue",
        node_size=2000,
        font_size=10,
        font_weight="bold",
        arrowsize=20,
        edge_color="gray",
        linewidths=2,
    )
    plt.title("Huffman Tree Visualization", fontsize=16, fontweight="bold")
    plt.axis("off")

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"Tree visualization saved to {save_path}")
    else:
        plt.tight_layout()
        plt.show()


def print_tree_ascii(root: Any, prefix: str = "", is_tail: bool = True) -> None:
    """Print an ASCII representation of the Huffman tree."""
    if root is None:
        return

    connector = "└── " if is_tail else "├── "
    if root.char is not None:
        print(f"{prefix}{connector}'{root.char}' ({root.freq})")
    else:
        print(f"{prefix}{connector}[{root.freq}]")

    extension = "    " if is_tail else "│   "
    new_prefix = prefix + extension
    if root.left or root.right:
        if root.right:
            print_tree_ascii(root.left, new_prefix, False)
            print_tree_ascii(root.right, new_prefix, True)
        else:
            print_tree_ascii(root.left, new_prefix, True)


def display_codes_table(codes: dict[str, str]) -> None:
    """Display Huffman codes in a formatted table."""
    print("\n" + "=" * 50)
    print("HUFFMAN CODES TABLE")
    print("=" * 50)
    print(f"{'Character':<12} {'ASCII':<8} {'Huffman Code':<15} {'Bits':<6}")
    print("-" * 50)

    for char in sorted(codes.keys()):
        code = codes[char]
        ascii_val = ord(char)
        char_display = repr(char) if char in ["\n", "\t", " "] else f"'{char}'"
        print(f"{char_display:<12} {ascii_val:<8} {code:<15} {len(code):<6}")

    print("=" * 50)


class HuffmanVisualizer:
    """Visualization helper used by the main application."""

    def plot_tree(self, root: Any) -> None:
        visualize_tree(root)

    def plot_frequency_bar(self, frequency: dict[str, int]) -> None:
        if not VISUALIZATION_AVAILABLE:
            print("Visualization libraries not available. Install with:")
            print("  pip install matplotlib networkx")
            return
        if not frequency:
            print("No frequency data to visualize.")
            return

        items = sorted(frequency.items(), key=lambda item: item[1], reverse=True)
        labels = [
            "space" if ch == " " else "\\n" if ch == "\n" else "\\t" if ch == "\t" else ch
            for ch, _ in items
        ]
        values = [count for _, count in items]

        plt.figure(figsize=(10, 5))
        plt.bar(labels, values)
        plt.title("Character Frequency")
        plt.xlabel("Character")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.show()

    def plot_compression_comparison(self, original_text: str, encoded_text: str) -> None:
        if not VISUALIZATION_AVAILABLE:
            print("Visualization libraries not available. Install with:")
            print("  pip install matplotlib networkx")
            return

        original_bits = len(original_text) * 8
        encoded_bits = len(encoded_text)

        plt.figure(figsize=(7, 4))
        plt.bar(
            ["Original", "Compressed"],
            [original_bits, encoded_bits],
            color=["#4e79a7", "#59a14f"],
        )
        plt.title("Compression Comparison")
        plt.ylabel("Bits")
        plt.tight_layout()
        plt.show()
