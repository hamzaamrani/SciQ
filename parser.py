from lark import (Lark, Transformer, Discard, Tree,
                  Token, v_args)
from lark.exceptions import VisitError, GrammarError
from itertools import chain
from functools import wraps
from log import Log, flatten
import re
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
"""
    Search regex: (\s*)(\S+(\s\S+)?)(\s*)
    Replace regex: $1"\"$2\"": "$2",
"""


def alias_string(mapping: dict, init=False, alias=True, prefix=""):
    mapping = list(mapping.items())
    s = "|" if init else "" + \
        mapping[0][0] + (" -> " +
                         (prefix + "_" if prefix != "" else "") + mapping[0][1] if alias else "")
    for k, v in mapping[1:]:
        s = s + "\n\t| " + k + (" -> " + (prefix + "_" if prefix !=
                                          "" else "") + v if alias else "")
    return s


binary_functions = {
    "\"frac\"": "latex_frac", "\"root\"": "latex_sqrt",
    "\"stackrel\"": "latex_stackrel", "\"overset\"": "latex_overset",
    "\"underset\"": "latex_underset", "\"color\"": "latex_textcolor", }

unary_functions = {
    "\"sqrt\"": "latex_sqrt",
    "\"text\"": "latex_textrm",
    "\"abs\"": "abs",
    "\"floor\"": "floor",
    "\"ceil\"": "ceil",
    "\"norm\"": "norm",
    "\"ubrace\"": "latex_underbrace",
    "\"underbrace\"": "latex_underbrace",
    "\"obrace\"": "latex_overbrace",
    "\"overbrace\"": "latex_overbrace",
    "\"cancel\"": "latex_cancel",
    "\"bb\"": "latex_boldsymbol",
    "\"bbb\"": "latex_mathbb",
    "\"cc\"": "latex_mathcal",
    "\"tt\"": "latex_texttt",
    "\"fr\"": "latex_mathfrak",
    "\"sf\"": "latex_textsf",
    "\"ul\"": "latex_underline",
    "\"underline\"": "latex_underline",
    "\"bar\"": "latex_overline",
    "\"overline\"": "latex_overline",
    "\"hat\"": "latex_hat",
    "\"vec\"": "latex_vec",
    "\"dot\"": "latex_dot",
    "\"ddot\"": "latex_ddot",
}

operation_symbols = {
    "\"+\"": "plus",
    "\"*\"": "latex_cdot",
    "\"-\"": "minus",
    "\"cdot\"": "latex_cdot",
    "\"**\"": "latex_ast",
    "\"ast\"": "latex_ast",
    "\"***\"": "latex_star",
    "\"star\"": "latex_star",
    "\"//\"": "frac",
    "\"\\\\\"": "latex_setminus",
    "\"setminus\"": "latex_setminus",
    "\"xx\"": "latex_times",
    "\"times\"": "latex_times",
    "\"-:\"": "latex_div",
    "\"div\"": "latex_div",
    "\"|><\"": "latex_ltimes",
    "\"ltimes\"": "latex_ltimes",
    "\"><|\"": "latex_rtimes",
    "\"rtimes\"": "latex_rtimes",
    "\"|><|\"": "latex_bowtie",
    "\"bowtie\"": "latex_bowtie",
    "\"@\"": "latex_circ",
    "\"circ\"": "latex_circ",
    "\"o+\"": "latex_oplus",
    "\"oplus\"": "latex_oplus",
    "\"ox\"": "latex_otimes",
    "\"otimes\"": "latex_otimes",
    "\"o.\"": "latex_odot",
    "\"odot\"": "latex_odot",
    "\"sum\"": "latex_sum",
    "\"prod\"": "latex_prod",
    "\"^^\"": "latex_wedge",
    "\"wedge\"": "latex_wedge",
    "\"^^^\"": "latex_bigwedge",
    "\"bidwedge\"": "latex_bidwedge",
    "\"vv\"": "latex_vee",
    "\"vee\"": "latex_vee",
    "\"vvv\"": "latex_bigvee",
    "\"bigvee\"": "latex_bigvee",
    "\"nn\"": "latex_cap",
    "\"cap\"": "latex_cap",
    "\"nnn\"": "latex_bigcap",
    "\"bigcap\"": "latex_bigcap",
    "\"uu\"": "latex_cup",
    "\"cup\"": "latex_cup",
    "\"uuu\"": "latex_bigcup",
    "\"bigcup\"": "latex_bigcup",
}

logical_symbols = {
    "\"and\"": "and",
    "\"or\"": "or",
    "\"not\"": "latex_neg",
    "\"neg\"": "latex_neg",
    "\"=>\"": "latex_implies",
    "\"implies\"": "latex_implies",
    "\"if\"": "if",
    "\"<=>\"": "latex_iff",
    "\"iff\"": "latex_iff",
    "\"AA\"": "latex_forall",
    "\"forall\"": "latex_forall",
    "\"EE\"": "latex_exists",
    "\"exists\"": "latex_exists",
    "\"_|_\"": "latex_bot",
    "\"bot\"": "latex_bot",
    "\"TT\"": "latex_top",
    "\"top\"": "latex_top",
    "\"|--\"": "latex_vdash",
    "\"vdash\"": "latex_vdash",
    "\"|==\"": "latex_models",
    "\"models\"": "latex_models",
}

relation_symbols = {
    "\"=\"": "equal",
    "\"!=\"": "latex_ne",
    "\"ne\"": "latex_ne",
    "\"<\"": "lt",
    "\"lt\"": "lt",
    "\">\"": "gt",
    "\"gt\"": "gt",
    "\"<=\"": "latex_le",
    "\"le\"": "latex_le",
    "\">=\"": "latex_ge",
    "\"ge\"": "latex_ge",
    "\"-<\"": "latex_prec",
    "\"prec\"": "latex_prec",
    "\"-<=\"": "latex_preceq",
    "\"preceq\"": "latex_preceq",
    "\">-\"": "latex_succ",
    "\"succ\"": "latex_succ",
    "\">-=\"": "latex_succeq",
    "\"succeq\"": "latex_succeq",
    "\"in\"": "latex_in",
    "\"!in\"": "latex_notin",
    "\"notin\"": "latex_notin",
    "\"sub\"": "latex_subset",
    "\"subset\"": "latex_subset",
    "\"sup\"": "latex_supset",
    "\"supset\"": "latex_supset",
    "\"sube\"": "latex_subseteq",
    "\"subseteq\"": "latex_subseteq",
    "\"supe\"": "latex_supseteq",
    "\"supseteq\"": "latex_supseteq",
    "\"-=\"": "latex_equiv",
    "\"equiv\"": "latex_equiv",
    "\"~=\"": "latex_cong",
    "\"cong\"": "latex_cong",
    "\"~~\"": "latex_approx",
    "\"approx\"": "latex_approx",
    "\"prop\"": "latex_propto",
    "\"propto\"": "latex_propto",
}

function_symbols = {
    "\"sin\"": "latex_sin",
    "\"cos\"": "latex_cos",
    "\"tan\"": "latex_tan",
    "\"sec\"": "latex_sec",
    "\"csc\"": "latex_csc",
    "\"cot\"": "latex_cot",
    "\"arcsin\"": "latex_arcsin",
    "\"arccos\"": "latex_arccos",
    "\"arctan\"": "latex_arctan",
    "\"sinh\"": "latex_sinh",
    "\"cosh\"": "latex_cosh",
    "\"tanh\"": "latex_tanh",
    "\"sech\"": "latex_sech",
    "\"csch\"": "latex_csch",
    "\"coth\"": "latex_coth",
    "\"exp\"": "latex_exp",
    "\"log\"": "latex_log",
    "\"ln\"": "latex_ln",
    "\"det\"": "latex_det",
    "\"dim\"": "latex_dim",
    "\"mod\"": "latex_mod",
    "\"gcd\"": "latex_gcd",
    "\"lcm\"": "latex_lcm",
    "\"lub\"": "latex_lub",
    "\"glb\"": "latex_glb",
    "\"min\"": "latex_min",
    "\"max\"": "latex_max",
    "\"lim\"": "latex_lim",
    "\"dstyle\"": "latex_displaystyle",
    "\"f\"": "f",
    "\"g\"": "g"
}

greek_letters = {
    "\"alpha\"": "latex_alpha",
    "\"beta\"": "latex_beta",
    "\"gamma\"": "latex_gamma",
    "\"Gamma\"": "latex_upper_gamma",
    "\"delta\"": "latex_delta",
    "\"Delta\"": "latex_upper_delta",
    "\"epsilon\"": "latex_epsilon",
    "\"varepsilon\"": "latex_varepsilon",
    "\"zeta\"": "latex_zeta",
    "\"eta\"": "latex_eta",
    "\"theta\"": "latex_theta",
    "\"Theta\"": "latex_upper_theta",
    "\"vartheta\"": "latex_vartheta",
    "\"iota\"": "latex_iota",
    "\"kappa\"": "latex_kappa",
    "\"lambda\"": "latex_lambda",
    "\"Lambda\"": "latex_upper_lambda",
    "\"mu\"": "latex_mu",
    "\"nu\"": "latex_nu",
    "\"xi\"": "latex_xi",
    "\"Xi\"": "latex_upper_xi",
    "\"pi\"": "latex_pi",
    "\"Pi\"": "latex_upper_pi",
    "\"rho\"": "latex_rho",
    "\"sigma\"": "latex_sigma",
    "\"Sigma\"": "latex_upper_sigma",
    "\"tau\"": "latex_tau",
    "\"upsilon\"": "latex_upsilon",
    "\"phi\"": "latex_phi",
    "\"Phi\"": "latex_upper_phi",
    "\"varphi\"": "latex_varphi",
    "\"chi\"": "latex_chi",
    "\"psi\"": "latex_psi",
    "\"Psi\"": "latex_upper_psi",
    "\"omega\"": "latex_omega",
    "\"Omega\"": "latex_upper_omega"
}

left_parenthesis = {
    "\"(\"": "left",
    "\"(:\"": "latex_langle",
    "\"[\"": "left_square",
    "\"{\"": "left_curly",
    "\"{:\"": "left_curly_semicolon",
    "\"langle\"": "latex_langle",
    "\"<<\"": "latex_langle",
}

right_parenthesis = {
    "\")\"": "right",
    "\":)\"": "latex_rangle",
    "\"]\"": "right_square",
    "\"}\"": "right_curly",
    "\":}\"": "right_curly_semicolon",
    "\"rangle\"": "latex_rangle",
    "\">>\"": "latex_rangle",
}

arrows = {
    "\"uarr\"": "latex_uparrow",
    "\"uparrow\"": "latex_uparrow",
    "\"darr\"": "latex_downarrow",
    "\"downarrow\"": "latex_downarrow",
    "\"rarr\"": "latex_rightarrow",
    "\"rightarrow\"": "latex_rightarrow",
    "\"->\"": "latex_to",
    "\"to\"": "latex_to",
    "\">->\"": "latex_rightarrowtail",
    "\"rightarrowtail\"": "latex_rightarrowtail",
    "\"->>\"": "latex_twoheadrightarrow",
    "\"twoheadrightarrow\"": "latex_twoheadrightarrow",
    "\">->>\"": "latex_twoheadrightarrowtail",
    "\"twoheadrightarrowtail\"": "latex_twoheadrightarrowtail",
    "\"|->\"": "latex_mapsto",
    "\"mapsto\"": "latex_mapsto",
    "\"larr\"": "latex_leftarrow",
    "\"leftarrow\"": "latex_leftarrow",
    "\"harr\"": "latex_leftrightarrow",
    "\"leftrightarrow\"": "latex_leftrightarrow",
    "\"rArr\"": "latex_upper_rightarrow",
    "\"Rightarrow\"": "latex_upper_rightarrow",
    "\"lArr\"": "latex_upper_leftarrow",
    "\"Leftarrow\"": "latex_upper_leftarrow",
    "\"hArr\"": "latex_upper_leftrightarrow",
    "\"Leftrightarrow\"": "latex_upper_leftrightarrow",
}

misc_symbols = {
    "\"|\"": "bar",
    "\"'\"": "squote",
    "\",\"": "comma",
    "\"_\"": "underscore",
    "\"^\"": "superflex",
    "\"int\"": "latex_int",
    "\"oint\"": "latex_oint",
    "\"del\"": "latex_partial",
    "\"partial\"": "latex_partial",
    "\"grad\"": "latex_nable",
    "\"nabla\"": "latex_nabla",
    "\"+-\"": "latex_pm",
    "\"pm\"": "latex_pm",
    "\"O/\"": "latex_emptyset",
    "\"emptyset\"": "latex_emptyset",
    "\"oo\"": "latex_infty",
    "\"infty\"": "latex_infty",
    "\"aleph\"": "latex_aleph",
    "\":.\"": "latex_therefore",
    "\"therefore\"": "latex_therefore",
    "\":'\"": "latex_because",
    "\"because\"": "latex_because",
    "\"...\"": "latex_ldots",
    "\"ldots\"": "latex_ldots",
    "\"cdots\"": "latex_cdots",
    "\"vdots\"": "latex_vdots",
    "\"ddots\"": "latex_ddots",
    "\"quad\"": "latex_quad",
    "\"/_\"": "latex_angle",
    "\"angle\"": "latex_angle",
    "\"frown\"": "latex_frown",
    "\"/_\\\\\"": "latex_triangle",
    "\"triangle\"": "latex_triangle",
    "\"diamond\"": "latex_diamond",
    "\"square\"": "latex_square",
    "\"|__\"": "latex_lfloor",
    "\"lfloor\"": "latex_lfloor",
    "\"__|\"": "latex_rfloor",
    "\"rfloor\"": "latex_rfloor",
    "\"|~\"": "latex_lceiling",
    "\"lceiling\"": "latex_lceiling",
    "\"~|\"": "latex_rceiling",
    "\"rceiling\"": "latex_rceiling",
    "\"CC\"": "complex_set",
    "\"NN\"": "natural_set",
    "\"QQ\"": "rational_set",
    "\"RR\"": "real_set",
    "\"ZZ\"": "integer_set",
}


class LatexTransformer(Transformer):

    def __init__(self, log=True, visit_tokens=False):
        super(LatexTransformer, self).__init__(visit_tokens=visit_tokens)
        self.latex_trans = {
            "bar": "|",
            "natural": "\\mathbb{N}",
            "rational": "\\mathbb{Q}",
            "real": "\\mathbb{R}",
            "integer": "\\mathbb{Z}",
            "complex": "\\mathbb{C}",
            "plus": "+",
            "minus": "-",
            "frac": "/",
            "<": "<",
            "lt": "<",
            ">": ">",
            "gt": ">",
            "equal": "=",
            "left": "(",
            "left_square": "[",
            "left_curly": "\\{",
            "left_curly_semicolon": "",
            "right": ")",
            "right_square": "]",
            "right_curly": "\\}",
            "right_curly_semicolon": "",
            "and": "and",
            "or": "or",
            "if": "if",
            "comma": ",",
            "underscore": "\\_",
            "superflex": "\\^",
            "squote": "'"
        }
        self.left_parenthesis = [
            "\\(", "\\[", "\\{", "langle", "<<"]
        self.right_parenthesis = ["\\)",
                                  "\\]", "\\}", "rangle", ">>"]
        self.formatted_left_parenthesis = "|".join(self.left_parenthesis)
        self.formatted_right_parenthesis = "|".join(self.right_parenthesis)
        self.start_end_par_pattern = re.compile(
            r"^(?:\\left(?:(?:\\)?({})))"
            r"(.*?)"
            r"(?:\\right(?:(?:\\)?({})))$".format(
                self.formatted_left_parenthesis,
                self.formatted_right_parenthesis
            )
        )
        self.split_par_pattern = re.compile(
            r"([\[\]\(\)])")
        logger_func = logging.info
        if not log:
            def logger_func(x): return x
        self._logger = Log(logger_func=logger_func)

    def _log(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            self = args[0]
            return self._logger.__call__(f)(*args, **kwargs)

        return decorator

    @_log
    def remove_parenthesis(self, s: str):
        return re.sub(self.start_end_par_pattern, r"\2", s)

    @_log
    def exp_par(self, items):
        lpar = items[0].data.split("_")
        rpar = items[-1].data.split("_")
        if "latex" in lpar:
            left = "\\left\\" + lpar[2] + " "
        else:
            left = "\\left" + ("." if "semicolon" in lpar else "") + \
                self.latex_trans["_".join(lpar[1:])]
        if "latex" in rpar:
            right = "\\right\\" + rpar[2] + " "
        else:
            right = "\\right" + \
                ("." if "semicolon" in rpar else "") + \
                self.latex_trans["_".join(rpar[1:])]
        return left + " ".join(items[1:-1]) + right

    @_log
    def exp_mat(self, items, mat_type="pmatrix"):
        return "\\begin{" + mat_type + "}" + \
            items[0] + "\\end{" + mat_type + "}"

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
        return ", ".join(items)

    @_log
    def csl_mat(self, items):
        return " \\\\ ".join(items)

    @_log
    def icsl_mat(self, items):
        return " & ".join(items)

    @_log
    def exp_frac(self, items):
        # logging.info("exp", items)
        return "\\frac{" + items[0] + "}{" + items[1] + "}"

    @_log
    def exp_under(self, items):
        # logging.info("exp_under", items)
        items[1] = self.remove_parenthesis(items[1])
        return items[0] + "_{" + items[1] + "}"

    @_log
    def exp_super(self, items):
        # logging.info("exp_super", items)
        items[1] = self.remove_parenthesis(items[1])
        return items[0] + "^{" + items[1] + "}"

    @_log
    def exp_interm(self, items):
        # logging.info("exp_interm", items)
        return items[0]

    @_log
    def exp_under_super(self, items):
        # logging.info("exp_under_super", items)
        items[1] = self.remove_parenthesis(items[1])
        items[2] = self.remove_parenthesis(items[2])
        return items[0] + "_{" + items[1] + "}^{" + items[2] + "}"

    @_log
    def symbol(self, items):
        # logging.info("exp_simple", items)
        return items[0]

    @_log
    def exp_unary(self, items):
        # logging.info("exp_unary", items)
        unary = items[0].data.split("_")
        items[1] = self.remove_parenthesis(items[1])
        if "latex" in unary:
            return "\\" + unary[2] + "{" + items[1] + "}"
        elif unary[1] == "norm":
            return "\\left \\lVert " + items[1] + " \\right \\rVert"
        elif unary[1] == "abs":
            return "\\left \\mid " + items[1] + " \\right \\mid"
        elif unary[1] == "floor":
            return "\\left \\lfloor " + items[1] + " \\right \\rfloor"
        else:
            return "\\left \\lceil " + items[1] + " \\right \\rceil"

    @_log
    def exp_binary(self, items):
        # logging.info("exp_binary", items)
        binary = items[0].data.split("_")
        items[1] = self.remove_parenthesis(items[1])
        items[2] = self.remove_parenthesis(items[2])
        if binary[2] == "sqrt":
            return "\\" + binary[2] +\
                "[" + items[1] + "]" +\
                "{" + items[2] + "}"
        else:
            return "\\" + binary[2] +\
                "{" + items[1] + "}" +\
                "{" + items[2] + "}"

    @_log
    def q_str(self, items):
        # logging.info("quoted_string", items)
        return "\\text{" + items[0] + "}"

    @_log
    def var(self, items):
        # logging.info("var", items)
        return items[0].value

    @_log
    def num(self, items):
        # logging.info("num", items)
        return items[0].value

    @_log
    def misc_symbols(self, items):
        # logging.info("misc", items)
        misc = items[0].data.split("_")
        if "latex" in misc:
            return '\\' + misc[2]
        else:
            return self.latex_trans[misc[1]]

    @_log
    def operation_symbols(self, items):
        # logging.info("op", items)
        op = items[0].data.split("_")
        if "latex" in op:
            return '\\' + op[2]
        else:
            return self.latex_trans[op[1]]

    @_log
    def logical_symbols(self, items):
        # logging.info("logical", items)
        log = items[0].data.split("_")
        if "latex" in log:
            return "\\" + log[2]
        else:
            return "\\text{" + self.latex_trans[log[1]] + "}"

    @_log
    def relation_symbols(self, items):
        # logging.info("rel", items)
        rel = items[0].data.split("_")
        if "latex" in rel:
            return "\\" + rel[2]
        else:
            return self.latex_trans[rel[1]]

    @_log
    def function_symbols(self, items):
        # logging.info("func", items)
        func = items[0].data.split("_")
        if "latex" in func:
            return "\\" + func[2]
        else:
            return func[1]

    @_log
    def greek_letters(self, items):
        # logging.info("func", items)
        greek = items[0].data.split("_")
        if "upper" in greek:
            return "\\" + greek[3].capitalize()
        else:
            return "\\" + greek[2]

    @_log
    def arrows(self, items):
        # logging.info("arrows", items)
        arr = items[0].data.split("_")
        return "\\" + arr[2]

    @_log
    def derivatives(self, items):
        # logging.info("derivatives", items)
        return items[0].value

    @_log
    def exp(self, items):
        return " ".join(items)


class ASCIIMath2Tex(object):

    def __init__(
            self, grammar, *args, inplace=False, parser="lalr",
            lexer="contextual",
            transformer=LatexTransformer(),
            **kwargs):
        self.inplace = inplace
        self.grammar = grammar
        self.transformer = transformer
        if inplace:
            kwargs.update({"transformer": transformer})
        self.parser = Lark(
            grammar,
            *args,
            parser=parser,
            lexer=lexer,
            **kwargs)

    def asciimath2tex(self, s: str, pprint=False):
        if not self.inplace:
            parsed = self.parser.parse(s)
            if pprint:
                print(parsed.pretty())
            return self.transformer.transform(parsed)
        else:
            return self.parser.parse(s)


asciimath_grammar = r"""
    start: i+ -> exp
    csl: start ("," start)* ","?                    // csl = Comma Separated List
    csl_mat: icsl_mat ("," icsl_mat)* ","?          // csl_mat = Comma Separated List for Matrices
    icsl_mat: "[" start? ("," start)* ","? "]"      // icsl_mat = Internal Comma Separated List
    i: s -> exp_interm
        | s "/" s -> exp_frac
        | s "_" s -> exp_under
        | s "^" s -> exp_super
        | s "_" s "^" s -> exp_under_super
    s: c -> symbol
        | l csl? r -> exp_par
        | "[" csl_mat? "]" -> exp_bmat
        | "(" csl_mat? ")" -> exp_pmat
        | "(" csl_mat? ")" -> exp_pmat
        | "{{" csl_mat? "}}" -> exp_cmat
        | "|" csl_mat? "|" -> exp_vmat
        | "||" csl_mat? "||" -> exp_nmat
        | "{{" csl_mat? ")" -> exp_system
        | u s -> exp_unary
        | b s s -> exp_binary
        | _qs -> q_str
    l: {} // left parenthesis
    r: {} // right parenthesis
    b: {} // binary functions
    u: {} // unary functions
    _qs: "\"" /(?<=").+(?=")/ "\""
    c: LETTER -> var
       | NUMBER -> num
       | /d[A-Za-z]/ -> derivatives
       | ms -> misc_symbols
       | os -> operation_symbols
       | rs -> relation_symbols
       | ls -> logical_symbols
       | fs -> function_symbols
       | g -> greek_letters
       | a -> arrows
    ms: {}
    os: {}
    rs: {}
    ls: {}
    fs: {}
    g: {}
    a: {}
    %import common.WS
    %import common.LETTER
    %import common.NUMBER
    %ignore WS
""".format(
    alias_string(left_parenthesis, prefix="par"),
    alias_string(right_parenthesis, prefix="par"),
    alias_string(binary_functions, prefix="binary"),
    alias_string(unary_functions, prefix="unary"),
    alias_string(misc_symbols, prefix="misc"),
    alias_string(operation_symbols, prefix="op"),
    alias_string(relation_symbols, prefix="rel"),
    alias_string(logical_symbols, prefix="logical"),
    alias_string(function_symbols, prefix="func"),
    alias_string(greek_letters, prefix="greek"),
    alias_string(arrows, prefix="arrow")
)
parser = ASCIIMath2Tex(
    asciimath_grammar,
    inplace=False,
    transformer=LatexTransformer())
text = ""
text = text + '''
    frac{root(5)(a iff c)}
    {
        dstyle int(
            sqrt(x_2^3.14)
            X
            root(langle x,t rangle) (max(dot z,4)) +
            min(x,y,"time",bbb C)
        ) dg
    }
'''
text = text + '''
    uuu_{2(x+1)=1)^{n}
    min{
            2x|x^{y+2} in bbb(N) wedge arccos root(3}(frac{1}{3x}) < i rarr Omega < b, 5=x
    }
'''
text = text + '''
  [[[[v, c], [a,b]]]]
  (((x+2), (int e^{x^2} dx)))
  oint (lfloor x rfloor quad) dx'''
text = text + '''lim_(N->oo) sum_(i=0)^N int_0^1 f(x)dx'''
text = text + '''||[2 x + 17 y = 23],[y = int_{0}^{x} t dt]||'''
text = text + \
    '''floor frac "Time" (A nn (bbb(N) | f'(x) = dx/dy | |><| (D setminus (B uu C))))'''
text = text + \
    '''[[1,2,[[5,6], [7,8,]]], [3,4]]'''
text = text + \
    '''e^{{([2 x + 17 y = 23, [1]],[y = dstyle int_{0}^{x} t dt],[y = dstyle int_{0}^{x} t dt])}}'''
text = text + ''','''
print(parser.asciimath2tex(text, pprint=True))