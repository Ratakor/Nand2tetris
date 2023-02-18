# assembleur

vc = 16

def traduire_A(instr):
    # traduit une instruction du genre @nombre en le nombre avec le plus fort binon à zéro
    # (donc nombre est compris entre 0 et 32767)
    # par exemple @0 donnera 0000 0000 0000 0000 soit (0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0)
    # par exemple @21 donnera 0000 0000 0001 0101 soit (1,0,1,0, 1,0,0,0, 0,0,0,0, 0,0,0,0)
    # par exemple @32767 donnera 0111 1111 1111 1111 soit (1,1,1,1, 1,1,1,1, 1,1,1,1, 1,1,1,0)

    # nombre ou symbole, @21 ou @étiquette
    global vc
    param = instr[1:]
    if param.isdigit():
        nombre = int(param)
    else:
        try:
            nombre = symboles[param]
        except KeyError:
            nombre = vc
            symboles[param] = nombre
            print("Ajoute symbole " + param + " avec valeur " + str(nombre))
            vc += 1

    bin = format(nombre, '016b') # format(21) -> "0000000000010101"
    liste = []
    for chiffre in bin[::-1]:
        liste.append(int(chiffre))
    return tuple(liste)

"""
def traduire_A(instr):
    nombre = int(instr[1;])
    return tuple(int(chiffre) for chiffre in format(nombre, '016b')[::-1])
"""
dests = {
#   ""      : (0,0,0),
    "M"     : (1,0,0),
    "D"     : (0,1,0),
    "MD"    : (1,1,0),
    "A"     : (0,0,1),
    "AM"    : (1,0,1),
    "AD"    : (0,1,1),
    "AMD"   : (1,1,1)
}

sauts = {
#   ""      : (0,0,0),
    "JGT"   : (1,0,0),
    "JEQ"   : (0,1,0),
    "JGE"   : (1,1,0),
    "JLT"   : (0,0,1),
    "JNE"   : (1,0,1),
    "JLE"   : (0,1,1),
    "JMP"   : (1,1,1)
}

calculs = {
    "0"     : (0,1,0,1,0,1,0),
    "1"     : (1,1,1,1,1,1,0),
    "-1"    : (0,1,0,1,1,1,0),
    "D"     : (0,0,1,1,0,0,0),
    "A"     : (0,0,0,0,1,1,0),
    "M"     : (0,0,0,0,1,1,1),
    "!D"    : (1,0,1,1,0,0,0),
    "!A"    : (1,0,0,0,1,1,0),
    "!M"    : (1,0,0,0,1,1,1),
    "-D"    : (1,1,1,1,0,0,0),
    "-A"    : (1,1,0,0,1,1,0),
    "-M"    : (1,1,0,0,1,1,1),
    "D+1"   : (1,1,1,1,1,0,0),
    "A+1"   : (1,1,1,0,1,1,0),
    "M+1"   : (1,1,1,0,1,1,1),
    "D-1"   : (0,1,1,1,0,0,0),
    "A-1"   : (0,1,0,0,1,1,0),
    "M-1"   : (0,1,0,0,1,1,1),
    "D+A"   : (0,1,0,0,0,0,0),
    "D+M"   : (0,1,0,0,0,0,1),
    "D-A"   : (1,1,0,0,1,0,0),
    "D-M"   : (1,1,0,0,1,0,1),
    "A-D"   : (1,1,1,0,0,0,0),
    "M-D"   : (1,1,1,0,0,0,1),
    "D&A"   : (0,0,0,0,0,0,0),
    "D&M"   : (0,0,0,0,0,0,1),
    "D|A"   : (1,0,1,0,1,0,0),
    "D|M"   : (1,0,1,0,1,0,1)
}

symboles = {
    "R0"    :   0,
    "R1"    :   1,
    "R2"    :   2,
    "R3"    :   3,
    "R4"    :   4,
    "R5"    :   5,
    "R6"    :   6,
    "R7"    :   7,
    "R8"    :   8,
    "R9"    :   9,
    "R10"   :   10,
    "R11"   :   11,
    "R12"   :   12,
    "R13"   :   13,
    "R14"   :   14,
    "R15"   :   15
}

pc = 0

def traduire_C(instr):
    # traduit uns instruction du genre dest=calcul;saut avec dest et saut optionels
    # donc du genre
    #   calcul
    #   dest=calcul
    #   calcul;saut
    #   dest=calcul;saut
    # l'encodage est (111 calcul dest saut)

    éléments = instr.split('=') # "D+1;JEQ" -> ("D+1;JEQ")
    if len(éléments) == 1:
        dest = (0,0,0)
        reste = instr
    else:
        dest = dests[éléments[0]] # A -> (0,0,1)
        reste = éléments[1]

    suite = reste.split(';') # -> ("D+1","JEQ")
    if len(suite) == 1:
        saut = (0,0,0)
    else:
        saut = sauts[suite[1]]
        reste = suite[0]

    calcul = calculs[reste] # D+1 -> (1,1,1,1,1,0,0)

    return saut+dest+calcul+(1,1,1)

def résoudre_L(instr):
    global pc
    # "(étiquette)"
    # clef & valeur
    clef = instr[1:-1]
    valeur = pc
    symboles[clef] = valeur
    print("Ajoute symbole " + clef + " avec valeur " + str(valeur)) # Ajoute symbole fin avec valeur 3

def traduire(instr): # analyse sémantique
    if instr[0] == '(':
        return None
    elif instr[0] == '@':
        return traduire_A(instr)
    else:
        return traduire_C(instr)

def extraire(ligne): # analyse lexicale
    instr = ""
    peutetre_commentaire = False

    for lettre in ligne:
        if lettre == '/':
            if peutetre_commentaire:
                break
            else:
                peutetre_commentaire = True
        elif lettre == ' ' or lettre == '\n':
            continue
        else:
            if peutetre_commentaire:
                peutetre_commentaire = False
                instr += '/'
            instr += lettre

    return instr

def vérifier(instr): # analyse syntaxique
    return instr

def résoudre(instr):
    global pc
    if instr[0] == '(':
        return résoudre_L(instr)
    else:
        pc += 1

def assemble(nom_source, nom_objet):

    with open(nom_source) as fichier:
        source = fichier.readlines()

    # permière passe, résolution des symboles
    for ligne in source:
        instr = extraire(ligne)
        if instr:
            résoudre(instr)

    # deuxième passe, traduction des instructions
    objet=[]
    for ligne in source:
        instr = extraire(ligne)
        if instr:
            if not vérifier(instr):
                # erreur dans le programme source
                exit(0)
            code = traduire(instr)
            if code:
                objet.append(code)

    with open(nom_objet, "w") as fichier:
        fichier.writelines(str(code)+'\n' for code in objet)

def main():
    src, obj = input("src : "), input("obj : ")
    assemble(src,obj)

main()

"""
// second essai
    @fin        # équiv. à @7                           # addr instr 0 pc (program counter)
// instruction plus difficile
    D=D-1;JEQ // décrémente D et saute si c'est nul     # addr instr 1
// instruction finale
    D=0 // remet D à zéro                               # addr instr 2
    @temp                                               # addr instr 3, addr mémoire 16
    M=D                                                 # addr instr 4
    @temp2                                              # addr instr 5, addr mémoire 17
    M=D                                                 # addr instr 6
    @temp                                               # addr instr 7, addr mémoire 16
    M=D                                                 # addr instr 8
(fin)                                                   # donc fin vaut 9
(autrefin)                                              # donc autrefin vaut 9

======

(1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0)
(0,1,0,0,1,0,0,1,1,1,0,0,0,1,1,1)
(0,0,0,0,1,0,0,1,0,1,0,1,0,1,1,1)
(0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0)
(1,0,0,0,0,0,0,0,1,1,0,0,0,1,1,1)
(1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0)
(1,0,0,0,0,0,0,0,1,1,0,0,0,1,1,1)
(0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0)
(1,0,0,0,0,0,0,0,1,1,0,0,0,1,1,1)
"""
