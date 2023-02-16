
"""Usage: milton_maps CMD ...

Arguments:
  CMD
Options:
  -h --help
"""

import sys
from docopt import docopt
from milton_maps import process_assessor_db
from milton_maps import process_town_boundaries
from milton_maps import process_openspace
from milton_maps import process_tax_parcels

def main():
    """Console script command routing for milton_maps."""

    argv = sys.argv[1:]
    #arguments = docopt(__doc__, argv)
    command = sys.argv[1]
    if command == "process_assessor_db":
        process_assessor_db.main(argv)
    elif command == "process_town_boundaries":
        process_town_boundaries.main(argv)
    elif command == "process_openspace":
        process_openspace.main(argv)
    elif command == "process_tax_parcels":
        process_tax_parcels.main(argv)
    else:
        raise ValueError(f"Command {command} unrecognized.")


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
