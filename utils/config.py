from decouple import config


def get_config(key: str, default=None, cast=None):
    """
    Retrieves configuration values from environment variables or .env file,
     casting them to the specified type if necessary.

    Args:
        key (str): The configuration key to retrieve.
        default (Any): The default value if the configuration key isn't found.
        cast (Callable, optional): A function to cast the value of the environment variable.
                                   If not provided, the raw string will be returned.

    Returns:
        Any: The value of the environment variable, optionally cast to a specified type.
    """
    if cast is not None:
        return config(key, default=default, cast=cast)
    else:
        return config(key, default=default)
