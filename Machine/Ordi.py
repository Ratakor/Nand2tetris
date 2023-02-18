from Mot import *
from Mém import *
from Proc import *
from Périph import *


class ordinateur:

    def __init__(self):
        self.CPU = CPU()
        self.RAM = ramfake() #ram(32768)
        self.ROM = ramfake() #ram(32768)
        self.zéro = (0,)*self.CPU.D.TAILLE
        self.adrzéro = self.zéro[:-1]

    def __str__(self):
        return "CPU:" + str(self.CPU) + \
             "\nROM:" + self.ROM.dump(self.adrzéro, 32) + \
             "\nRAM:" + self.RAM.dump(self.adrzéro, 32)

    def _execute(self, instruction, inM, reset):

        writeM, outM, addressM, pc = self.CPU.exec(instruction, inM, reset)
        self.RAM.set(writeM, outM, addressM)
        inM = self.RAM.probe(addressM)
        instruction = self.ROM.probe(pc)
        reset = 0
        return pc, instruction, inM, reset

    def reset(self, trace, pasàpas):

        # inconnu et inconséquent
        inM = self.zéro
        instruction = self.zéro
        reset = 1

        # Remarque: la valeur de pc n'a pas à être initialisée (inconnu et inconséquent)
        # et la boucle devrait être infinie mais une condition d'arrêt arbitraire (pc tout 1)
        # est définie pour la simulation
        pc = self.adrzéro
        while pc != (1,)*len(pc):

            pc, instruction, inM, reset = self._execute(instruction, inM, reset)

            # Uniquement pour la simulation, ne fait pas partie de la logique du circuit
            if trace:
                print(self.CPU)
            if pasàpas:
                input("prochain pas ?")

    ##### Utilitaires #####
    def loadrom(self, programme):
        self.ROM.store(programme, self.adrzéro)

    def loadram(self, données):
        self.RAM.store(données, self.adrzéro)


class ordinateurIO(ordinateur):

    def __init__(self):
        super().__init__()
        self.IO = IO()

    def _execute(self, instruction, inM, reset):

        writeM, outM, addressM, pc = self.CPU.exec(instruction, inM, reset)
        RAMwriteM, RAMinM, RAMaddrM, DISPwriteM, DISPinM, DISPaddrM = chipsetIN(writeM, outM, addressM)
        self.RAM.set(RAMwriteM, RAMinM, RAMaddrM)
        self.IO.set(DISPwriteM, DISPinM, DISPaddrM)
        inM = chipsetOUT(addressM, self.RAM.probe(RAMaddrM), self.IO.probe(DISPaddrM), self.IO.key())
        instruction = self.ROM.probe(pc)
        reset = 0
        return pc, instruction, inM, reset
