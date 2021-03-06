import ast
from collections import defaultdict

class ast_visitor(ast.NodeVisitor):
    def __init__(self):
        self.callees = [] 

    def visit_Call(self, node):
        self.callees.append(node.func.id)
        self.generic_visit(node)


def get_call_graph(tree):
    call_graph = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            visitor = ast_visitor()
            visitor.visit(node)
            call_graph[node.name] = visitor.callees

    return call_graph 

def compute_reach_graph(tree):
    nodes = tree.keys()
    reach_map = {}
    for curr_node in nodes:
        reach_map[curr_node] = get_reach_nodes(tree, curr_node, curr_node, [], 1) 
    return reach_map

def get_reach_nodes(call_graph, curr_call, root, reach_nodes_h, root_flag):
    if not call_graph[curr_call] and not root_flag:
        if curr_call not in reach_nodes_h:
            reach_nodes_h += [curr_call]
        return reach_nodes_h 
    else:
        if curr_call in reach_nodes_h:
            if curr_call not in reach_nodes_h:
                reach_nodes_h += [curr_call]
            return reach_nodes_h 
        if root == curr_call and not root_flag:
            reach_nodes_h += ['*']
            return reach_nodes_h 
        else:
            if curr_call != root:
                if curr_call not in reach_nodes_h:
                    reach_nodes_h += [curr_call]
            for call_iter in call_graph[curr_call]:
                reach_nodes_h = get_reach_nodes(call_graph, call_iter, root, reach_nodes_h, 0)
            return reach_nodes_h

