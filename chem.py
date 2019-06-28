import argparse
import moles, periodic_table

def moleHandler(args):
    if args.grams is None and args.moles is None:
        # find molar mass
        print(f"{moles.molarMass(args.COMPOUND)} g/mol")
    elif args.grams is None:
        # convert m to g
        print(f"{args.moles * moles.molarMass(args.COMPOUND):.{args.precision}f} g")
    else:
        # convert m to g
        print(f"{args.grams / moles.molarMass(args.COMPOUND):.{args.precision}f} mol")

def ptableHandler(args):
    result = None
    if not (args.atomic_number is None):
        result = periodic_table.ptable.getByNumber(args.atomic_number)
    elif not (args.symbol is None):
        result = periodic_table.ptable.getBySymbol(args.symbol)
    else:
        result = periodic_table.ptable.getByName(args.name.capitalize())
    if result:
        print(result.verbose_repr())
    else:
        print("No such element found")

parser = argparse.ArgumentParser(description = "A suite of chemistry-related utilities.")
subparsers = parser.add_subparsers(help="which computation to perform")
subparsers.required = True
subparsers.dest = "MAIN_COMMAND"

mole_parser = subparsers.add_parser("mole", description = """Utilities related to molar conversions.

Given the -g option, it finds the number of moles in GRAMS grams of the compound.
Given the -m option, it finds the number of grams in MOLES moles of the compound.
Given neither, it finds the molar mass of the compound.""")

mole_group = mole_parser.add_mutually_exclusive_group()
mole_group.add_argument("-g", "--grams", type=float, help="amount of COMPOUND in grams")
mole_group.add_argument("-m", "--moles", type=float, help="amount of COMPOUNT in moles")
mole_parser.add_argument("-p", "--precision", type=int, help="Digits to round off the answer to.", default = 6)
mole_parser.add_argument("COMPOUND", type=str, help="The compound to convert.")
mole_parser.set_defaults(func=moleHandler);

ptable_parser = subparsers.add_parser("ptable", description = """Utility for periodic table-based lookups.

Given the -a option, finds an element with that atomic number.
Given the -s option, finds an element with that symbol.
Given the -n option, it finds that element.""")
ptable_group = ptable_parser.add_mutually_exclusive_group(required = True)
ptable_group.add_argument("-a", "--atomic-number", type=int, help="Atomic number requested.")
ptable_group.add_argument("-s", "--symbol", type=str, help="Atomic number requested.")
ptable_group.add_argument("-n", "--name", type=str, help="Name of element requested.")
ptable_parser.set_defaults(func=ptableHandler)

args = parser.parse_args()
args.func(args)

