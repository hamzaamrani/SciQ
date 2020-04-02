from lark import Lark, Transformer, Discard, Tree, Token, v_args
from lark.exceptions import VisitError, GrammarError
from itertools import chain
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


def alias_string(mapping: dict, init=False, alias=True, prefix=""):
    mapping = list(mapping.items())
    s = (
        "|"
        if init
        else ""
        + mapping[0][0]
        + (
            " -> " + (prefix + "_" if prefix != "" else "") + mapping[0][1]
            if alias
            else ""
        )
    )
    for k, v in mapping[1:]:
        s = (
            s
            + "\n\t| "
            + k
            + (
                " -> " + (prefix + "_" if prefix != "" else "") + v
                if alias
                else ""
            )
        )
    return s


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
        return "\\left" + left + " " + items[1] + " \\right" + right

    @_log
    def exp_mat(self, items, mat_type="pmatrix"):
        if (items != []) & (items[0] != ""):
            return (
                "\\begin{"
                + mat_type
                + "}"
                + (items[0] if items != [] else "\\null")
                + "\\end{"
                + mat_type
                + "}"
            )
        else:
            return ""

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

    @_log
    def var(self, items):
        return items[0].value

    @_log
    def num(self, items):
        return items[0].value

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

    @_log
    def derivatives(self, items):
        return items[0].value

    @_log
    def latex_smb(self, items):
        return smb[self._concat(items[0])]

    @_log
    def exp(self, items):
        return " ".join(items)


sys.setrecursionlimit(1024)


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
            grammar, *args, parser=parser, lexer=lexer, **kwargs
        )

    def asciimath2tex(self, s: str, pprint=False):
        if not self.inplace:
            parsed = self.parser.parse(s)
            if pprint:
                print(parsed.pretty())
            return self.transformer.transform(parsed)
        else:
            return self.parser.parse(s)


if __name__ == "__main__":
    asciimath_grammar = r"""
        start: i+ -> exp
        csl: start ("," start)* ","?                    // csl = Comma Separated List
        csl_mat: icsl_mat ("," icsl_mat)* ","?          // csl_mat = Comma Separated List for MATrices
        icsl_mat: "[" start? ("," start)* ","? "]"      // icsl_mat = Internal Comma Separated List for MATrices
        i: s -> exp_interm
            | s "/" s -> exp_frac
            | s "_" s -> exp_under
            | s "^" s -> exp_super
            | s "_" s "^" s -> exp_under_super
        s: _l csl? _r -> exp_par
            | "[" csl_mat? "]" -> exp_bmat
            | "(" csl_mat? ")" -> exp_pmat
            | "(" csl_mat? ")" -> exp_pmat
            | "{{" csl_mat? "}}" -> exp_cmat
            | "|" csl_mat? "|" -> exp_vmat
            | "||" csl_mat? "||" -> exp_nmat
            | "{{" csl_mat? ")" -> exp_system
            | _u s -> exp_unary
            | _b s s -> exp_binary
            | _qs -> q_str
            | _c -> symbol
        _c: LETTER
        | NUMBER
        | /d[A-Za-z]/
        | _ls
        !_l: {} // left parenthesis
        !_r: {} // right parenthesis
        !_b: {} // binary functions
        !_u: {} // unary functions
        !_ls: {} // LaTeX Symbols
        _qs: "\"" /(?<=").+(?=")/ "\"" // Quoted String
        %import common.WS
        %import common.LETTER
        %import common.NUMBER
        %ignore WS
    """.format(
        alias_string(left_parenthesis, alias=False, prefix="par"),
        alias_string(right_parenthesis, alias=False, prefix="par"),
        alias_string(binary_functions, alias=False, prefix="binary"),
        alias_string(unary_functions, alias=False, prefix="unary"),
        alias_string(smb, alias=False, prefix="misc"),
        # alias_string(operation_symbols, prefix="op"),
        # alias_string(relation_symbols, prefix="rel"),
        # alias_string(logical_symbols, prefix="logical"),
        # alias_string(function_symbols, prefix="func"),
        # alias_string(greek_letters, prefix="greek"),
        # alias_string(arrows, prefix="arrow")
    )
    parser = ASCIIMath2Tex(
        asciimath_grammar, inplace=False, transformer=LatexTransformer()
    )
    text = ""
    text = (
        text
        + """
        frac{root(5)(a iff c)}
        {
            dstyle int(
                sqrt(x_2^3.14)
                X
                root(langle x,t rangle) (max(dot z,4)) +
                min(x,y,"time",bbb C)
            ) dg
        }
    """
    )
    text = (
        text
        + """
        uuu_{2(x+1)=1)^{n}
        min{
                2x|x^{y+2} in bbb(N) wedge arccos root(3}(frac{1}{3x}) < i rarr Omega < b, 5=x
        }
    """
    )
    text = (
        text
        + """
        [[[[v, c], [a,b]]]]
        (((x+2), (int e^{x^2} dx)))
        oint (lfloor x rfloor quad) dx
    """
    )
    text = text + """lim_(N->oo) sum_(i=0)^N int_0^1 f(x)dx"""
    text = text + """||[2 x + 17 y = 23],[y = int_{0}^{x} t dt]||"""
    text = (
        text
        + """floor frac "Time" (A nn (bbb(N) | f'(x) = dx/dy | |><| (D setminus (B uu C))))"""
    )
    text = text + """(1,2,3)"""
    text = (
        text
        + """e^{{([2 x + 17 y = 23, [1]],[y = dstyle int_{0}^{x} t dt],[y = dstyle int_{0}^{x} t dt])}}"""
    )
    text = text + """([1,2], )"""
    print(parser.asciimath2tex(text, pprint=True))
