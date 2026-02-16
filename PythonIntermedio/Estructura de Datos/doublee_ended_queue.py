class Node:
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None


class Deque:
    def __init__(self):
        self.left = None   
        self.right = None

    def push_left(self, value):
        new_node = Node(value)

        if self.left is None:
            self.left = new_node
            self.right = new_node
        else:
            new_node.next = self.left
            self.left.prev = new_node
            self.left = new_node

        print(f"Pushed left: {value}")

    def push_right(self, value):
        new_node = Node(value)

        if self.right is None:
            self.left = new_node
            self.right = new_node
        else:
            new_node.prev = self.right
            self.right.next = new_node
            self.right = new_node

        print(f"Pushed right: {value}")

    def pop_left(self):
        if self.left is None:
            print("Deque is empty. Cannot pop_left.")
            return None

        removed_value = self.left.value

        if self.left == self.right:
            self.left = None
            self.right = None
        else:
            self.left = self.left.next
            self.left.prev = None

        print(f"Popped left: {removed_value}")
        return removed_value

    def pop_right(self):
        if self.right is None:
            print("Deque is empty. Cannot pop_right.")
            return None

        removed_value = self.right.value

        if self.left == self.right:
            self.left = None
            self.right = None
        else:
            self.right = self.right.prev
            self.right.next = None

        print(f"Popped right: {removed_value}")
        return removed_value

    def print_deque(self):
        if self.left is None:
            print("Deque is empty.")
            return

        print("Deque (left to right):")
        current = self.left
        while current:
            print(current.value)
            current = current.next


dq = Deque()

dq.push_left(10)   
dq.push_right(20)  
dq.push_left(5)    
dq.push_right(30)  

dq.print_deque()

dq.pop_left()
dq.pop_right()     

dq.print_deque()