class TernaryNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.middle = None
        self.right = None

def print_tree(node, level=0, prefix="Root:"):
    """
    Prints the ternary tree structure.
    """
    if node is not None:
        print(" " * (level*4) + prefix, node.data)
        if node.left or node.middle or node.right:
            print_tree(node.left, level + 1, "L---")
            print_tree(node.middle, level + 1, "M---")
            print_tree(node.right, level + 1, "R---")

if __name__ == '__main__':
    # Example of building a ternary tree representing a Triad Matrix

    # Level 0
    root = TernaryNode("Level 0")

    # Level 1
    root.left = TernaryNode("Level 1 - Node 1")
    root.middle = TernaryNode("Level 1 - Node 2")
    root.right = TernaryNode("Level 1 - Node 3")

    # Level 2
    root.left.left = TernaryNode("Level 2 - Node 1.1")
    root.left.middle = TernaryNode("Level 2 - Node 1.2")
    root.left.right = TernaryNode("Level 2 - Node 1.3")

    root.middle.left = TernaryNode("Level 2 - Node 2.1")
    # ... and so on

    print("Ternary Tree Representation of a Triad Matrix:")
    print_tree(root)
