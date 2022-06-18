from astroid import nodes
from pylint.checkers import BaseChecker
from pylint.lint import PyLinter


def get_node_type(self, node: nodes):
    return type(node).__name__


class ForChecker(BaseChecker):

    name = "for-checker"
    msgs = {
        "W0528": (
            "First line after %s is not a statment",
            "non-statement-first-line",
            "First line after statments should not be expretions.",
        ),
    }

    allow_list = [
        "For",
        "FunctionDef",
        "AsyncFunctionDef",
        "ClassDef",
        "Return",
        "AsyncFor",
        "While",
        "If",
        "With",
        "AsyncWith",
        "Raise",
        "Try",
        "Assert"
    ]

    def visit_for(self, node: nodes.For):
        for child_node in node.get_children():
            if child_node.lineno <= node.lineno:
                continue
            if get_node_type(child_node) in self.allow_list:
                break
            else:
                if child_node.lineno != node.lineno + 2:
                    self.add_message("non-statement-first-line", node=node, args="for")
                break


def register(linter: "PyLinter") -> None:
    """This required method auto registers the checker during initialization.
    :param linter: The linter to register the checker to.
    """
    linter.register_checker(ForChecker(linter))
