from typing import Union, Optional, Iterable, TypeVar, List


T = TypeVar("T")


def first(a: Iterable[T], n: Optional[int] = 1) -> Union[T, List[T]]:
    """
    This method returns the first N entities in a list of entities.

    Parameters
    ----------
    a : Iterable[T]
        An iterable of entities
    n : int, optional
        The number of first elements to return from the list, by default 1

    Returns
    -------
    T|List[T]
        The first entity or a list of the first N entities
    """
    if not a:
        return a
    elif n == 1:
        return list(a)[0]
    else:
        return list(a)[:n]


def last(a: Iterable[T], n: Optional[int] = 1) -> Union[T, List[T]]:
    """
    This method returns the last N entities in a list of entities.

    Parameters
    ----------
    a : Iterable[T]
        An iterable of entities
    n : int, optional
        The number of last elements to return from the list, by default 1

    Returns
    -------
    T|List[T]
        The first entity or a list of the last N entities
    """
    first = list(a)[-1] if n == 1 else list(a)[:-n]
    return first


def sort(a: Iterable[T], text: str) -> Iterable[T]:
    """
    This method sorts an iterable of entities based on a given text attribute.

    Parameters
    ----------
    a : Iterable[T]
        An iterable of entities
    text : str
        The attribute to sort the entities by expressed as a text string

    Returns
    -------
    T|List[T]
        The first entity or a list of the last N entities
    """
    return sorted(a, key=lambda x: getattr(x, text))


def filter(a: Iterable[T], **kwargs) -> Iterable[T]:
    """
    This method filters an iterable of entities based on a given keywords.

    Parameters
    ----------
    a : Iterable[T]
        An iterable of entities
    kwargs : dict
        Arbitrary keyword arguments to filter the list of entities by.
        These keywords are expected to be attributes of the entities.

    Returns
    -------
    T|List[T]
        The first entity or a list of the last N entities
    """
    return [
        x
        for x in a
        if all(
            hasattr(x, key) and getattr(x, key) == value
            for key, value in kwargs.items()
        )
    ]
