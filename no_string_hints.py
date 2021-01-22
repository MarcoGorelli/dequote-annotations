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


def process_annotation(
    annotation: Optional[Union[ast.expr, ast.slice]],
    to_replace: MutableMapping[Offset, str],
) -> None:
    if isinstance(annotation, ast.Constant):
        if isinstance(annotation.value, str):
            to_replace[
                Offset(
                    annotation.lineno,
                    annotation.col_offset,
                )
            ] = annotation.value
        return
    if isinstance(annotation, ast.Str):  # pragma: nocover_py38
        # Only for Python 3.6, Python 3.7
        to_replace[
            Offset(
                annotation.lineno,
                annotation.col_offset,
            )
        ] = annotation.s
        return
    if isinstance(annotation, (ast.Name, ast.NameConstant)):
        return
    if isinstance(annotation, (ast.Tuple, ast.List)):
        for i in annotation.elts:
            process_annotation(i, to_replace)
        return
    if isinstance(annotation, ast.Index):
        return process_annotation(annotation.value, to_replace)
    if isinstance(annotation, ast.Subscript):
        return process_annotation(annotation.slice, to_replace)
    return


def process_function(
    func: ast.FunctionDef,
    to_replace: MutableMapping[Offset, str],
) -> None:
    for i in func.args.args:
        process_annotation(i.annotation, to_replace)
    for i in func.args.kwonlyargs:
        process_annotation(i.annotation, to_replace)
    for i in getattr(func.args, 'posonlyargs', []):
        process_annotation(i.annotation, to_replace)
    process_annotation(func.returns, to_replace)
    process_body(func.body, to_replace)


def process_class(
    class_: ast.ClassDef,
    to_replace: MutableMapping[Offset, str],
) -> None:
    for statement in class_.body:
        if isinstance(statement, ast.AnnAssign):
            process_annotation(statement.annotation, to_replace)
        elif isinstance(statement, ast.FunctionDef):
            process_function(statement, to_replace)
        elif isinstance(statement, ast.ClassDef):
            process_class(statement, to_replace)
    process_body(class_.body, to_replace)


def process_body(
    body: Sequence[ast.stmt],
    to_replace: MutableMapping[Offset, str],
) -> None:
    for statement in body:
        if isinstance(statement, ast.FunctionDef):
            process_function(statement, to_replace)
        elif isinstance(statement, ast.ClassDef):
            process_class(statement, to_replace)
        elif isinstance(statement, ast.AnnAssign):
            process_annotation(statement.annotation, to_replace)


def no_string_types(file: str) -> None:
    to_replace: MutableMapping[Offset, str] = {}

    with open(file, encoding='utf-8') as fd:
        content = fd.read()
    tree = ast.parse(content)

    process_body(tree.body, to_replace)
    tokens = src_to_tokens(content)

    if not to_replace:
        return
    for n, i in reversed_enumerate(tokens):
        if i.offset in to_replace:
            tokens[n] = i._replace(src=to_replace[i.offset])

    with open(file, 'w', encoding='utf-8') as fd:
        fd.write(tokens_to_src(tokens))


def main(argv: Optional[Sequence[str]] = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*')
    args = parser.parse_args(argv)

    for i in args.files:
        no_string_types(i)


if __name__ == '__main__':  # pragma: nocover
    main()
