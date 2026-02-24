from functools import wraps
from typing import get_args, get_origin, Union
from inspect import signature, Parameter


def _isinstance(obj, annotation) -> bool:
    if annotation is Parameter.empty:
        return True

    origin = get_origin(annotation)
    args = get_args(annotation)
    if origin is Union:
        return any(_isinstance(obj, arg) for arg in args)

    elif origin is list or origin is set:
        if not isinstance(obj, origin):
            return False
        if args:
            return all(_isinstance(item, args[0]) for item in obj)
        return True

    elif origin is tuple:
        if not isinstance(obj, tuple):
            return False
        if args:
            if len(args) == 2 and args[1] is ...:
                item_type = args[0]
                return all(_isinstance(item, item_type) for item in obj)
            elif len(args) == len(obj):
                return all(_isinstance(item, arg_type)
                           for item, arg_type in zip(obj, args))
        return True

    elif origin is dict:
        if not isinstance(obj, dict):
            return False

        if args and len(args) == 2:
            key, val = args
            return all(
                _isinstance(k, key) and _isinstance(v, val)
                for k, v in obj.items()
            )
        return True

    else:
        return isinstance(obj, annotation)


def strict_annotations(*arg_names):
    """
    Checks if args match their annotations.
    Warning: callable and protocols are check only with is_instance()
    :param arg_names:
    :return: decorator
    :raise TypeError if args do not match their annotations
    """

    def decorator(func):
        sig = signature(func)
        parameters = sig.parameters
        check_args = arg_names if arg_names else tuple(parameters.keys())

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            all_args = bound_args.arguments
            for arg_name in check_args:
                param = parameters[arg_name]
                value = all_args[arg_name]
                if not _isinstance(value, param.annotation):
                    raise TypeError(
                        f"invalid arg type for '{arg_name}' in function '{func.__name__}': expected {param.annotation}, found {type(value)}")
            return func(*args, **kwargs)

        return wrapper

    return decorator


if __name__ == '__main__':
    @strict_annotations()
    def x(a: dict[str, int]): ...

    print(x(1))