from Mot import *
from Mém import *

# Opérateur logique et arithmétique
def ALU(x,y,zx,nx,zy,ny,f,no):
    zero = (0,)*len(x)
    x1 = mux16(zx, x, zero)
    x2 = mux16(nx, x1, not16(x1))
    y1 = mux16(zy, y, zero)
    y2 = mux16(ny, y1, not16(y1))
    xfy = mux16(f, and16(x2,y2), add16(x2,y2))
    out = mux16(no, xfy, not16(xfy))
    ng = out[15]
    zr = not_(or16way(out))
    return out, zr, ng

# Cellule de traitement contenant des registres donc ce doit être une classe car elle retient des données
class CPU:

    def __init__(self):
        self.A = registre()
        self.D = registre()
        self.PC = compteur()

    def __str__(self):
        return "A:"+str(self.A)+", D:"+str(self.D)+", PC:"+str(self.PC)

    def exec(self, instruction, inM, reset):

        jp, jz, jn, destM, destD, destA, no, f, ny, zy, nx, zx, mem, _, _, calcul = instruction

        outALU = (0,)*len(inM) # inconnu mais inconséquent
        inA = mux16(not_(calcul), outALU, instruction)
        self.A.set(not_(calcul), inA)

        x = self.D.probe()
        y = mux16(mem, self.A.probe(), inM)
        outALU, zr, ng = ALU(x,y,zx,nx,zy,ny,f,no)

        inA = mux16(not_(calcul), outALU, instruction)
        self.A.set(and_(calcul, destA), inA)
        self.D.set(and_(calcul, destD), outALU)

        outA = self.A.probe()

        ps = and_(not_(ng), not_(zr))
        jpos = and_(jp, ps)
        jzer = and_(jz, zr)
        jneg = and_(jn, ng)
        jump = and_(calcul, or_(jneg, or_(jpos, jzer)))
        self.PC.set(reset, jump, not_(jump), outA)

        outM = outALU
        writeM = and_(calcul, destM)
        addressM = outA[:-1]
        pc = self.PC.probe()[:-1]

        return writeM, outM, addressM, pc
