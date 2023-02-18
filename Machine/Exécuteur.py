from Ordi import *

def lire(nom_de_fichier):
    with open(nom_de_fichier) as fichier:
        contenu = tuple(tuple(int(ligne[position]) for position in range(1,1+16*3,3)) for ligne in fichier)
    return contenu


objet = input("Nom du programme à exécuteur ? ")
données = input("Nom des données à charger ? ")

contenu_rom = lire("..\\Programmes\\" + objet + ".mot")
print(len(contenu_rom), "instructions")

if données:
    contenu_ram = lire("..\\Programmes\\" + données + ".mot")
else:
    contenu_ram = ()
print(len(contenu_ram), "données")

ordi = ordinateurIO()
ordi.loadram(contenu_ram)
ordi.loadrom(contenu_rom)

print(ordi)
ordi.reset(trace=0,pasàpas=0)
print(ordi)
