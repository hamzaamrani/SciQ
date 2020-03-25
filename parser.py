from lark import Lark
import logging
logging.basicConfig(level=logging.DEBUG)


asciimath_parser = Lark(r"""
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
        | WORD -> raw
    ?l: "(" -> left_par
        | "(:" -> left_semi_colon_par
        | "[" -> left_square_par
        | "{" -> left_curly_par
        | "{:" -> left_curly_semi_colon_par
        | "langle" -> langle
    ?r: ")" -> right_par
        | ":)" -> right_semi_colon_par
        | "]" -> right_square_par
        | "}" -> right_curly_par
        | ":}" -> right_curly_semi_colon_par
        | "rangle" -> rangle
    ?b: "frac" -> frac
        | "root" -> root
        | "stackrel" -> stackrel
    ?u: "sqrt" -> sqrt
        | "text" -> text
        | "bb" -> bb
        | "dot" -> dot
    ?c: NUMBER -> num
        | "+" -> plus_op
        | "*" -> cdot_op
        | "," -> comma
        | "min" -> min
        | "max" -> max
        | "int" -> int

    %import common.WS
    %import common.WORD
    %import common.NUMBER
    %ignore WS
""", start="e", parser='lalr', debug=True, )

text = 'frac{root(5)(langle z,y rangle)}{int(sqrt(x_2^3.14) X root(langle x,t rangle) (max(dot z,4)) + min(x,y,text(time)))dx}'
parsed_text = asciimath_parser.parse(text)
print(parsed_text.pretty())
