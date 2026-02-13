class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class Stack:
    def __init__(self):
        self.top = None

    def push(self, value):
        new_node = Node(value)
        new_node.next = self.top
        self.top = new_node
        print(f"Pushed: {value}")

    def pop(self):
        if self.top is None:
            print("Stack is empty. Cannot pop.")
            return None

        removed_value = self.top.value
        self.top = self.top.next
        print(f"Popped: {removed_value}")
        return removed_value

    def print_stack(self):
        if self.top is None:
            print("Stack is empty.")
            return

        current = self.top
        print("Stack (top to bottom):")
        while current:
            print(current.value)
            current = current.next


stack = Stack()

stack.push(10)
stack.push(20)
stack.push(30)

stack.print_stack()

stack.pop()
stack.print_stack()
stack.pop()
stack.print_stack()
stack.pop()
stack.print_stack()