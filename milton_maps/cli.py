"""Usage: milton_maps CMD ...

Arguments:
  CMD
Options:
  -h --help
"""

import sys

from milton_maps import (
    process_assessor_db,
    process_openspace,
    process_tax_parcels,
    process_town_boundaries,
)


def main():
    """Console script command routing for milton_maps."""
    cmd = sys.argv[1]
    argv = sys.argv[2:]
    if cmd == "process_assessor_db":
        process_assessor_db.main(argv)
    elif cmd == "process_town_boundaries":
        process_town_boundaries.main(argv)
    elif cmd == "process_openspace":
        process_openspace.main(argv)
    elif cmd == "process_tax_parcels":
        process_tax_parcels.main(argv)
    else:
        raise ValueError(f"Command {cmd} unrecognized.")


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
