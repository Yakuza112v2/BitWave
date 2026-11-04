import sys

if "--library-worker" in sys.argv[1:]:
    # The library scanner process (see bitwave.library_worker), decided before
    # the app's own imports: the scanner must never load Qt.
    from bitwave.library_worker import main as worker_main

    raise SystemExit(worker_main(sys.argv[1:]))

from .app import bitwave_activate

raise SystemExit(bitwave_activate())
