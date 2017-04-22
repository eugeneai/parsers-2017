import re

B=0x11000

FOR = B
TO = B-1
DO = B-2
ID = B-3
NUMBER = ID-1
OP = ID-2
ASSIGN = OP-1

FOR_N=ASSIGN-1

LEX={
    "for": FOR,
    "to": TO,
    "do": DO,
    "[a-z_][a-z_0-9]*": ID,
    "\d*\.?\d+": NUMBER,
    ":=": ASSIGN,
    "[\+\-\*/]": OP
}

class Tray(object):
    pass

tray=Tray()
tray.val=None

def lex():
    l=tray.l
    l=l.lstrip() # Pascal ignore spaces between symbols
    for regexp, lex in LEX.items():
        m = re.match(regexp, l)
        if m:
            ls = re.split(regexp, l, maxsplit=1)
            if len(ls)>1 and ls[0]=="":
                tray.l=ls[1]
                tray.val=m.group(0)
                print(tray.val)
                return lex
    raise RuntimeErrror("should not get here")

def get():
    return tray.l.lstrip()[0]

def tr():
    l=tray.l
    l=l.lstrip() # Pascal ignore spaces between symbols
    for regexp, lex in LEX.items():
        ls = re.split(regexp, l, maxsplit=1)
        if len(ls)>1 and ls[0]=="":
            return lex
    raise RuntimeErrror("should not get here")

    

def trans_for():
    if lex() != FOR:
        return
    rc1=trans_assign()
    if rc1 is None:
        return
    if lex() != TO:
        return
    rc2=trans_exp()
    if rc2 is None:
        return
    if lex() == DO:
        return {"OP":"FOR",
                "ASSIGN": rc1,
                "TERM": rc2
        }


def trans_assign():
    if lex()!=ID:
        return
    id = tray.val
    if lex()!=ASSIGN:
        return
    return {
        "ID":id,
        "EXP":trans_exp()
    }

def trans_exp():
    acc=None
    op=None
    while True:
        o2 = trans_mult()
        if o2 is None:
            return
        if op == "+":
            acc+=o2
        elif op=="-":
            acc-=o2
        else:
            acc=o2
        op=get()
        if op in "+-":
            lex()
        else:
            return acc

def trans_mult():
    acc=None
    op=None
    while True:
        operand2=trans_term()
        if operand2 is None:
            return
        if op == "*":
            acc = acc*operand2
        elif op == "/":
            acc = acc/operand2
        else:
            acc = operand2
        op = get()
        if op in "*/":
            lex()
        else:
            return acc
        
def trans_term():
    #if tr()==ID:
    #    lex()
    #    return True
    if tr()==NUMBER:
        lex()
        return float(tray.val)
    return


vars={}

def main():
    IN = "for i:=1 to 20 do"
    tray.l = IN
    answer = trans_for()
    print(answer)
    vars[answer["ASSIGN"]["ID"]]=answer["ASSIGN"]["EXP"]
    term = answer["TERM"]
    forvar = answer["ASSIGN"]["ID"]
    while True:
        if vars[forvar] > term:
            break
        print(vars[forvar])
        vars[forvar]=vars[forvar]+1
    

main()


# BISON + FLEX YACC+LEX
# ANTLR
# 
