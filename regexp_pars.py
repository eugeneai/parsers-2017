# Finite state automat

import re

ID=re.compile("[a-z_]([a-z]|[0-9])*")
FIO=re.compile("^.*?((\w{3,})\s+(\w{2,}))\s+(\w{2,})?$") # \w = [a-zA-Z], \d=[0-9] \s=[ \t]


m = FIO.match("  Черкашин    Евгений   ")
print(m.groups())
print(m.group(1))
print(m.group(2), m.group(3))


# 1234 1234 



alpha="qwertyuiopasd_fghjklzxcvbnm"
digit="1234567890"
A=[
    (0, alpha, 1),
    (1, alpha+digit, 1)
]

def translate(string, automat, start, stop):
    Q = start
    for s in string:
        for (q, a, qn) in automat:
            if q==Q and s in a:
                Q=qn
                break
        else:
            return False
    return Q in stop
            

# print(translate("qwertt3423465234fjkh123h1kjh4gj2", A, 0, [1]))
# print(translate("64564546qwertt3423465234fjkh123h1kjh4gj2", A, 0, [1]))
# print(ID.match("qwe234"))
# print(ID.match("234oiuoi"))

