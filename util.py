class Node:
    def __init__(self, data, next):
        self.data = data
        self.next = next

class Stack:
    def __init__(self):
        self.top = None
        self.count = 0
    
    def push(self, item):
        if self.top == None:
            self.top = Node(item, None)
        else:
            new = Node(item, self.top)
            self.top = new
        self.count += 1

    def pop(self):
        if self.top != None:
            result = self.top.data
            self.top = self.top.next
            self.count -= 1
            return result
        else:
            return None

    def peek(self):
        if self.count == 0:
            return None
        return self.top.data

    def size(self):
        return self.count

    def isEmpty(self):
        return self.count == 0

class Queue:
    def __init__(self):
        self.first = None
        self.last = None
        self.count = 0

    def enqueue(self, item):
        if self.first == None:
            self.last = Node(item, None)
            self.first = self.last
        else:
            self.last.next = Node(item, None)
            self.last = self.last.next
        self.count += 1

    def dequeue(self):
        if self.first != None:
            result = self.first.data
            self.first = self.first.next
            self.count -= 1
            return result
        return None

    def peek(self):
        if self.count == 0:
            return None
        return self.first.data

    def size(self):
        return self.count

    def isEmpty(self):
        return self.count == 0


class MinStack:
    def __init__(self):
        self.mainStack = Stack()
        self.minStack = Stack()

    def push(self, item):
        if self.mainStack.isEmpty():
            self.mainStack.push(item)
            self.minStack.push(item)
        else:
            self.mainStack.push(item)
            if item < self.minStack.peek():
                self.minStack.push(item)

    def pop(self):
        if self.mainStack.isEmpty():
            return None
        poppedItem = self.mainStack.pop()
        if poppedItem == self.minStack.peek():
            self.minStack.pop()
        return poppedItem

    def min(self):
        return self.minStack.peek()

    def size(self):
        return self.mainStack.size()

    def isEmpty(self):
        return self.mainStack.isEmpty()

class Tree:
    def __init__(self, value):
        self.data = value
        self.left = None
        self.right = None

    def add(self, value):
        if value < self.data:
            if self.left == None:
                self.left = Tree(value)
            else:
                self.left.add(value)
        if value > self.data:
            if self.right == None:
                self.right = Tree(value)
            else:
                self.right.add(value)
    
    def preorderPrint(self):
        print self.data
        if self.left != None:
            self.left.preorderPrint()
        if self.right != None:
            self.right.preorderPrint()

    def preorderArray(self):
        result = [self.data]
        left, right = [], []
        if self.left != None:
            left += self.left.preorderArray()
        if self.right != None:
            right += self.right.preorderArray()
        return result + left + right

    def equals(self, b):
        if self.data != b.data:
            return False
        left_eq, right_eq = True, True
        if self.left != None and b.left != None:
            left_eq = self.left.equals(b.left)
        if self.right != None and b.left != None:
            right_eq = self.right.equals(b.right)
        return left_eq and right_eq
