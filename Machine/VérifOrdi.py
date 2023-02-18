import time
from Ordi import *



# Vérification sur un exemple
print("programme Add2 : RAM[2]=RAM[0]+RAM[1]")
programme = ((0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0),
             (0,0,0,0, 1,0,0,0, 0,0,1,1, 1,1,1,1),
             (1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0),
             (0,0,0,0, 1,0,0,1, 0,0,0,0, 1,1,1,1),
             (0,1,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0),
             (0,0,0,1, 0,0,0,0, 1,1,0,0, 0,1,1,1),
             (1,1,1,1, 1,1,1,1, 1,1,1,1, 1,1,1,0),
             (1,1,1,0, 0,0,0,1, 0,1,0,1, 0,1,1,1))
données = ((1,1,1,1, 0,0,0,0, 0,0,0,0, 0,0,0,0), (1,0,0,1, 0,0,0,0, 0,0,0,0, 0,0,0,0))
sortie = " 000F 0009 0018 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000"

for typeordi in (ordinateur, ordinateurIO):
    print(typeordi.__name__)
    ordi = typeordi()
    print(ordi)

    ordi.loadp(programme)
    print(ordi)

    ordi.loadd(données)
    print(ordi)

    print("c'est parti")
    ordi.reset(trace=1,pasàpas=0)

    print(ordi)
    assert str(ordi).partition("RAM:0000:")[2] == sortie
