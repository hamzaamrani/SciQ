import re
import logging

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)


def concat(s: str):
    return '"' + s + '"'


def check_mat(s: str):
    rows = 0
    cols = 0
    max_cols = 0
    par_stack = []
    transitions = 0
    for c in s:
        if c == "[":
            if transitions != rows:
                logging.info("WRONG: ROW WITHOUT COMMA")
                return False
            par_stack.append(c)
        elif c == "]":
            if len(par_stack) == 0:
                logging.info("WRONG: UNMATCHED PARS")
                return False
            else:
                par_stack.pop()
            if len(par_stack) == 0:
                transitions = transitions + 1
                if max_cols == 0 and cols > 0:
                    max_cols = cols
                elif max_cols != cols:
                    logging.info("WRONG: COLS DIFFER")
                    return False
                cols = 0
        elif c == ",":
            if len(par_stack) == 1 and par_stack[-1] == "[":
                cols = cols + 1
            elif len(par_stack) == 0:
                rows = rows + 1
                if transitions != rows:
                    logging.info("WRONG: NO OPEN-CLOSE PAR BETWEEN TWO COMMAS")
                    return False
    if len(par_stack) != 0:
        logging.info("WRONG: UNMATCHED PARS")
        return False
    elif rows == 0 or transitions - rows != 1:
        logging.info("WRONG: MISSING COMMA OR EMPTY ROW")
        return False
    return True


def get_mat(s: str, p: re.Pattern):
    s = re.sub(p, "", s)
    stack_par = []
    mat = ""
    for c in s:
        if c == "[":
            stack_par.append(c)
            if len(stack_par) > 1:
                mat = mat + "\\left" + c
        elif c == "]":
            stack_par.pop()
            if len(stack_par) > 0:
                mat = mat + "\\right" + c
        elif c == "," and len(stack_par) == 1:
            mat = mat + " & "
        elif c == "," and len(stack_par) == 0:
            mat = mat + " \\\\ "
        else:
            if len(stack_par) > 0:
                mat = mat + c
    return mat
