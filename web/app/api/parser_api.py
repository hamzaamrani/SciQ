from flask import jsonify, request

from web.app import limiter
from web.app.services.parser.const import asciimath_grammar
from web.app.services.parser.parser import ASCIIMath2Tex


def exp2latex(exp):
    parser = ASCIIMath2Tex(
        asciimath_grammar, inplace=True, parser="lalr", lexer="contextual"
    )
    return parser.asciimath2tex(exp)


@limiter.limit("200 per day;50 per hour")
def exp2json():
    exp = request.args.get("expression")
    return jsonify(latex=exp2latex(exp))
