import logging

from flask import jsonify, request

from flask_jwt_extended import jwt_optional
from web.app import limiter
from web.app.services.parser.const import asciimath_grammar
from web.app.services.parser.parser import ASCIIMath2Tex
from web.app.services.utils.utils import exempt_limit, get_limit

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)


def exp2latex(exp):
    parser = ASCIIMath2Tex(
        asciimath_grammar, inplace=True, parser="lalr", lexer="contextual"
    )
    return parser.asciimath2tex(exp)


@jwt_optional
@limiter.limit(get_limit, exempt_when=exempt_limit)
def exp2json():
    if request.is_json:
        exp = None
        if "expression" in request.get_json():
            exp = request.get_json()["expression"]
    else:
        exp = request.args.get("expression")
    if exp is None:
        return jsonify({"error": "no expression to parse"})
    return jsonify(latex=exp2latex(exp))
