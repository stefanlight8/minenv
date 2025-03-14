"""A minimal module for working with dotenv files.

Examples
--------
>>> from minenv import load_dotenv, getenv
>>> load_dotenv()

Load the dotenv file from `.env`. If any error occurs, nothing will happen.
However, if the value is being retrieved from a `load_dotenv()` call:

>>> env = load_dotenv()
>>> print(env)  # `None` if all is alright.
>>> print(env)  # In case of `Exception`, Houston, we have a problem.

>>> load_dotenv(verbose=True)

In this case, if there's an exception, the function will raise it.

>>> key: str = getenv("API_KEY")

`getenv()` returns the value from the environment by the key if it exists.
If the key doesn't exist, `getenv()` will raise a `KeyError`.

To avoid this exception:

>>> max_connections: Union[str, int] = getenv("MAX_CONNECTIONS", default=100)

You can pass any value as the `default` argument, which prevents the exception!

However, as you can see, `max_connections` might be `str`, which could be problematic.
To avoid this, `getenv()` provides a way to cast the result:

>>> max_connections: int = getenv("MAX_CONNECTIONS", into=int)

Now `max_connections` will be of type `int`.
"""

import sys
import typing
from os import PathLike, environ

if sys.version_info >= (3, 13):
    from collections.abc import Callable, Iterable, Sequence
else:
    from typing import Callable, Iterable, Sequence

__all__: Sequence[str] = ("load", "load_dotenv", "get", "getenv")

DefaultT = typing.TypeVar("DefaultT")
T = typing.TypeVar("T")

UNDEFINED: typing.Final = ...
QUOTES: typing.Final[typing.Set[str]] = {'"', "'"}


def parse_stream(stream: typing.TextIO) -> Iterable[typing.Tuple[str, str]]:
    for line in stream:
        content = line.strip()
        if not content or content[0] == "#" or "=" not in content:
            continue

        key, _, value = content.partition("=")
        key, value = key.strip(), value.strip()
        if value[1] in QUOTES and value[-1] in QUOTES:
            value = value[1:-1]

        yield key, value


def load(
    path: typing.Union[str, PathLike[str]] = ".env",
    stream: typing.Optional[typing.TextIO] = None,
    *,
    override: bool = True,
    verbose: bool = False,
) -> typing.Union[None, Exception]:
    """Load environment variables from a dotenv file.

    Parameters
    ----------
    path : str or PathLike, default=".env"
        The path to the dotenv file to be loaded.
    stream: TextIO, optional
        A file-like object to read from instead of opening the file at `path`.
        If provided, `path` is ignored.
    override : bool, default=True
        Whether to override existing environment variables with values from
        the file. If `False`, existing environment variables are not overwritten.
    verbose : bool, default=False
        Check returns.

    Returns
    -------
    None or Exception
        - If no errors occur, the function returns `None`.
        - If an error occurs and `verbose` is `False`,
            the exception will be returned.
        - If `verbose` is `True`, the exception will be raised.

    Notes
    -----
    - Lines starting with `#` are treated as comments and are ignored.
    - Comments after a value are not supported and may cause parsing issues.
    """
    try:
        with stream or open(path, encoding="UTF-8") as inner:
            for key, value in parse_stream(inner):
                if not override and environ.get(key):
                    continue
                environ[key] = value
    except Exception as error:
        if verbose:
            raise error
        return error


@typing.overload
def get(key: str, *, into: Callable[[typing.Any], T] = str) -> T: ...


@typing.overload
def get(key: str, *, default: DefaultT, into: Callable[[typing.Any], T] = str) -> typing.Union[T, DefaultT]: ...


def get(
    key: str, *, default: typing.Any = UNDEFINED, into: Callable[[typing.Any], T] = str
) -> typing.Union[T, typing.Any]:
    """Get value from the environment by key.

    Parameters
    ----------
    key : str
        The environment variable key to retrieve.
    default : DT, optional
        The value to return if the environment variable is not found.
        Defaults to `NO_DEFAULT`, which raises a `KeyError` if no value is found.
    into : Callable[[Any], T], optional
        A function used to convert the retrieved value.
        Defaults to `str`, meaning the value will be returned as a string.

    Notes
    -----
    Default value is not converting by `into`.
    """
    value: typing.Any = environ.get(key, default=default)
    if value is UNDEFINED:
        raise KeyError(f"`{key}` cannot be found in environment")
    if value is None:
        return value
    return into(value)


load_dotenv = load
getenv = get
