from lark import Lark
import logging
logging.basicConfig(level=logging.DEBUG)

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
    "\"frac\"": "latex_frac",
    "\"root\"": "root",
    "\"stackrel\"": "latex_stackrel",
    "\"overset\"": "overset",
    "\"underset\"": "underset",
    "\"color\"": "color",
}

unary_functions = {
    "\"sqrt\"": "latex_sqrt",
    "\"text\"": "latex_textrm",
    "\"abs\"": "abs",
    "\"floor\"": "floor",
    "\"ceil\"": "ceil",
    "\"norm\"": "norm",
    "\"ubrace\"": "latex_underbrace",
    "\"underbrace\"": "latex_underbrace",
    "\"obrace\"": "obrace",
    "\"overbrace\"": "latex_overbrace",
    "\"cancel\"": "cancel",
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
    "\"*\"": "cdot",
    "\"-\"": "minus",
    "\"cdot\"": "latex_cdot",
    "\"**\"": "latex_ast",
    "\"ast\"": "latex_ast",
    "\"***\"": "latex_star",
    "\"star\"": "latex_star",
    "\"//\"": "frac",
    "\"\\\\\"": "latex_backslash_setminus",
    "\"backslash_setminus\"": "latex_backslash_setminus",
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
    "\"<\"": "latex_lt",
    "\"lt\"": "latex_lt",
    "\">\"": "latex_gt",
    "\"gt\"": "latex_gt",
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
    "\"{:\"": "left_curly_semi_colon",
    "\"langle\"": "latex_langle",
    "\"<<\"": "latex_langle"
}

right_parenthesis = {
    "\")\"": "right",
    "\":)\"": "latex_rangle",
    "\"]\"": "right_square",
    "\"}\"": "right_curly",
    "\":}\"": "right_curly_semi_colon",
    "\"rangle\"": "latex_rangle",
    "\">>\"": "latex_rangle"
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
    "\"aleph\"": "aleph",
    "\":.\"": "latex_therefore",
    "\"therefore\"": "latex_therefore",
    "\":'\"": "latex_because",
    "\"because\"": "latex_because",
    "\"...\"": "latex_ldots",
    "\"ldots\"": "latex_ldots",
    "\"cdots\"": "latex_cdots",
    "\"vdots\"": "latex_vdots",
    "\"ddots\"": "latex_ddots",
    "\"quad\"": "empty_space",
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
    "\"rceiling\"": "rceiling",
    "\"CC\"": "complex_set",
    "\"NN\"": "natural_set",
    "\"QQ\"": "rational_set",
    "\"RR\"": "real_set",
    "\"ZZ\"": "integer_set",
}

asciimath_grammar = r"""
    ?e: i+ -> exp
    ?i: s -> exp_interm
        | s "/" s -> exp_frac
        | s "_" s -> exp_under
        | s "^" s -> exp_super
        | s "_" s "^" s -> exp_under_super
    ?s: c -> exp_simple
        | l e r -> exp_par
        | u s -> exp_unary_exp
        | b s s -> exp_binary
        | quoted_string -> quoted_string
    ?l: {} // left parenthesis
    ?r: {} // right parenthesis
    ?b: {} // binary functions
    ?u: {} // unary functions
    ?c: /[A-Za-z]/ -> var
        | NUMBER -> num
        | "," -> comma
        | "." -> point
        | misc_symbols
        | operation_symbols
        | relation_symbols
        | logical_symbols
        | function_symbols
        | greek_letters
        | arrows
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

    %import common.WS
    %import common.WORD
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
asciimath_parser = Lark(asciimath_grammar, start="e",
                        parser='lalr', debug=True)
text = '''
    frac{root(5)(langle alpha,omega rangle)}
    {
        int(
            sqrt(x_2^3.14)
            X
            root(langle x,t rangle) (max(dot z,4)) +
            min(x,y,text("time"))
        ) dg
    }
'''
# text = 'uuu_{i=1}^{n}{min{2x|x in bbb(N) wedge arccos x < i}}'
# text = '''
#   [[v, c], [a,b]]
#   (((x+2), (int e^{x^2} dx)))
#   oint (lfloor x rfloor quad) dx'''
parsed_text = asciimath_parser.parse(text)
print(parsed_text.pretty())
