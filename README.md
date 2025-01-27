# dotenv
A minimal module for working with dotenv files.

## Examples
```py
>>> from dotenv import load_dotenv, getenv
>>> load_dotenv()
```

Load the dotenv file from `.env`. If any error occurs, nothing will happen.
However, if the value is being retrieved from a `load_dotenv()` call:

```py
>>> env = load_dotenv()
>>> print(env)  # `None` if all is alright.
>>> print(env)  # In case of `Exception`, Houston, we have a problem.

>>> load_dotenv(verbose=True)
```

In this case, if there's an exception, the function will raise it.

```py
>>> key: str = getenv("API_KEY")
```

`getenv()` returns the value from the environment by the key if it exists.
If the key doesn't exist, `getenv()` will raise a `KeyError`.

To avoid this exception:

```py
>>> max_connections: Union[str, int] = getenv("MAX_CONNECTIONS", default=100)
```

You can pass any value as the `default` argument, which prevents the exception!

However, as you can see, `max_connections` might be `str`, which could be problematic.
To avoid this, `getenv()` provides a way to cast the result:

```py
>>> max_connections: int = getenv("MAX_CONNECTIONS", into=int)
```
Now `max_connections` will be of type `int`.

# Installation
```sh
> pip install git+https://github.com/stefanlight8/dotenv
```

## Requirements
- Python 3.6<
