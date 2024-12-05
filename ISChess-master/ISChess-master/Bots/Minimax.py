class Tree:
    def __init__(self):
        self.left = None
        self.right = None
        self.data = None


if __name__ == '__main__':
    root = Tree()
    root.data = "root"
    root.left = Tree()
    root.left.data = "left"
    root.right = Tree()
    root.right.data = "right"
    print(root)
