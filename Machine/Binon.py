# Opérations sur binons (encodés par un entier valant 0 ou 1).

# Circuit de base
def nand(a,b):
    return ((1,1),(1,0))[a][b]

# Circuits dérivés pour logique
def not_(a):
    return nand(a,a)

def and_(a,b):
    return not_(nand(a,b))

def or_(a,b):
    return nand(not_(a),not_(b))

def xor(a,b):
    return or_(and_(a,not_(b)),and_(not_(a),b))

def mux(sel,a,b):
    return or_(and_(a,not_(sel)),and_(b,sel))

def dmux(sel,inp):
    return and_(not_(sel),inp),and_(sel,inp)

def dmux4way(sel,inp):
    ab, cd = dmux(sel[1],inp)
    return dmux(sel[0],ab) + dmux(sel[0],cd)

def dmux8way(sel,inp):
    abcd, efgh = dmux(sel[2],inp)
    return dmux4way(sel[:2],abcd) + dmux4way(sel[:2],efgh)

# Circuits dérivés pour arithmétique
def halfadder(a,b):
    return xor(a,b), and_(a,b)

def fulladder(a,b,c):
    aplusb, r1 = halfadder(a,b)
    aplusbplusc, r2 = halfadder(aplusb,c)
    return aplusbplusc, or_(r1,r2)
