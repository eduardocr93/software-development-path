class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if self.root is None:
            self.root = Node(value)
        else:
            self._insert_recursive(self.root, value)

    def _insert_recursive(self, current, value):
        if value < current.value:
            if current.left is None:
                current.left = Node(value)
            else:
                self._insert_recursive(current.left, value)
        else:
            if current.right is None:
                current.right = Node(value)
            else:
                self._insert_recursive(current.right, value)

    def print_tree(self):
        if self.root is None:
            print("Tree is empty.")
        else:
            self._print_structure(self.root, 0)

    def _print_structure(self, node, level):
        if node is not None:
            self._print_structure(node.right, level + 1)

            print("    " * level + str(node.value))

            self._print_structure(node.left, level + 1)

tree = BinaryTree()

tree.insert(10)
tree.insert(5)
tree.insert(20)
tree.insert(3)
tree.insert(7)
tree.insert(30)

tree.print_tree()