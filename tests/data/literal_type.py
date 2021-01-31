from typing import List

a: Literal["foo"]
b: Literal['foo', 'bar']


def f(a: Literal['bar']) -> List[Literal['baz']]:
    pass



class Cat:

    a: str
    b: Literal['str']

    def func2(b: str, c: Literal['str']):
        def func2func(d: Literal['int']):
            d = d
            d = cast('int', d)

    class Bat:
        e: Literal['int']


def callable_func(a: Callable[[Literal['str']], Literal['str']]):
    ...
