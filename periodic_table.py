import itertools
import os

"""
Module responsible for loading data on elements.
"""

class Atom:
    def __init__(self, **kwargs):
        self.atNumber = kwargs.atNumber
        self.symbol = kwargs.symbol
        self.molarMass = kwargs.molarMass
    def __init__(self,  infoRow):
        atNumber, fullName, symb, mm = infoRow.split()
        self.atNumber = int(atNumber)
        self.fullName = fullName
        self.symbol = symb
        self.molarMass = float(mm)
    def __repr__(self):
        return f"{self.symbol}"
    def getElectronConfig(self, long=True):
        orbitals = "spdf"
        bannedPairs = ["1p", "1d", "1f", "2d", "2f", "3f"]
        electronCount = [2, 6, 10, 14]
        remainingElectrons = self.atNumber
        ePerOrbital = []
        subshellNames = []
        for i in itertools.count(0):
            if remainingElectrons == 0:
                break
            for orbitIndex in range(len(orbitals) - 1, -1, -1):
                shellNum = i - orbitIndex + 1
                if shellNum <= 0 or str(shellNum) + orbitals[orbitIndex] in bannedPairs:
                    continue
                subshellNames.append(str(shellNum) + orbitals[orbitIndex])
                ePerOrbital.append(min(remainingElectrons, electronCount[orbitIndex]))
                remainingElectrons -= ePerOrbital[-1]
                if remainingElectrons == 0:
                    break
        if long:
            return list(map(lambda x: x[1] + str(x[0]), zip(ePerOrbital, subshellNames)))
        else:
            breakOrbitals = []


    def verbose_repr(self):
        return f"""
    {self.fullName} ({self.symbol})
    no. {self.atNumber}
    {self.molarMass} g/mol
    Long configuration:
        {'.'.join(self.getElectronConfig())}
       """

class PeriodicTable:
    def __init__(self, atomList):
        self.aList = atomList
    @staticmethod
    def fromFile(fileName):
        result = PeriodicTable([])
        with open(fileName) as pfile:
            for line in pfile:
                line = line.rstrip()
                if line == "":
                    continue
                result.aList.append(Atom(line))
        return result
    def getBySymbol(self,sym):
        for atom in self.aList:
            if atom.symbol == sym:
                return atom
        return None
    def getByNumber(self,num):
        for atom in self.aList:
            if atom.atNumber == num:
                return atom
        return None
    def getByName(self,name):
        for atom in self.aList:
            if atom.fullName == name:
                return atom
        return None

scriptDir = os.path.dirname(__file__)

ptable = PeriodicTable.fromFile(os.path.join(scriptDir, "ptable_data.txt"))

