
"""Usage: milton_maps CMD ...

Arguments:
  CMD
Options:
  -h --help
"""
import sys
from docopt import docopt
from milton_maps import process_assessor_db


def main():
    """Console script for milton_maps."""

    argv = sys.argv[1:]
    arguments = docopt(__doc__, argv)
    command = arguments['CMD'][0]
    if command == "process_assessor_db":
        process_assessor_db.main(argv)
    else:
        print(arguments)
        raise ValueError(f"CMD {command} unrecognized.")


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
