from Mot import *

# Rétention de valeurs.
# Il ne s'agit plus de simples fonctions mais de mécanismes qui gardent des valeurs.
# Il faut donc utiliser des objets et donc définir les classes correspondantes.

# Rétention d'un binon
class binon:

    def __init__(self):
        self.val = 0

    def __str__(self):
        return str(self.val)

    def probe(self):
        return self.val

    def set(self, load, inp):
        self.val = mux(load, self.val, inp)

# Rétention d'un mot
class registre:

    # Remarque: contrairement aux fonctions de Mot, 16 est fixé car il faut garder une donnée
    # (et donc connaître sa taille) et non simplement faire un calcul dessus
    TAILLE = 16 # en binons

    def __init__(self):
        # Remarque: (binon(),)*registre.TAILLE donnerait TAILLE fois le MÊME binon
        self.binons = tuple(binon() for _ in range(registre.TAILLE))

    def __str__(self):
        return hexa(self.probe())

    # Remarque: le paramètre adresse permet d'éviter un cas particulier dans l'objet ram
    def probe(self, adresse=None):
        return tuple(b.probe() for b in self.binons)

    def set(self, load, inp, adresse=None):
        for b,val in zip(self.binons, inp):
            b.set(load, val)


# Rétention d'un mot avec comportement spécial
class compteur(registre):

    def set(self, reset, load, inc, inp):
        actuel = self.probe()
        plus1 = inc16(actuel)
        zero = (0,)*len(actuel)
        super().set(or_(reset, or_(load, inc)),
                    mux16(reset,
                        mux16(load,
                            mux16(inc, actuel,
                            plus1),
                        inp),
                    zero))


# Rétention d'un groupe de mots
#
# Une RAM est composée de blocs qui peuvent eux-même être des RAMs plus petites et finalement
# de simples registres.
# Remarque: L'adresse d'un registre est décomposée en binons d'ordre supérieur qui désignent
# le bloc et le restant qui désigne l'adresse du registre dans le bloc.

class ram:

    # Nombre de blocs adressables en fonction de la taille de l'adresse en binons
    TAILLE_ADRESSE = 3
    NUM_BLOCS = 2**TAILLE_ADRESSE

    def __init__(self, quantité): # en registres
        # La quantité totale de registres doit pouvoir être répartie entre les blocs
        assert quantité % ram.NUM_BLOCS == 0
        self.taille_bloc = quantité // ram.NUM_BLOCS

        # Chaque bloc est soit un registre, soit une RAM plus petite (récursion)
        self.blocs = tuple((registre() if self.taille_bloc==1 else ram(self.taille_bloc)) for _ in range(ram.NUM_BLOCS))

    def __str__(self):
        chaîne = "$"+str(self.taille_bloc)+":\n"
        for bloc in self.blocs:
            chaîne += str(bloc) + " "
        chaîne += "\n:"+str(self.taille_bloc)+"$\n"
        return chaîne

    def probe(self, adresse):
        # Les binons supérieurs (donc en fin de tuple) permettent de sélectioner un bloc
        # et les binons restants désignent l'adresse dans ce bloc (récursion)
        return mux8way16(adresse[-ram.TAILLE_ADRESSE:], *(bloc.probe(adresse[:-ram.TAILLE_ADRESSE]) for bloc in self.blocs))

    def set(self, load, inp, address):
        loads = dmux8way(address[-ram.TAILLE_ADRESSE:], load)
        for l,bloc in zip(loads, self.blocs):
            bloc.set(l, inp, address[:-ram.TAILLE_ADRESSE])


    ##### Utilitaires #####

    # !!! REMARQUE !!!
    # Comme indiqué en tête de Mot, toutes les fonctions 16 marchent en fait
    # sur des mots de n'importe quelle longueur. On n'a donc pas besoin de
    # connaître la taille de l'adresse (qui dépend de la taille de l'objet ram)
    # pour l'incrémenter.

    def store(self, contenu, adresse):
        for x in contenu:
            self.set(1, x, adresse)
            adresse = inc16(adresse)

    def dump(self, adresse, quantité):
        chaîne = hexa(adresse) + ':'
        while quantité > 0:
            valeur = self.probe(adresse)
            chaîne += " " + hexa(valeur)
            adresse = inc16(adresse)
            quantité -= 1
        return chaîne


###### TRICHERIE POUR PERFORMANCE ######
# La définition récursive de ram est trop lente pour être utlisable.
# Cette implémentation calque l'interface de la classe ram mais utilise
# directement un tableau de registres pour éviter la récursion.
###### L'IMPLÉMENTATION NE SUIT PAS L'ÉLECTRONIQUE MAIS SE COMPORTE PAREILLEMENT ######
class ramfake(ram):

    TAILLE = 32768 # en registres, fixée à 32K mots

    def __init__(self):
        self.registres = tuple(registre() for _ in range(ramfake.TAILLE))

    def __str__(self):
        chaîne = "$RAMFAKE:"
        limite = 256
        for adr in range(limite):
            if adr % 16 == 0:
                chaîne += "\n"+f"{adr:0{4}X}"+":"
            chaîne += str(self.registres[adr])
        chaîne += "\n:RAMFAKE$\n"
        return chaîne

    def probe(self, adresse):
        adr = entier(adresse)
        return self.registres[adr].probe() if adr < ramfake.TAILLE else (0,)*16

    def set(self, load, inp, adresse):
        adr = entier(adresse)
        if load and adr < ramfake.TAILLE:
            self.registres[adr].set(load, inp)

