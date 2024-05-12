from typing import Any
from ast import *
from representations.tree.node import Node
from representations.builders.ast.tearers.base_tearer import BaseTearer
from representations.builders.ast.tearers.tearer_factory import TearerFactory


class CallTearer(BaseTearer):
    def is_match(self, node):
        return node.label in ["Call"]

    def tear(self, node: Node) -> Any:
        factory = TearerFactory()

        # func
        func = None
        func_node = node.children[0]
        if func_node.label == "func":
            tearer = factory.get_tearer(func_node.children[0])
            func = tearer.tear(func_node.children[0])
           
        # args 
        args = []
        if node.get_children(label="arg", direct=True):
            arg_nodes = [child for child in node.get_children(label="arg", direct=True)]
            for arg_node in arg_nodes:
                if arg_node.label == "arg":
                    tearer = factory.get_tearer(arg_node.children[0])
                    item = tearer.tear(arg_node.children[0])
                    args.append(item)
        
        # keywords    
        keywords = []
        if node.get_children(label="keyword", direct=True):
            keyword_nodes = [child for child in node.get_children(label="keyword", direct=True)]
            for child in keyword_nodes:
                if child.label == "keyword":
                    tearer = factory.get_tearer(child)
                    item = tearer.tear(child)
                    keywords.append(item)
                
        return Call(func=func, args=args, keywords=keywords, lineno=None)
        