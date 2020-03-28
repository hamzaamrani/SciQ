from lark import (Lark, Transformer, Discard, Tree,
                  Token)
from lark.exceptions import VisitError, GrammarError
from itertools import chain
from log import Log, flatten
import re
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
"""
    Search regex: (\s*)(\S+(\s\S+)?)(\s*)
    Replace regex: $1"\"$2\"": "$2",
"""


def alias_string(mapping: dict, init=False, prefix=""):
    mapping = list(mapping.items())
    s = "|" if init else "" + \
        mapping[0][0] + " -> " + \
        (prefix + "_" if prefix != "" else "") + mapping[0][1]
    for k, v in mapping[1:]:
        s = s + "\n\t| " + k + " -> " + \
            (prefix + "_" if prefix != "" else "") + v
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
    # "\"f\"": "f",
    # "\"g\"": "g"
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
    "\"{:\"": "left_curly_semi_colon",
    "\"langle\"": "latex_langle",
    "\"<<\"": "latex_langle",
}

right_parenthesis = {
    "\")\"": "right",
    "\":)\"": "latex_rangle",
    "\"]\"": "right_square",
    "\"}\"": "right_curly",
    "\":}\"": "right_curly_semi_colon",
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


def __init__(self, data, children, meta=None, parent=None):
    self.data = data
    self.children = children
    self._meta = meta
    self.parent = parent


Tree.__init__ = __init__


class LatexTransformer(Transformer):
    log = Log(logger_func=logging.info)

    # TODO: translate LateX matrices

    def __init__(self, visit_tokens=False):
        super(LatexTransformer, self).__init__(visit_tokens=visit_tokens)
        # TODO: left/right curly semicolon
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
            "left_curly_semi_colon": "\\{",
            "right": ")",
            "right_square": "]",
            "right_curly": "\\}",
            "right_curly_semi_colon": "\\}",
            "and": "and",
            "or": "or",
            "if": "if"
        }
        self.left_parenthesis = [
            "\\(", ":\\(", "\\[", "\\{", ":\\{", "langle", "<<"]
        self.right_parenthesis = ["\\)", ":\\)",
                                  "\\]", "\\}", ":\\}", "rangle", ">>"]
        self.formatted_left_parenthesis = "|".join(self.left_parenthesis)
        self.formatted_right_parenthesis = "|".join(self.right_parenthesis)
        self.start_end_par_reg = re.compile(
            r"^(?:\\left(?:(?:\\)?(?:{})))"
            r"(.*?)"
            r"(?:\\right(?:(?:\\)?(?:{})))$".format(
                self.formatted_left_parenthesis,
                self.formatted_right_parenthesis
            )
        )

    def _call_userfunc(self, tree, new_children=None):
        # Assumes tree is already transformed
        children = tree.children if new_children is None else new_children
        try:
            f = getattr(self, tree.data)
        except AttributeError:
            return self.__default__(tree, children)
        else:
            try:
                wrapper = getattr(f, 'visit_wrapper', None)
                if wrapper is not None:
                    return f.visit_wrapper(f, tree, children)
                else:
                    return f(children)
            except (GrammarError, Discard):
                raise
            except Exception as e:
                raise VisitError(tree.data, tree, e)

    def _transform_children(self, tree):
        for c in tree.children:
            try:
                if isinstance(c, Tree):
                    c.parent = tree
                    yield self._transform_tree(c)
                elif self.__visit_tokens__ and isinstance(c, Token):
                    c.parent = tree
                    yield self._call_userfunc_token(c)
                else:
                    yield c
            except Discard:
                pass

    def _transform_tree(self, tree):
        children = list(self._transform_children(tree))
        return self._call_userfunc(tree, children)

    def transform(self, tree):
        tree.parent = None
        return self._transform_tree(tree)

    def __default__(self, tree, children):
        """Default operation on tree (for override)"""
        return Tree(tree.data, children, tree.meta, tree.parent)

    def remove_parenthesis(self, s: str):
        return re.sub(self.start_end_par_reg, r"\1", s)

    @log
    def exp(self, items):
        # logging.info("exp", items)
        if isinstance(items[0], list):
            return " ".join(items[0])
        return " ".join(items)

    @log
    def exp_system(self, items):
        # logging.info("exp", items)
        return "\\begin{cases}" + "\\\\".join(
            map(lambda x: re.sub(r"(?<!&)=", "&=", x, 1),
                items)) + "\\end{cases}"

    @log
    def exp_pmat(self, items):
        items = items[0]
        n = len(items[0])
        consistent_mat = all(len(el) == n for el in items[1:])
        if consistent_mat:
            mat = "\\begin{pmatrix}" + "\\\\".join(
                [" & ".join(el) for el in items]) + "\\end{pmatrix}"
        return mat

    @log
    def exp_bmat(self, items):
        n = len(items[0])
        consistent_mat = all(len(el) == n for el in items[1:])
        if consistent_mat:
            mat = "\\begin{bmatrix}" + "\\\\".join(
                [" & ".join(el) for el in items]) + "\\end{bmatrix}"
        return mat

    @log
    def exp_list(self, items):
        return [list(flatten(el)) for el in items]

    @log
    def exp_frac(self, items):
        # logging.info("exp", items)
        return "\\frac{" + items[0] + "}{" + items[1] + "}"

    @log
    def exp_under(self, items):
        # logging.info("exp_under", items)
        items[1] = self.remove_parenthesis(items[1])
        return items[0] + "_{" + items[1] + "}"

    @log
    def exp_super(self, items):
        # logging.info("exp_super", items)
        items[1] = self.remove_parenthesis(items[1])
        return items[0] + "^{" + items[1] + "}"

    @log
    def exp_interm(self, items):
        # logging.info("exp_interm", items)
        return items[0]

    @log
    def exp_under_super(self, items):
        # logging.info("exp_under_super", items)
        items[1] = self.remove_parenthesis(items[1])
        items[2] = self.remove_parenthesis(items[2])
        return items[0] + "_{" + items[1] + "}^{" + items[2] + "}"

    @log
    def exp_simple(self, items):
        # logging.info("exp_simple", items)
        return items[0]

    @log
    def exp_par(self, items):
        # logging.info("exp_par", items)
        # if items[0].parent.parent.data not in [
        #         "exp_under_super", "exp_super", "exp_under", "exp_frac"]:
        lpar = items[0].data.split("_")
        rpar = items[2].data.split("_")
        if "latex" in lpar:
            left = "\\left\\" + lpar[2] + " "
        else:
            left = "\\left" + self.latex_trans["_".join(lpar[1:])]
        if "latex" in rpar:
            right = "\\right\\" + rpar[2] + " "
        else:
            right = "\\right" + self.latex_trans["_".join(rpar[1:])]
        return left + items[1] + right
        # else:
        #     return items[1]

    @log
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

    @log
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

    @log
    def quoted_string(self, items):
        # logging.info("quoted_string", items)
        return "\\text{" + items[0] + "}"

    @log
    def var(self, items):
        # logging.info("var", items)
        return items[0].value

    @log
    def num(self, items):
        # logging.info("num", items)
        return items[0].value

    @log
    def punctuation(self, items):
        # logging.info("punct", items)
        return items[0]

    @log
    def misc_symbols(self, items):
        # logging.info("misc", items)
        misc = items[0].data.split("_")
        if "latex" in misc:
            return '\\' + misc[2]
        else:
            return self.latex_trans[misc[1]]

    @log
    def operation_symbols(self, items):
        # logging.info("op", items)
        op = items[0].data.split("_")
        if "latex" in op:
            return '\\' + op[2]
        else:
            return self.latex_trans[op[1]]

    @log
    def logical_symbols(self, items):
        # logging.info("logical", items)
        log = items[0].data.split("_")
        if "latex" in log:
            return "\\" + log[2]
        else:
            return "\\text{" + self.latex_trans[log[1]] + "}"

    @log
    def relation_symbols(self, items):
        # logging.info("rel", items)
        rel = items[0].data.split("_")
        if "latex" in rel:
            return "\\" + rel[2]
        else:
            return self.latex_trans[rel[1]]

    @log
    def function_symbols(self, items):
        # logging.info("func", items)
        func = items[0].data.split("_")
        if "latex" in func:
            return "\\" + func[2]
        else:
            return func[1]

    @log
    def greek_letters(self, items):
        # logging.info("func", items)
        greek = items[0].data.split("_")
        if "upper" in greek:
            return "\\" + greek[3].capitalize()
        else:
            return "\\" + greek[2]

    @log
    def arrows(self, items):
        # logging.info("arrows", items)
        arr = items[0].data.split("_")
        return "\\" + arr[2]

    @log
    def derivatives(self, items):
        # logging.info("derivatives", items)
        return items[0].value

    @log
    def exp_comma(self, items):
        return ",".join(items)


asciimath_grammar = r"""
    ?e: i+ -> exp 
        | e "," i? -> exp_comma
    ?i: s -> exp_interm
        | s "/" s -> exp_frac
        | s "_" s -> exp_under
        | s "^" s -> exp_super
        | s "_" s "^" s -> exp_under_super
        | "{{" ("(" e ")" ","?)+ ":}}" -> exp_system
    ?s: c -> exp_simple
        | l e r -> exp_par
        | u s -> exp_unary
        | b s s -> exp_binary
        | quoted_string -> quoted_string
    ?l: {} // left parenthesis
    ?r: {} // right parenthesis
    ?b: {} // binary functions
    ?u: {} // unary functions
    ?c: /[A-Za-z]/ -> var
        | NUMBER -> num
        | misc_symbols -> misc_symbols
        | operation_symbols -> operation_symbols
        | relation_symbols -> relation_symbols
        | function_symbols -> function_symbols
        | logical_symbols -> logical_symbols
        | greek_letters -> greek_letters
        | arrows -> arrows
        | DERIVATIVES -> derivatives
    ?misc_symbols: {}
    ?operation_symbols: {}
    ?relation_symbols: {}
    ?logical_symbols: {}
    ?function_symbols: {}
    ?greek_letters: {}
    ?arrows: {}
    ?quoted_string: "\"" DOUBLE_QUOTED_STRING "\""
        | "'" SINGLE_QUOTED_STRING "'"
    DOUBLE_QUOTED_STRING: /(?<=").+(?=")/
    SINGLE_QUOTED_STRING: /(?<=').+(?=')/
    DERIVATIVES: /d[A-Za-z]/
    // PUNCTUATION: ","
    //    | "."
    //    | "'"
    %import common.WS
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
asciimath_parser = Lark(
    asciimath_grammar, start="e", parser='lalr', debug=True, )
# text = '''
#     frac{root(5)(a iff c)}
#     {
#         dstyle int(
#             sqrt(x_2^3.14)
#             X
#             root(langle x,t rangle) (max(dot z,4)) +
#             min(x,y,"time",bbb C)
#         ) dg
#     }
# '''
# text = '''
#     uuu_{2(x+1)=1)^{n}
#     min{
#             2x|x^{y+2} in bbb(N) wedge arccos root(3}(frac{1}{3x}) < i rarr Omega < b
#         }
#     }
# '''
# text = '''
#   [[[[v, c], [a,b]]]]
#   (((x+2), (int e^{x^2} dx)))
#   oint (lfloor x rfloor quad) dx'''
# text = '''
#     floor frac "Time" (A nn (bbb(N) |><| (D setminus (B uu C))))
# '''
# text = '''lim_(N->oo) sum_(i=0)^N int_0^1 f(x)dx'''
# text = '''{(2 x + 17 y = 23),(y = int_{0}^{x} t dt):}'''
text = '''lim_(N->oo) sum_(i=0)^N dstyle int_0^1 f(x)dx'''
parsed_text = asciimath_parser.parse(text)
print(parsed_text.pretty())
print(LatexTransformer().transform(parsed_text))
