from flask import jsonify, request

from flask_jwt_extended import jwt_optional
from web.app import limiter
from web.app.services.parser.const import asciimath_grammar
from web.app.services.parser.parser import ASCIIMath2Tex
from web.app.services.utils.utils import exempt_limit, get_limit


def exp2latex(exp):
    parser = ASCIIMath2Tex(
        asciimath_grammar, inplace=True, parser="lalr", lexer="contextual"
    )
    return parser.asciimath2tex(exp)


@jwt_optional
@limiter.limit(get_limit, exempt_when=exempt_limit)
def exp2json():
    exp = request.args.get("expression")
    return jsonify(latex=exp2latex(exp))
