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
        # self.latex_trans = {
        #     "bar": "|",
        #     "natural": "\\mathbb{N}",
        #     "rational": "\\mathbb{Q}",
        #     "real": "\\mathbb{R}",
        #     "integer": "\\mathbb{Z}",
        #     "complex": "\\mathbb{C}",
        #     "plus": "+",
        #     "minus": "-",
        #     "frac": "/",
        #     "<": "<",
        #     "lt": "<",
        #     ">": ">",
        #     "gt": ">",
        #     "equal": "=",
        #     "left": "(",
        #     "left_square": "[",
        #     "left_curly": "\\{",
        #     "left_curly_semicolon": "",
        #     "right": ")",
        #     "right_square": "]",
        #     "right_curly": "\\}",
        #     "right_curly_semicolon": "",
        #     "and": "and",
        #     "or": "or",
        #     "if": "if",
        #     "comma": ",",
        #     "underscore": "\\_",
        #     "superflex": "\\^",
        #     "squote": "'"
        # }
        formatted_left_parenthesis = "|".join(
            ["\\(", "\\[", "\\{", "langle", "<<"]
        )
        formatted_right_parenthesis = "|".join(
            ["\\)", "\\]", "\\}", "rangle", ">>"]
        )
        self.start_end_par_pattern = re.compile(
            r"^(?:\\left(?:(?:\\)?({})))"
            r"(.*?)"
            r"(?:\\right(?:(?:\\)?({})))$".format(
                formatted_left_parenthesis, formatted_right_parenthesis,
            )
        )
        logger_func = logging.info
        if not log:

            def logger_func(x):
                return x

        self._logger = Log(logger_func=logger_func)

    def _log(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            self = args[0]
            return self._logger.__call__(f)(*args, **kwargs)

        return decorator

    def _concat(self, s):
        return '"' + s + '"'

    @_log
    def remove_parenthesis(self, s: str):
        return re.sub(self.start_end_par_pattern, r"\2", s)

    @_log
    def exp_par(self, items):
        left = left_parenthesis[self._concat(items[0])]
        right = right_parenthesis[self._concat(items[-1])]
        # if "latex" in lpar:
        #     left = "\\left\\" + lpar[2] + " "
        # else:
        #     left = "\\left" + ("." if "semicolon" in lpar else "") + \
        #         self.latex_trans["_".join(lpar[1:])]
        # if "latex" in rpar:
        #     right = "\\right\\" + rpar[2] + " "
        # else:
        #     right = "\\right" + \
        #         ("." if "semicolon" in rpar else "") + \
        #         self.latex_trans["_".join(rpar[1:])]
        return "\\left" + left + ", ".join(items[1:-1]) + "\\right" + right

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
        if self._concat(items[0]) in smb:
            return smb[self._concat(items[0])]
        else:
            return items[0].value

    @_log
    def exp_unary(self, items):
        unary = unary_functions[self._concat(items[0])]
        items[1] = self.remove_parenthesis(items[1])
        if unary == "norm":
            return "\\left \\lVert " + items[1] + " \\right \\rVert"
        elif unary == "abs":
            return "\\left \\mid " + items[1] + " \\right \\mid"
        elif unary == "floor":
            return "\\left \\lfloor " + items[1] + " \\right \\rfloor"
        elif unary == "ceil":
            return "\\left \\lceil " + items[1] + " \\right \\rceil"
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

    # @_log
    # def var(self, items):
    #     return items[0].value

    # @_log
    # def num(self, items):
    #     return items[0].value

    # @_log
    # def misc_symbols(self, items):
    #     misc = items[0].data.split("_")
    #     if "latex" in misc:
    #         return '\\' + misc[2]
    #     else:
    #         return self.latex_trans[misc[1]]

    # @_log
    # def operation_symbols(self, items):
    #     op = items[0].data.split("_")
    #     if "latex" in op:
    #         return '\\' + op[2]
    #     else:
    #         return self.latex_trans[op[1]]

    # @_log
    # def logical_symbols(self, items):
    #     log = items[0].data.split("_")
    #     if "latex" in log:
    #         return "\\" + log[2]
    #     else:
    #         return "\\text{" + self.latex_trans[log[1]] + "}"

    # @_log
    # def relation_symbols(self, items):
    #     rel = items[0].data.split("_")
    #     if "latex" in rel:
    #         return "\\" + rel[2]
    #     else:
    #         return self.latex_trans[rel[1]]

    # @_log
    # def function_symbols(self, items):
    #     func = items[0].data.split("_")
    #     if "latex" in func:
    #         return "\\" + func[2]
    #     else:
    #         return func[1]

    # @_log
    # def greek_letters(self, items):
    #     greek = items[0].data.split("_")
    #     if "upper" in greek:
    #         return "\\" + greek[3].capitalize()
    #     else:
    #         return "\\" + greek[2]

    # @_log
    # def arrows(self, items):
    #     arr = items[0].data.split("_")
    #     return "\\" + arr[2]

    # @_log
    # def derivatives(self, items):
    #     return items[0].value

    # @_log
    # def latex_smb(self, items):
    #     return smb[self._concat(items[0])]

    @_log
    def punct(self, items):
        return items[0]

    @_log
    def exp(self, items):
        return " ".join(items)


class ASCIIMath2Tex(object):
    def __init__(
        self,
        grammar,
        *args,
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
            grammar, *args, parser=parser, lexer=lexer, cache=True, **kwargs
        )

    def asciimath2tex(self, s: str, pprint=False):
        if not self.inplace:
            parsed = self.parser.parse(s)
            if pprint:
                print(parsed.pretty())
            return self.transformer.transform(parsed)
        else:
            return self.parser.parse(s)