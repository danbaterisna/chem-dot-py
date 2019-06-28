import argparse, collections
import moles, periodic_table

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

    Given the --conv option, performs the specified conversion.
    The format of the arguments are --conv [FROM] [TO] [GIVEN_FROM]
    [FROM] and [TO] are one of {grams, moles, items}. {g, m, i} are acceptable shorthands.

    Without the --conv option, returns the molar mass of the compound.""", \
    formatter_class = argparse.RawTextHelpFormatter)

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
mole_parser.add_argument("-p", "--precision", type=int, help="Significant figures in the output.", default=20)
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


