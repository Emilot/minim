"""
Utility functions
=================
.. moduleauthor:: Benjamin Ye <GitHub: @bbye98>

This module contains a collection of utility functions.
"""

from . import Any, Union

try:
    import Levenshtein
    FOUND_LEVENSHTEIN = True
except ModuleNotFoundError:
    FOUND_LEVENSHTEIN = False
try:
    import numpy as np
    FOUND_NUMPY = True
except ModuleNotFoundError:
    FOUND_NUMPY = False

__all__ = ["format_multivalue", "levenshtein_ratio"]

def format_multivalue(
        value: Any, multivalue: bool, *, primary: bool = False,
        sep: Union[str, tuple[str]] = (", ", " & ")) -> Union[str, list[Any]]:
    
    """
    Format a field value based on whether multivalue for that field is 
    supported.

    Parameters
    ----------
    value : `Any`
        Field value to format.

    multivalue : `bool`
        Determines whether multivalue tags are supported. If 
        :code:`False`, the items in `value` are concatenated using the
        separator(s) specified in `sep`.

    primary : `bool`, keyword-only, default: :code:`False`
        Specifies whether the first item in `value` should be used when
        `value` is a `list` and :code:`multivalue=False`.

    sep : `str` or `tuple`, keyword-only, default: :code:`(", ", " & ")`
        Separator(s) to use to concatenate multivalue tags. If a 
        :code:`str` is provided, it is used to concatenate all values.
        If a :code:`tuple` is provided, the first :code:`str` is used to
        concatenate all values except the last, and the second 
        :code:`str` is used to append the final value. 

    Returns
    -------
    value : `Any`
        Formatted field value.
    """

    if isinstance(value, list):
        if not multivalue:
            if len(value) == 1 or primary:
                return value[0]
            elif isinstance(value[0], str):
                if isinstance(sep, str):
                    return sep.join(value)
                return f"{sep[0].join(value[:-1])}{sep[1]}{value[-1]}"
    elif multivalue:
        return [value]
    return value

def levenshtein_ratio(
        base: str, values: Union[str, list[str]]
    ) -> Union[float, list[float], "np.ndarray[float]"]:

    """
    Compute the Levenshtein ratio, a measure of similarity, for
    string(s) with respect to a reference string.

    Parameters
    ----------
    base : `str`
        Reference string.

    values : `str` or `list`
        String(s) to compare with `base`.

    Returns
    -------
    ratios : `float`, `list`, or `numpy.ndarray`
        Levenshtein ratio(s). If `values` is a `str`, a `float` is
        returned. If `values` is a `list`, a `numpy.ndarray` is returned
        if NumPy is installed; otherwise, a `list` is returned.
    """

    if not FOUND_LEVENSHTEIN:
        emsg = ("The Levenshtein module was not found, so "
                "minim.utility.levenshtein_ratio() is unavailable.")
        raise ImportError(emsg)
    
    if isinstance(values, str):
        return Levenshtein.ratio(base, values)
    gen = (Levenshtein.ratio(base, v) for v in values)
    if FOUND_NUMPY:
        return np.fromiter(gen, dtype=float, count=len(values))
    return list(gen)