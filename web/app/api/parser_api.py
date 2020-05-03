from flask import jsonify, request
from web.app.services.parser.parser import ASCIIMath2Tex
from web.app.services.parser.const import asciimath_grammar


def exp2latex(exp):
    parser = ASCIIMath2Tex(
        asciimath_grammar, inplace=True, parser="lalr", lexer="contextual"
    )
    return parser.asciimath2tex(exp)


def exp2json():
    exp = request.args.get("expression")
    return jsonify(latex=exp2latex(exp))
