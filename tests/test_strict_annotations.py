import pytest

from src.utils.checkers import strict_annotations


@strict_annotations()
def accept_simple(a: str, b: int, c: bool) -> bool:
    return True


@strict_annotations()
def accept_complex(a: list[int], b: tuple[str, ...], c: dict[str, list[int]]) -> bool:
    return True


@pytest.mark.parametrize("a, b, c, arg_exc, func",
                         [
                             ("1", 2, True, None, accept_simple),
                             (2, 1, True, "a", accept_simple),
                             ("2", "1", True, "b", accept_simple),
                             ("2", 1, "x", "c", accept_simple),
                             ([1], ("1",), {"1": [1]}, None, accept_complex),
                             (["1"], ("1", "2",), {"1": [1]}, "a", accept_complex),
                             (1, ("1",), {"1": [1]}, "a", accept_complex),
                             ([1], 1, {"1": [1]}, "b", accept_complex),
                             ([1], (1, 2), {"1": [1]}, "b", accept_complex),
                             ([1], ("1",), 1, "c", accept_complex),
                             ([1], ("1",), {1: [1]}, "c", accept_complex),
                             ([1], ("1",), {"1": 3}, "c", accept_complex),
                         ]
                         )
def test_simple(a, b, c, arg_exc, func):
    if not arg_exc:
        assert func(a, b, c)
    else:
        with pytest.raises(TypeError) as exc:
            func(a, b, c)

        assert f"'{arg_exc}'" in str(exc)
