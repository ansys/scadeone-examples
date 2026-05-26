"""Generate instance tree diagram for Scade One models."""

import argparse
import os
from typing import Union, cast

import networkx as nx
import pydot

from ansys.scadeone.core.scadeone import ScadeOne
from ansys.scadeone.core.svc.swan_visitor import SwanVisitor
import ansys.scadeone.core.swan as swan

scade_one_install_dir = r"C:\Program Files\ANSYS Inc\v261\Scade One"
graphviz_path = r"C:\cygwin64\bin"  # Should be configured by user if not in PATH
os.environ["PATH"] += os.pathsep + graphviz_path


def is_library_operator(path):
    """Check if `path` is part of Swan standard library."""
    module_name = path.split("::", 1)[0]  # extract module or toplevel namespace
    return module_name in [
        "Bitfield",
        "Control",
        "Digital",
        "Float",
        "Flows",
        "Math",
        "Matrix",
        "Harness",
        "Vector",
    ]


class InstanceVisitor(SwanVisitor):
    """Visitor to compute the operators called by all operators in the model."""

    def __init__(self) -> None:
        super().__init__()
        self._current_op = None
        self._called = {}

    def get_called(self, op):
        """Return the list of operators called by 'op'."""
        return self._called.get(op, None)

    def visit_OperatorDefinition(  # noqa: N802
        self,
        swan_obj: swan.OperatorDefinition,
        owner: Union[swan.SwanItem, None],
        property: Union[str, None],
    ) -> None:
        """Visit an operator definition and track called operators.

        Sets _current_op to the current operator and continues traversal.
        """
        self._current_op = swan_obj
        self._called[swan_obj.get_full_path()] = []
        super().visit_OperatorDefinition(swan_obj, owner, property)
        self._current_op = None

    def visit_NamedInstance(  # noqa: N802
        self,
        swan_obj: swan.NamedInstance,
        owner: Union[swan.SwanItem, None],
        property: Union[str, None],
    ) -> None:
        """Visit a named instance and record operator calls.

        Ignores unknown operators.
        """
        if self._current_op is None:
            return
        name = str(swan_obj.path_id)
        op = self._current_op.body.get_declaration(name)
        if op is None:
            return

        # add called_operator to the list of called operators
        called_operator = cast(swan.OperatorDefinition, op).get_full_path()
        current_op_name = self._current_op.get_full_path()
        if called_operator not in self._called[current_op_name]:
            self._called[current_op_name].append(called_operator)


def gen_instance_tree(model, root):
    """Generate an instance tree, starting from root (and ignoring library operators)."""

    def add_to_graph(graph, op, visitor):
        """Add node `op` to the graph, using info from `visitor`."""
        graph.add_node(op)
        called_ops = visitor.get_called(op)
        # ignore called operators for library operators
        if not is_library_operator(op) and called_ops:
            for called_op in called_ops:
                graph.add_edge(op, called_op)
                add_to_graph(graph, called_op, visitor)

    # Create visitor and visit model
    visitor = InstanceVisitor()
    for module in model.modules:
        visitor.visit(module)

    if not visitor.get_called(root):
        print("Unknown operator: %s" % root)
        exit(2)
    # build graph starting from root
    graph = nx.DiGraph()
    add_to_graph(graph, root, visitor)
    return graph


def print_graph(graph, output_file):
    """Print the graph as a PNG, using graphviz."""

    def id(n):
        return n.replace("::", "_")  # avoid '::' in names

    dot_graph = pydot.Dot("instance_tree", graph_type="digraph")
    for n in graph.nodes():
        dot_n = pydot.Node(id(n), label=n, shape="box")
        if is_library_operator(n):
            dot_n.set("color", "blue")
        dot_graph.add_node(dot_n)
        for dst in graph.neighbors(n):
            dot_e = pydot.Edge(id(n), id(dst))
            dot_graph.add_edge(dot_e)
    dot_graph.write(output_file, format="png")


if __name__ == "__main__":
    # Parse project path and root operator from command line
    parser = argparse.ArgumentParser(
        prog="InstanceTree", description="Generate instance tree"
    )
    parser.add_argument("project")
    parser.add_argument("root")
    args = parser.parse_args()

    # initialize PyScadeOne and get model
    app = ScadeOne(install_dir=scade_one_install_dir)
    project = app.load_project(args.project)
    project.model.load_all_modules()

    # generate and print instance tree
    graph = gen_instance_tree(project.model, args.root)
    print_graph(graph, args.root.replace("::", "_") + "_graph.png")
