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
    def verbose_repr(self):
        return f"""{self.fullName} ({self.symbol})
no. {self.atNumber}
{self.molarMass} g/mol
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

ptable = PeriodicTable.fromFile("ptable_data.txt")

