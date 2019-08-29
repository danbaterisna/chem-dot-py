from functools import reduce
from math import gcd
import formula

class Compound(formula.FormulaComponent):
    def __init__(self, form):
        cplist = form
        if isinstance(form, str):
            cplist = formula.Formula(form).parseFormula()
            cplist = formula.FormulaComponent(cplist, 1)
        elif isinstance(form, list):
            cplist = formula.FormulaComponent(cplist, 1)
        if isinstance(cplist.comps, list):
            self.comps = [Compound(fc) for fc in cplist.comps]
            self.count = cplist.count
        else:
            self.comps = cplist.comps
            self.count = cplist.count
    def getElemDistribution(self):
        """Returns a dict representing the molecular formula."""
        if isinstance(self.comps, str):
            # this is a root
            return {self.comps: self.count}
        else:
            # yeet
            result = dict()
            for subForm in self.comps:
                for k, v in subForm.getElemDistribution().items():
                    if k not in result.keys():
                        result[k] = 0
                    result[k] += v
            afterMult = dict()
            for k, v in result.items():
                afterMult[k] = v * self.count
            return afterMult
    def getMolecular(self):
        eDistrib = self.getElemDistribution()
        return Compound([f"{elem}{int(count)}" for elem, count in eDistrib.items()])
    def getEmpirical(self):
        eDistrib = self.getElemDistribution()
        divFactor = reduce(gcd, eDistrib.values())
        return Compound([f"{elem}{int(count)//divFactor}" for elem, count in eDistrib.items()])

