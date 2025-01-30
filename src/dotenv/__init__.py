"""A minimal module for working with dotenv files.

Examples
--------
>>> from dotenv import load_dotenv, getenv
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

from typing import Any, Callable, Final, Optional, Sequence, TextIO, TypeVar, Union, overload
from os import PathLike, environ

__all__: Sequence[str] = ("load", "load_dotenv", "get", "getenv")

NO_DEFAULT: Final = ...
DT = TypeVar("DT")  # Default value Type
T = TypeVar("T")


def load(
    path: Union[str, PathLike[str]] = ".env",
    stream: Optional[TextIO] = None,
    *,
    override: bool = True,
    verbose: bool = False,
) -> Union[None, Exception]:
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
    if not path and stream is None:
        raise ValueError("You must input path or stream to load dotenv file.")
    try:
        if stream is None:
            stream = open(path, "r", encoding="UTF-8")
        for line in stream:
            line = line.strip()
            if not line or line[0] == "#":
                continue

            key, value = line.split("=", 1)
            key, value = key.strip(), value.strip().strip('"').strip("'")

            if key in environ and not override:
                continue

            environ[key] = value
    except Exception as error:
        if verbose:
            raise error
        return error
    finally:
        if stream:
            stream.close()
            # we're closing stream anyway, because there's no reason
            # to use it in other place if this is a stream of dotenv
            # file.


@overload
def get(key: str, *, into: Callable[[Any], T] = str) -> T: ...


@overload
def get(key: str, *, default: DT, into: Callable[[Any], T] = str) -> Union[T, DT]: ...


def get(key: str, *, default: Any = NO_DEFAULT, into: Callable[[Any], T] = str) -> Union[T, Any]:
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
    value: Any = environ.get(key, default=default)
    if value is NO_DEFAULT:
        raise KeyError(f"`{key}` cannot be found in environment")
    if value is None:
        return value
    return into(value)


load_dotenv = load
getenv = get
