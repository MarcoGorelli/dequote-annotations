import argparse
import ast
from typing import MutableMapping
from typing import Optional
from typing import Sequence
from typing import Union

from tokenize_rt import Offset
from tokenize_rt import reversed_enumerate
from tokenize_rt import src_to_tokens
from tokenize_rt import tokens_to_src


class Visitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.to_replace: MutableMapping[Offset, str] = {}
        self.has_future_annotations: bool = False

    def replace_string_literal(
        self,
        annotation: Optional[Union[ast.expr, ast.slice]],
    ) -> None:
        if isinstance(annotation, ast.Constant):
            if isinstance(annotation.value, str):
                self.to_replace[
                    Offset(
                        annotation.lineno,
                        annotation.col_offset,
                    )
                ] = annotation.value
            return
        elif isinstance(annotation, ast.Str):  # pragma: nocover_py38
            # Only for Python 3.6, Python 3.7
            self.to_replace[
                Offset(
                    annotation.lineno,
                    annotation.col_offset,
                )
            ] = annotation.s
            return
        elif isinstance(annotation, (ast.Tuple, ast.List)):
            for i in annotation.elts:
                self.replace_string_literal(i)
        elif isinstance(annotation, ast.Index):
            self.replace_string_literal(annotation.value)
        elif isinstance(annotation, ast.Subscript):
            if isinstance(annotation.value, ast.Name):
                if annotation.value.id != 'Literal':
                    self.replace_string_literal(annotation.slice)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        for i in node.args.args:
            self.replace_string_literal(i.annotation)
        for i in node.args.kwonlyargs:
            self.replace_string_literal(i.annotation)
        for i in getattr(node.args, 'posonlyargs', []):
            self.replace_string_literal(i.annotation)
        self.replace_string_literal(node.returns)
        super().generic_visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        self.replace_string_literal(node.annotation)
        super().generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if (
            node.module == '__future__'
            and 'annotations' in {i.name for i in node.names}
        ):
            self.has_future_annotations = True
        super().generic_visit(node)


def no_string_types(content: str) -> Optional[str]:
    tree = ast.parse(content)

    visitor = Visitor()
    visitor.visit(tree)

    if not visitor.to_replace or not visitor.has_future_annotations:
        # nothing to replace.
        return content

    tokens = src_to_tokens(content)
    for n, i in reversed_enumerate(tokens):
        if i.offset in visitor.to_replace:
            tokens[n] = i._replace(src=visitor.to_replace[i.offset])

    return tokens_to_src(tokens)


def main(argv: Optional[Sequence[str]] = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*')
    args = parser.parse_args(argv)

    for i in args.files:
        with open(i, encoding='utf-8') as fd:
            content = fd.read()
        new_content = no_string_types(content)
        if new_content is not None:
            with open(i, 'w', encoding='utf-8') as fd:
                fd.write(new_content)


if __name__ == '__main__':  # pragma: nocover
    main()
