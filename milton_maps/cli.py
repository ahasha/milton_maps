
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


def main():
    """Console script command routing for milton_maps."""

    argv = sys.argv[1:]
    arguments = docopt(__doc__, argv)
    command = arguments['CMD'][0]
    if command == "process_assessor_db":
        process_assessor_db.main(argv)
    elif command == "process_town_boundaries":
        process_town_boundaries.main(argv)
    elif command == "process_openspace":
        process_openspace.main(argv)
    else:
        print(arguments)
        raise ValueError(f"CMD {command} unrecognized.")


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
