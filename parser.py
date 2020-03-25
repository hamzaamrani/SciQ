from lark import Lark
import logging
logging.basicConfig(level=logging.DEBUG)

"""
    Search regex: (\s*)(\S+(\s\S+)?)(\s*)
    Replace regex: $1"\"$2\"": "$2",
"""

def alias_string(mapping: dict, init=False):
    mapping = list(mapping.items())
    s = "|" if init else "" + mapping[0][0] + " -> " + mapping[0][1]
    for k, v in mapping[1:]:
        s = s + "\n\t| " + k + " -> " + v
    return s


binary_functions = {
    "\"frac\"": "frac",
    "\"root\"": "root",
    "\"stackrel\"": "stackrel",
    "\"overset\"": "overset",
    "\"underset\"": "underset",
    "\"color\"": "color",
}

unary_functions = {
    "\"sqrt\"": "sqrt",
    "\"text\"": "textrm",
    "\"dot\"": "dot",
    "\"abs\"": "abs",
    "\"floor\"": "floor",
    "\"ceil\"": "ceil",
    "\"norm\"": "norm",
    "\"ubrace\"": "ubrace",
    "\"obrace\"": "obrace",
    "\"cancel\"": "cancel",
    "\"bb\"": "boldsymbol",
    "\"bbb\"": "mathbb",
    "\"cc\"": "mathcal",
    "\"tt\"": "texttt",
    "\"fr\"": "mathfrak",
    "\"sf\"": "textsf",
}

operation_symbols = {
    "\"+\"": "op_plus",
    "\"*\"": "op_cdot",
    "\"-\"": "op_minus",
    "\"cdot\"": "op_cdot",
    "\"**\"": "op_ast",
    "\"ast\"": "op_ast",
    "\"***\"": "op_star",
    "\"star\"": "op_star",
    "\"//\"": "op_frac",
    "\"\\\\\"": "op_backslash_setminus",
    "\"backslash_setminus\"": "op_backslash_setminus",
    "\"xx\"": "op_xx",
    "\"times\"": "op_times",
    "\"-:\"": "op_div",
    "\"div\"": "op_div",
    "\"|><\"": "op_ltimes",
    "\"ltimes\"": "op_ltimes",
    "\"><|\"": "op_rtimes",
    "\"rtimes\"": "op_rtimes",
    "\"|><|\"": "op_bowtie",
    "\"bowtie\"": "op_bowtie",
    "\"@\"": "op_circ",
    "\"circ\"": "op_circ",
    "\"o+\"": "op_oplus",
    "\"oplus\"": "op_oplus",
    "\"ox\"": "op_otimes",
    "\"otimes\"": "op_otimes",
    "\"o.\"": "op_odot",
    "\"odot\"": "op_odot",
    "\"sum\"": "op_sum",
    "\"prod\"": "op_prod",
    "\"^^\"": "op_wedge",
    "\"wedge\"": "op_wedge",
    "\"^^^\"": "op_bigwedge",
    "\"bidwedge\"": "op_bidwedge",
    "\"vv\"": "op_vee",
    "\"vee\"": "op_vee",
    "\"vvv\"": "op_bigvee",
    "\"bigvee\"": "op_bigvee",
    "\"nn\"": "op_cap",
    "\"cap\"": "op_cap",
    "\"nnn\"": "op_bigcap",
    "\"bigcap\"": "op_bigcap",
    "\"uu\"": "op_cup",
    "\"cup\"": "op_cup",
    "\"uuu\"": "op_bigcup",
    "\"bigcup\"": "op_bigcup",
}

logical_symbols = {
    "\"and\"": "logical_and",
    "\"or\"": "logical_or",
    "\"not\"": "logical_not",
    "\"neg\"": "logical_neg",
    "\"=>\"": "logical_implies",
    "\"implies\"": "logical_implies",
    "\"if\"": "logical_if",
    "\"<=>\"": "logical_iff",
    "\"iff\"": "logical_iff",
    "\"AA\"": "logical_forall",
    "\"forall\"": "logical_forall",
    "\"EE\"": "logical_exists",
    "\"exists\"": "logical_exists",
    "\"_|_\"": "logical_bot",
    "\"bot\"": "logical_bot",
    "\"TT\"": "logical_top",
    "\"top\"": "logical_top",
    "\"|--\"": "logical_vdash",
    "\"vdash\"": "logical_vdash",
    "\"|==\"": "logical_models",
    "\"models\"": "logical_models",
}

relation_symbols = {
    "\"=\"": "rel_equal",
    "\"!=\"": "rel_ne",
    "\"ne\"": "rel_ne",
    "\"<\"": "rel_lt",
    "\"lt\"": "rel_lt",
    "\">\"": "rel_gt",
    "\"gt\"": "rel_gt",
    "\"<=\"": "rel_le",
    "\"le\"": "rel_le",
    "\">=\"": "rel_ge",
    "\"ge\"": "rel_ge",
    "\"-<\"": "rel_prec",
    "\"prec\"": "rel_prec",
    "\"-<=\"": "rel_preceq",
    "\"preceq\"": "rel_preceq",
    "\">-\"": "rel_succ",
    "\"succ\"": "rel_succ",
    "\">-=\"": "rel_succeq",
    "\"succeq\"": "rel_succeq",
    "\"in\"": "rel_in",
    "\"in\"": "rel_in",
    "\"!in\"": "rel_notin",
    "\"notin\"": "rel_notin",
    "\"sub subset\"": "rel_sub_subset",
    "\"sup	supset\"": "rel_sup_supset",
    "\"sube\"": "rel_subseteq",
    "\"subseteq\"": "rel_subseteq",
    "\"supe\"": "rel_supseteq",
    "\"supseteq\"": "rel_supseteq",
    "\"-=\"": "rel_equiv",
    "\"equiv\"": "rel_equiv",
    "\"~=\"": "rel_cong",
    "\"cong\"": "rel_cong",
    "\"~~\"": "rel_approx",
    "\"approx\"": "rel_approx",
    "\"prop\"": "rel_propto",
    "\"propto\"": "rel_propto",
}

function_symbols = {
    "\"sin\"": "func_sin",
    "\"cos\"": "func_cos",
    "\"tan\"": "func_tan",
    "\"sec\"": "func_sec",
    "\"csc\"": "func_csc",
    "\"cot\"": "func_cot",
    "\"arcsin\"": "func_arcsin",
    "\"arccos\"": "func_arccos",
    "\"arctan\"": "func_arctan",
    "\"sinh\"": "func_sinh",
    "\"cosh\"": "func_cosh",
    "\"tanh\"": "func_tanh",
    "\"sech\"": "func_sech",
    "\"csch\"": "func_csch",
    "\"coth\"": "func_coth",
    "\"exp\"": "func_exp",
    "\"log\"": "func_log",
    "\"ln\"": "func_ln",
    "\"det\"": "func_det",
    "\"dim\"": "func_dim",
    "\"mod\"": "func_mod",
    "\"gcd\"": "func_gcd",
    "\"lcm\"": "func_lcm",
    "\"lub\"": "func_lub",
    "\"glb\"": "func_glb",
    "\"min\"": "func_min",
    "\"max\"": "func_max",
    "\"f\"": "func_f",
    "\"g\"": "func_g"
}

greek_letters = {
    "\"alpha\"": "alpha",
    "\"beta\"": "beta",
    "\"gamma\"": "gamma",
    "\"Gamma\"": "upper_gamma",
    "\"delta\"": "delta",
    "\"Delta\"": "upper_delta",
    "\"epsilon\"": "epsilon",
    "\"varepsilon\"": "varepsilon",
    "\"zeta\"": "zeta",
    "\"eta\"": "eta",
    "\"theta\"": "theta",
    "\"Theta\"": "upper_theta",
    "\"vartheta\"": "vartheta",
    "\"iota\"": "iota",
    "\"kappa\"": "kappa",
    "\"lambda\"": "lambda",
    "\"Lambda\"": "upper_lambda",
    "\"mu\"": "mu",
    "\"nu\"": "nu",
    "\"xi\"": "xi",
    "\"Xi\"": "upper_xi",
    "\"pi\"": "pi",
    "\"Pi\"": "upper_pi",
    "\"rho\"": "rho",
    "\"sigma\"": "sigma",
    "\"Sigma\"": "upper_sigma",
    "\"tau\"": "tau",
    "\"upsilon\"": "upsilon",
    "\"phi\"": "phi",
    "\"Phi\"": "upper_phi",
    "\"varphi\"": "varphi",
    "\"chi\"": "chi",
    "\"psi\"": "psi",
    "\"Psi\"": "upper_psi",
    "\"omega\"": "omega",
    "\"Omega\"": "upper_omega"
}

asciimath_grammar = r"""
    ?e: i+ -> exp
    ?i: s -> inter_exp
        | s "/" s -> frac_exp
        | s "_" s -> under_exp
        | s "^" s -> super_exp
        | s "_" s "^" s -> under_super_exp
    ?s: c -> simple_exp
        | l e r -> par_exp
        | u s -> unary_exp
        | b s s -> binary_exp
        | quoted_string -> quoted_string
    ?l: "(" -> left_par
        | "(:" -> left_semi_colon_par
        | "[" -> left_square_par
        | "{{" -> left_curly_par
        | "{{:" -> left_curly_semi_colon_par
        | "langle" -> langle
    ?r: ")" -> right_par
        | ":)" -> right_semi_colon_par
        | "]" -> right_square_par
        | "}}" -> right_curly_par
        | ":}}" -> right_curly_semi_colon_par
        | "rangle" -> rangle
    ?b: {} // binary functions
    ?u: {} // unary functions
    ?c: /[A-Za-z]/ -> var
        | NUMBER -> num
        | "," -> comma
        | "int" -> int
        | "|" -> bar
        | operation_symbols
        | relation_symbols
        | logical_symbols
        | function_symbols
        | greek_letters
        | DERIVATIVES -> derivatives
    ?operation_symbols: {}
    ?relation_symbols: {}
    ?logical_symbols: {}
    ?function_symbols: {}
    ?greek_letters: {}
    ?quoted_string: "\"" DOUBLE_QUOTED_STRING "\""
        | "'" SINGLE_QUOTED_STRING "'"
    DOUBLE_QUOTED_STRING: /(?<=").+(?=")/
    SINGLE_QUOTED_STRING: /(?<=').+(?=')/
    DERIVATIVES: /d[A-Za-z]/

    %import common.WS
    %import common.WORD
    %import common.LETTER
    %import common.NUMBER
    %ignore WS
""".format(
    alias_string(binary_functions),
    alias_string(unary_functions),
    alias_string(operation_symbols),
    alias_string(relation_symbols),
    alias_string(logical_symbols),
    alias_string(function_symbols),
    alias_string(greek_letters)
)
asciimath_parser = Lark(asciimath_grammar, start="e",
                        parser='lalr', debug=True)
# text = 'frac{root(5)(langle alpha,omega rangle)}{int(sqrt(x_2^3.14) X root(langle x,t rangle) (max(dot z,4)) + min(x,y,text("time")))dg}'
text = 'min{2x|x in bbb(N) wedge arccos x < 3}'
parsed_text = asciimath_parser.parse(text)
print(parsed_text.pretty())
