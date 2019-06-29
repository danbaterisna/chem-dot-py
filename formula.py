import periodic_table

validElemList = [atom.symbol for atom in periodic_table.ptable.aList]

class UnrecognizedElementException(Exception):
    pass

class UnbalancedParensException(Exception):
    pass

class FormulaComponent:
    """A more workable representation for chemical formulas.
        self.comps - either a str with an elemental symbol, or a list denoting the
            components of the formula
        self.count - number of copies of self.comps in the formula"""
    def __init__(self, comps, count):
        self.comps = comps
        self.count = count
    def __str__(self):
        if isinstance(self.comps, str):
            return f"{self.comps}{self.count if self.count > 1 else ''}"
        parts = ''.join(str(comp) for comp in self.comps)
        if self.count == 1:
            return parts
        else:
            return f"({parts}){self.count}"
    def __repr__(self):
        return self.__str__()

class Formula:
    # sets for parsing
    """A class for working with and parsing formulas."""
    __numerics = "0123456789"
    __parens = "()"
    def __init__(self, form):
        self.form = form
        self.cptr = 0
    def __repr__(self):
        return f"Formula({self.form}, {self.cptr})"
    def __str__(self):
        return f"{self.form} (currently at {self.cptr})"
    def isFinished(self):
        return self.cptr == len(self.form)
    def parseElement(self):
        # reads the input stream until a numeric or parens is reached
        if self.cptr == len(self.form) or not self.form[self.cptr].isupper():
            return None
        else:
            result = self.form[self.cptr]
            self.cptr += 1
            while (self.cptr < len(self.form) and \
                   self.form[self.cptr] not in self.__numerics + self.__parens and \
                   not self.form[self.cptr].isupper()):
                result += self.form[self.cptr]
                self.cptr += 1
            if result not in validElemList:
                raise UnrecognizedElementException(f"Unrecognized element {result}")
            return result
    def parseNumber(self):
        # reads input until i run out of numerics
        if self.cptr == len(self.form):
            return 1
        elif self.form[self.cptr] not in self.__numerics:
            return 1
        else:
            number = ""
            while (self.cptr < len(self.form) and self.form[self.cptr] in self.__numerics):
                number += self.form[self.cptr]
                self.cptr += 1
            return int(number)
    def parseFormula(self):
        # Returns a list of FormulaComponent objects that represents the formula.
        result = []
        while not self.isFinished():
            result.append(self.parsePair())
        return result
    def parsePair(self):
        # Returns a FormulaComponent object that represents the next pair.
        if self.cptr == len(self.form):
            return None
        if self.form[self.cptr] == '(':
            # the recursive case
            subFormula = ""
            remainingOpen = 1
            self.cptr += 1
            while self.cptr < len(self.form) and remainingOpen > 0:
                subFormula += self.form[self.cptr]
                if self.form[self.cptr] == ')':
                    remainingOpen -= 1
                elif self.form[self.cptr] == '(':
                    remainingOpen += 1
                self.cptr += 1
            if remainingOpen > 0:
                raise UnbalancedParensException(f"Expecting more closing parens")
            fnum = self.parseNumber()
            subFormula = subFormula[:-1] # remove the trailing close parens
            return FormulaComponent(Formula(subFormula).parseFormula(), fnum)
        elif self.form[self.cptr] == ')':
            raise UnbalancedParensException(f"Unexpected closing parens")
        else:
            # the base case
            return FormulaComponent(self.parseElement(), self.parseNumber())

