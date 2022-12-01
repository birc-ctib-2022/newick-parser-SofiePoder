"""A Newick parser."""

from __future__ import annotations
from dataclasses import dataclass
from typing import Union, cast
import re


def tokenize(tree: str) -> list[str]:
    """
    Extract the tokens from the text representation of a tree.

    >>> tokenize("A")
    ['A']
    >>> tokenize("(A, (B, C))")
    ['(', 'A', '(', 'B', 'C', ')', ')']
    """
    return re.findall(r'[()]|\w+', tree)


@dataclass(repr=False)
class Leaf:
    """
    A leaf in a tree.

    This will just be a string for our application.
    """

    name: str

    def __str__(self) -> str:
        """Simplified text representation."""
        return self.name
    __repr__ = __str__


@dataclass(repr=False)
class Node:
    """An inner node."""

    children: list[Tree]

    def __str__(self) -> str:
        """Simplified text representation."""
        return f"({','.join(str(child) for child in self.children)})"
    __repr__ = __str__


# A tree is either a leaf or an inner node with sub-trees
Tree = Union[Leaf, Node]

class EmptyStack(Exception):
    pass

class Stack(object):
    #building stack from the book#
    def __init__(self):
        self.stack = []
    
    def push(self, x):
        self.stack.append(x)

    def top(self):
        try:
            return self.stack[-1]
        except IndexError:
            raise EmptyStack()
    
    def pop(self): 
        try:
            return self.stack.pop()
        except IndexError:
            raise EmptyStack()
    
    def is_empty(self):
        return len(self.stack) == 0

    def __bool__(self):
        return not self.is_empty()


my_stack = Stack()

def parse(tree: str) -> Tree:
    """
    Parse a string into a tree.

    >>> parse("(A, (B, C))")
    (A,(B,C))
    """
    for token in tokenize(tree):
        if token == "(":           # Whenever you see a token that isn’t ), push it on the stack
            my_stack.push(token)
            

        if token != "(" and token != ")":
            my_stack.push(token)
            
    
        elif token == ")":        # If you see a token that is neither ( or ) it must be a leaf
            leaf_lst = []         # so create a leaf and push it to the stack
            
            leaf = my_stack.pop() # When you see ), iteratively pop trees from the stack and collect them in a list.
            while leaf != "(":    #  When you reach the first ( you stop popping, you create the new tree, and you push it on the stack.
                leaf_lst.append(leaf)
                leaf = my_stack.pop()
            leaf_lst.reverse()
            subtree = Node(leaf_lst)
            my_stack.push(subtree)

    return my_stack.pop()
            
                
          


            
    
print(parse("(A, (B, C))"))