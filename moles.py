import os
import periodic_table, formula

avogadro = 6.02214076e23

# Takes in a chemical formula in standard input.
# Prints the molar mass (accurate to 2 dps) in standard output.

massByElement = dict((atom.symbol, atom.molarMass) for atom in periodic_table.ptable.aList)

def molarMass(comps):
    if isinstance(comps, str):
        compound = formula.Formula(comps.rstrip())
        comps = formula.FormulaComponent(compound.parseFormula(), 1)
    distrib = comps.getElemDistribution()
    ans = 0
    for elem, v in distrib.items():
        ans += massByElement[elem] * v
    return ans

