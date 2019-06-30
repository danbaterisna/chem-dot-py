import argparse, collections, sys, os
import moles, periodic_table, compound

_precision_parser = argparse.ArgumentParser(add_help = False)
_precision_parser.add_argument("-p", "--precision", type=int, default=10, help="Number of significant figures of the answer.")

parser = argparse.ArgumentParser(description = "A suite of chemistry-related utilities.")
subparsers = parser.add_subparsers(help="which computation to perform")
subparsers.required = True
subparsers.dest = "MAIN_COMMAND"

def moleHandler(args):
    mmass = moles.molarMass(args.COMPOUND)
    if args.conv is None:
        print(f"{mmass} g/mol")
    else:
        # convert from the unit
        fmoles = None
        if args.qfrom == "grams":
            fmoles = args.quantity / mmass
        elif args.qfrom == "moles":
            fmoles = args.quantity
        else:
            fmoles = args.quantity / moles.avogadro
        if args.qto == "grams":
            print(f"{fmoles * mmass:.{args.precision}g} g")
        elif args.qto == "moles":
            print(f"{fmoles:.{args.precision}g} mol")
        elif args.qto == "items":
            print(f"{fmoles * moles.avogadro:.{args.precision}g} items")

mole_parser = subparsers.add_parser("mole", description = """Utilities related to molar conversions.

    Given the --conv option, performs the specified conversion.
    The format of the arguments are --conv [FROM] [TO] [GIVEN_FROM]
    [FROM] and [TO] are one of {grams, moles, items}. {g, m, i} are acceptable shorthands.

    Without the --conv option, returns the molar mass of the compound.""", \
    formatter_class = argparse.RawTextHelpFormatter, parents=[_precision_parser])

class MoleConvValidator(argparse.Action):
    def __call__(self, parser, args, values, option_string=None):
        shortcuts = {'g' : "grams", 'm' : "moles", 'i' : "items"}
        cFrom = shortcuts.get(values[0], values[0])
        cTo = shortcuts.get(values[1], values[1])
        if cFrom not in shortcuts.values():
            raise argparse.ArgumentTypeError(f"{cFrom} not an accepted quantity")
        elif cTo not in shortcuts.values():
            raise argparse.ArgumentTypeError(f"{cTo} not an accepted quantity")
        try:
            quantity = float(values[2])
        except ValueError:
            raise argparse.ArgumentTypeError(f"{values[2]} not a valid float value")
        setattr(args, "qfrom", cFrom)
        setattr(args, "qto", cTo)
        setattr(args, "quantity", quantity)
        setattr(args, "conv", True)

mole_parser.add_argument("-c", "--conv", nargs=3, action=MoleConvValidator, \
                         help="Converts a given quantity.")
mole_parser.add_argument("COMPOUND", type=str, help="The compound to convert.")
mole_parser.set_defaults(func=moleHandler)

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

ptable_parser = subparsers.add_parser("ptable", description = """Utility for periodic table-based lookups.

Given the -a option, finds an element with that atomic number.
Given the -s option, finds an element with that symbol.
Given the -n option, it finds that element.""", \
    formatter_class = argparse.RawTextHelpFormatter)

ptable_group = ptable_parser.add_mutually_exclusive_group(required = True)
ptable_group.add_argument("-a", "--atomic-number", type=int, help="Atomic number requested.")
ptable_group.add_argument("-s", "--symbol", type=str, help="Atomic number requested.")
ptable_group.add_argument("-n", "--name", type=str, help="Name of element requested.")
ptable_parser.set_defaults(func=ptableHandler)

def compdHandler(args):
    cpd = compound.Compound(args.COMPOUND)
    if args.COMMAND == "molec":
        print(cpd.getMolecular())
    elif args.COMMAND == "empi":
        print(cpd.getEmpirical())
    else:
        elements = cpd.getElemDistribution()
        totalMass = moles.molarMass(cpd)
        for elem, ct in elements.items():
            elemMass = periodic_table.ptable.getBySymbol(elem).molarMass
            print(f"{elemMass * ct * 100 / totalMass:.{args.precision}g}% {elem}")
compd_parser = subparsers.add_parser("compd", description="""Utilities for compound properties.

The -p option is ignored if the output is not numeric.
""", parents=[_precision_parser])

compd_parser.add_argument("COMMAND", type=str, help="The action to perform", choices=["pcbm", "molec", "empi"])
compd_parser.add_argument("COMPOUND", type=str, help="The compound to operate on.")
compd_parser.set_defaults(func=compdHandler)

def interactHandler(args):
    while True:
        command = input("chem.py$ ")
        sub_args = parser.parse_args(command.split())
        sub_args.func(sub_args)
        # i somehow want to dodge the exit syscall
        # the above code makes.
        # this is my best current guess, although
        # you can do shell injection with this.
        # os.system("python3 chem.py " + command)

interact_parser = subparsers.add_parser("interact", description="""Enter interactive mode.

In interactive mode, one can directly enter commands without `python chem.py`.
However, only those commands will be available.

Note that if an invalid command is entered, or if any  -h option
is invoked, then chem.py will exit.""", \
    formatter_class = argparse.RawTextHelpFormatter)

interact_parser.set_defaults(func=interactHandler)

def iexitHandler(args):
    sys.exit(0)

iexit_parser = subparsers.add_parser("iexit", description="Exits interactive mode.")
iexit_parser.set_defaults(func=iexitHandler)

args = parser.parse_args()
args.func(args)

