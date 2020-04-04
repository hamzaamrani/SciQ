from lark import Lark, Transformer, Discard, Tree, Token, v_args
from lark.exceptions import VisitError, GrammarError
from itertools import chain, islice
from functools import wraps
from log import Log, flatten
from const import *
import re
import sys
import logging

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)
"""
    Search regex: (\s*)(\S+(\s\S+)?)(\s*)
    Replace regex: $1"\"$2\"": "$2",
"""


class LatexTransformer(Transformer):
    def __init__(self, log=True, visit_tokens=False):
        super(LatexTransformer, self).__init__(visit_tokens=visit_tokens)
        formatted_left_parenthesis = "|".join(
            ["\\(", "\\[", "\\{", "langle", "<<"]
        )
        formatted_right_parenthesis = "|".join(
            ["\\)", "\\]", "\\}", "rangle", ">>"]
        )
        self.left_right_pattern = re.compile(r"(\\right|\\left)")
        self.start_end_par_pattern = re.compile(
            r"^(?:\\left(?:(?:\\)?({})))"
            r"(.*?)"
            r"(?:\\right(?:(?:\\)?({})))$".format(
                formatted_left_parenthesis, formatted_right_parenthesis,
            )
        )
        self._logger_func = logging.info
        if not log:
            self._logger_func = lambda x: x
        self._logger = Log(logger_func=self._logger_func)

    def _log(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            self = args[0]
            return self._logger.__call__(f)(*args, **kwargs)

        return decorator

    def _concat(self, s):
        return '"' + s + '"'

    @_log
    def _check_mat(self, s):
        rows = 0
        cols = 0
        max_cols = 0
        par_stack = []
        transitions = 0
        for c in s:
            if c == "[":
                par_stack.append(c)
            elif c == "]":
                if len(par_stack) == 0:
                    logging.info("WRONG: UNMATCHED PARS")
                    return False
                else:
                    par_stack.pop()
                if max_cols == 0 and cols > 0:
                    max_cols = cols
                elif len(par_stack) == 0:
                    if max_cols != cols:
                        logging.info("WRONG: COLS DIFFER")
                        return False
                if len(par_stack) == 0:
                    transitions = transitions + 1
                cols = 0
            elif c == ",":
                if len(par_stack) == 1 and par_stack[-1] == "[":
                    cols = cols + 1
                elif len(par_stack) == 0:
                    rows = rows + 1
                    if transitions != rows:
                        logging.info(
                            "WRONG: NO OPEN-CLOSE PAR BETWEEN TWO COMMAS"
                        )
                        return False
        if len(par_stack) != 0:
            logging.info("WRONG: UNMATCHED PARS")
            return False
        elif rows == 0 or transitions - rows != 1:
            logging.info("WRONG: MISSING COMMA OR EMPTY ROW")
            return False
        return True

    @_log
    def _get_mat(self, s):
        s = re.sub(self.left_right_pattern, "", s)
        stack_par = []
        mat = ""
        for c in s:
            if c == "[":
                stack_par.append(c)
                if len(stack_par) > 1:
                    mat = mat + "\\left" + c
            elif c == "]":
                stack_par.pop()
                if len(stack_par) > 0:
                    mat = mat + "\\right" + c
            elif c == "," and len(stack_par) == 1:
                mat = mat + " & "
            elif c == "," and len(stack_par) == 0:
                mat = mat + " \\\\ "
            else:
                if len(stack_par) > 0:
                    mat = mat + c
        return mat

    @_log
    def remove_parenthesis(self, s: str):
        return re.sub(self.start_end_par_pattern, r"\2", s)

    @_log
    def exp_par(self, items):
        mat = False
        if items[1].startswith("\\left"):
            if self._check_mat(items[1]):
                mat = True
                s = self._get_mat(items[1])
            else:
                s = ", ".join(items[1:-1])
        else:
            s = ", ".join(items[1:-1])
        lpar = left_parenthesis[self._concat(items[0])]
        rpar = right_parenthesis[self._concat(items[-1])]
        if lpar == "\\langle":
            left = "\\left" + lpar + " "
        elif lpar == "{:":
            left = "\\left."
        else:
            left = "\\left" + lpar
        if rpar == "\\rangle":
            right = " \\right" + rpar
        elif rpar == ":}":
            right = "\\right."
        else:
            right = "\\right" + rpar
        return (
            left
            + ("\\begin{matrix}" + s + "\\end{matrix}" if mat else s)
            + right
        )

    @_log
    def exp_mat(self, items, mat_type="pmatrix"):
        if items == [] or items != [] and items[0] == "":
            return "".join(matrix2par[mat_type])
        else:
            return (
                "\\begin{"
                + mat_type
                + "}"
                + (items[0] if items != [] else "\\null")
                + "\\end{"
                + mat_type
                + "}"
            )

    @_log
    def exp_cmat(self, items):
        return self.exp_mat(items, mat_type="Bmatrix")

    @_log
    def exp_bmat(self, items):
        return self.exp_mat(items, mat_type="bmatrix")

    @_log
    def exp_vmat(self, items):
        return self.exp_mat(items, mat_type="vmatrix")

    @_log
    def exp_nmat(self, items):
        return self.exp_mat(items, mat_type="Vmatrix")

    @_log
    def exp_pmat(self, items):
        return self.exp_mat(items)

    @_log
    def exp_system(self, items):
        return re.sub(r"(?<!&)=", "&=", self.exp_mat(items, mat_type="cases"))

    @_log
    def csl(self, items):
        return ",".join(items)

    @_log
    def csl_mat(self, items):
        return " \\\\ ".join(items)

    @_log
    def icsl_mat(self, items):
        if items == []:
            return "\\null"
        return " & ".join(items)

    @_log
    def exp_frac(self, items):
        return "\\frac{" + items[0] + "}{" + items[1] + "}"

    @_log
    def exp_under(self, items):
        items[1] = self.remove_parenthesis(items[1])
        return items[0] + "_{" + items[1] + "}"

    @_log
    def exp_super(self, items):
        items[1] = self.remove_parenthesis(items[1])
        return items[0] + "^{" + items[1] + "}"

    @_log
    def exp_interm(self, items):
        return items[0]

    @_log
    def exp_under_super(self, items):
        items[1] = self.remove_parenthesis(items[1])
        items[2] = self.remove_parenthesis(items[2])
        return items[0] + "_{" + items[1] + "}^{" + items[2] + "}"

    @_log
    def symbol(self, items):
        return smb[self._concat(items[0])]

    @_log
    def const(self, items):
        return items[0].value

    @_log
    def exp_unary(self, items):
        unary = unary_functions[self._concat(items[0])]
        items[1] = self.remove_parenthesis(items[1])
        if unary == "norm":
            return "\\left\\lVert " + items[1] + " \\right\\rVert"
        elif unary == "abs":
            return "\\left\\mid " + items[1] + " \\right\\mid"
        elif unary == "floor":
            return "\\left\\lfloor " + items[1] + " \\right\\rfloor"
        elif unary == "ceil":
            return "\\left\\lceil " + items[1] + " \\right\\rceil"
        else:
            return unary + "{" + items[1] + "}"

    @_log
    def exp_binary(self, items):
        binary = binary_functions[self._concat(items[0])]
        items[1] = self.remove_parenthesis(items[1])
        items[2] = self.remove_parenthesis(items[2])
        if binary == "\\sqrt":
            return binary + "[" + items[1] + "]" + "{" + items[2] + "}"
        else:
            return binary + "{" + items[1] + "}" + "{" + items[2] + "}"

    @_log
    def q_str(self, items):
        return "\\text{" + items[0] + "}"

    @_log
    def exp(self, items):
        return " ".join(items)


class ASCIIMath2Tex(object):
    def __init__(
        self,
        grammar,
        *args,
        cache=False,
        inplace=False,
        parser="lalr",
        lexer="contextual",
        transformer=LatexTransformer(),
        **kwargs
    ):
        self.inplace = inplace
        self.grammar = grammar
        self.transformer = transformer
        if inplace:
            kwargs.update({"transformer": transformer})
        self.parser = Lark(
            grammar, *args, parser=parser, lexer=lexer, cache=cache, **kwargs
        )

    def asciimath2tex(self, s: str, pprint=False):
        if not self.inplace:
            parsed = self.parser.parse(s)
            if pprint:
                print(parsed.pretty())
            return self.transformer.transform(parsed)
        else:
            return self.parser.parse(s)
