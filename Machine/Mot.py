from functools import reduce
from Binon import *

# Opérations sur mots (encodés par un tuple d'entiers valant 0 ou 1).
# Remarque: les fonctions ne dépendent pas de la longueur du mot,
# même si en pratique ce seront des mots de 16 binons.

# Circuits dérivés pour logique
def not16(A):
    return tuple(not_(a) for a in A)

def and16(A,B):
    return tuple(and_(a,b) for a,b in zip(A,B))

def or16(A,B):
    return tuple(or_(a,b) for a,b in zip(A,B))

def or16way(A):
    return reduce(or_, A)

def mux16(sel,A,B):
    return tuple(mux(sel,a,b) for a,b in zip(A,B))

def mux4way16(sel, A, B, C, D):
    return mux16(sel[1], mux16(sel[0], A, B), mux16(sel[0], C, D))

def mux8way16(sel, A, B, C, D, E, F, G, H):
    return mux16(sel[2], mux4way16(sel[:2], A, B, C, D), mux4way16(sel[:2], E, F, G, H))

# Circuits dérivés pour arithmétique
#
# Remarque: pour les opérations logiques, les binons d'un mot sont équivalents mais pour
# les opérations arithmétiques, le mot représente un nombre dont les binons sont les chiffres.
# Ils sont alors rangés du moins significatif au plus significatif de manière à ce que
# leur place correspondent à leur puissance.
# Par exemple: (1,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0) représente 257 avec 1 en position 0 et en
# position 8, soit 2**0 + 2**8 = 1 + 256 = 257
def add16(A,B):
    r = 0
    return tuple(résultat[0] for a,b in zip(A,B) if (résultat := fulladder(a,b,r), r := résultat[1]))

def inc16(A):
    r = 1
    return tuple(résultat[0] for a in A if (résultat := halfadder(a,r), r := résultat[1]))


##### Utilitaires #####
def entier(A):
    return reduce(lambda x,y: x*2+y, A[::-1])

def hexa(A):
    return f"{entier(A):0{4}X}"
