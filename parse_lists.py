from lark import (Lark, Transformer, Discard, Tree,
                  Token, v_args)
from lark.exceptions import VisitError, GrammarError, UnexpectedToken
from itertools import chain
from log import Log, flatten
import re
import logging
import copy

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


class Transformer(Transformer):
    log = Log(logger_func=logging.info)

    def get_level(self, l: list, lvl):
        if lvl > 2:
            return lvl
        for el in l:
            if el == "[":
                lvl = lvl + 1
            elif el == "]":
                lvl = lvl - 1
            if isinstance(el, list):
                lvl = self.get_level(el, lvl)
        return lvl

    @log
    def list(self, items):
        return items

    @log
    def exp(self, items):
        if isinstance(items[0], Token):
            return items[0].value
        return items[0]

    @log
    def visit(self, l: list, action="remove"):
        expanded_l = []
        for el in l:
            if isinstance(el, list):
                el = self.visit(el, action=action)
            elif isinstance(el, Token):
                if action == "remove":
                    continue
                elif action == "expand":
                    el = el.value
            expanded_l = expanded_l + [el]
        return expanded_l

    @log
    def mat(self, items):
        max_lvl = self.get_level(items, 0)
        if max_lvl > 2:
            return ['['] + items + [']']
        else:
            items = self.visit(items, action="remove")
            return "\\begin{bmatrix}" + " \\\\ ".join([" & ".join(el)
                                                       if isinstance(el, list) else el
                                                       for el in items]) + "\\end{bmatrix}"

    def recursive_join(self, l: list):
        s = ""
        for el in l:
            if isinstance(el, list):
                el = self.recursive_join(el)
            elif isinstance(el, Token):
                el = el.value
            s = s + el
        return s

    @log
    def stmt(self, items):
        return self.recursive_join(items)


asciimath_parser = Lark(r"""
    stmt: _csl
    exp: list
        | mat
        | NUMBER
    mat: "[:" _csl? ":]"
    list: (L _csl? R | DOT_L _csl? R | L _csl? DOT_R) -> list
    L.0: "(" | "[" | "{{"
    R.0: ")" | "]" | "}}"
    DOT_L.1: "[:"
    DOT_R.1: ":]"
    _csl: exp (/,/? exp)* /,/?
    %import common.WS
    %import common.NUMBER
    %ignore WS
""", start="stmt", parser='lalr', debug=True)
text = '''1,2,3,4[:[1,3],[:1,[:[1,2], [3,4]:]:]:]'''
parsed_text = asciimath_parser.parse(text)
print(parsed_text.pretty())
print(Transformer().transform(parsed_text))
