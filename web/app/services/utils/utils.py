import logging
from collections.abc import Iterable

from flask import request

from flask_jwt_extended import get_jwt_identity
from flask_limiter.util import get_remote_address

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)

def custom_key_func():
    if request.headers.getlist("X-Forwarded-For"):
        logging.info(request.headers.getlist("X-Forwarded-For"))
        return request.headers.getlist("X-Forwarded-For")[0]
    else:
        return get_remote_address()

def get_limit():
    appid = request.args.get("appid")
    if appid is None:
        return "50 per hour;200 per day"
    else:
        return "200 per hour;800 per day"


def exempt_limit():
    if (
        get_jwt_identity() is not None  # Buy unlimited API usage
        and request.args.get("appid") is not None
    ):
        return True
    else:
        return False


def concat(s: str):
    return '"' + s + '"'


def flatten(l):
    """Flatten a list (or other iterable) recursively"""
    for el in l:
        if isinstance(el, Iterable) and not isinstance(el, str):
            for sub in flatten(el):
                yield sub
        else:
            yield el


class UtilsMat(object):
    """Static class to check matrix-structure of a string and returns its
    LaTeX translation.

    It performs two opertions:
    1) Given a string, it checks if the string could be a rendered as LaTeX
       matrix. A correct matrix structure is:
       L [... (, ...)*], [... (, ...)*] (, [... (, ...)*])* R or
       L (... (, ...)*), (... (, ...)*) (, (... (, ...)*))* R, where L and R
       are all the possible left and right parenthesis defined by the parser;
       '[... (, ...)*]' or '(... (, ...)*)' identifies a row in the matrix
       which can be made by one or more columns, comma separated.
       In order to be considered as a matrix, the string must contain at
       leat two rows and every rows must contain the same number of columns
    2) Given a correctly matrix-like string, it returns the LaTeX translation:
       col (& col)* \\\\ col (& col)* (\\\\ col (& col)*)*
    """

    @classmethod
    def get_row_par(cls, s):
        """Given a string, it returns the first index i such that the char in
        position i of the string is a left parenthesis, '(' or '[', and the
        open-close parenthesis couple, needed to identify matrix
        rows in the string.

        Parameters:
        - s: str

        Returns:
        - i: int, [left_par, right_par]: list
        """

        for i, c in enumerate(s):
            if c == "[" or c == "(":
                return i, ["[", "]"] if c == "[" else ["(", ")"]
        return -1, []

    @classmethod
    def check_mat(cls, s):
        """Given a string, runs a matrix-structure check.
        Returns True if the string s has a matrix-structure-like,
        False otherwise. It returns also the row delimiters.

        Parameters:
        - s: str

        Returns:
        - b: bool
        - [l_par, r_par]: list
        """

        rows = 0
        cols = 0
        max_cols = 0
        par_stack = []
        transitions = 0
        i, row_par = cls.get_row_par(s)
        if i != -1 or row_par == []:
            for c in s[i:]:
                # c is a left par
                if c == row_par[0]:
                    if transitions != rows:
                        logging.info("ROW WITHOUT COMMA")
                        return False, []
                    par_stack.append(c)
                # c is a right par
                elif c == row_par[1]:
                    if len(par_stack) == 0:
                        logging.info("UNMATCHED PARS")
                        return False, []
                    else:
                        par_stack.pop()
                    if len(par_stack) == 0:
                        transitions = transitions + 1
                        if transitions == 1 and max_cols == 0 and cols > 0:
                            max_cols = cols
                        elif max_cols != cols:
                            logging.info("COLS DIFFER")
                            return False, []
                        cols = 0
                elif c == ",":
                    if len(par_stack) == 1 and par_stack[-1] == row_par[0]:
                        cols = cols + 1
                    elif len(par_stack) == 0:
                        # If the comma is not at the and of the string
                        # count another row
                        rows = rows + 1
                        if transitions - rows != 0:
                            logging.info(
                                "NO OPEN-CLOSE PAR BETWEEN TWO COMMAS"
                            )
                            return False, []
            if len(par_stack) != 0:
                logging.info("UNMATCHED PARS")
                return False, []
            elif transitions < 2:
                logging.info("NOT ENOUGH ROWS: AT LEAST 2")
                return False, []
            elif rows == 0 or transitions - rows > 1:
                logging.info("MISSING COMMA OR EMPTY ROW")
                return False, []
            return True, row_par
        else:
            return False, []

    @classmethod
    def get_mat(cls, s, row_par=["[", "]"]):
        """Given a known matrix-structured string, translate it into the
        matrix LaTeX format.

        Parameters:
        - s: str
        - max_cols: int. How many columns per rows
        - row_par: list. Row delimiters

        Returns:
        - mat: str
        """

        i = 0
        empty_col = True
        stack_par = []
        mat = ""
        if row_par != []:
            while i < len(s):
                c = s[i]
                if c == row_par[0]:
                    stack_par.append(c)
                    if len(stack_par) > 1:
                        mat = mat + c
                elif c == row_par[1]:
                    stack_par.pop()
                    if len(stack_par) > 0:
                        mat = mat + c
                    else:
                        if empty_col:
                            mat = mat + "\\null"
                        empty_col = True
                elif c == ",":
                    if len(stack_par) == 1:
                        mat = mat + (" & " if not empty_col else "\\null & ")
                    elif len(stack_par) == 0:
                        mat = mat + " \\\\ "
                    empty_col = True
                else:
                    # Does not include \\left in the result string
                    if len(stack_par) == 0 and s[i : i + 5] == "\\left":
                        i = i + 4
                    # Does not include \\right in the result string
                    elif (
                        len(stack_par) == 1
                        and s[i : i + 7] == "\\right" + row_par[1]
                    ):
                        i = i + 5
                    else:
                        if not c.isspace():
                            empty_col = False
                        mat = mat + c
                i = i + 1
            return mat
        else:
            return s


if __name__ == "__main__":
    s = UtilsMat.get_mat("\\left[,\\right] , \\left[,\\right]")
    print(s)
