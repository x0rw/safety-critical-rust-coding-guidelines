#!/usr/bin/env python3
# SPDX-License-Identifier: MIT OR Apache-2.0
# SPDX-FileCopyrightText: The Coding Guidelines Subcommittee Contributors

# Convenience script to build Sphinx books, including setting up a Python
# virtual environment to install Sphinx into (removing the need to manage
# dependencies globally). Each book should have a `make.py` script that updates
# the submodules, import this shared module, and calls the main function here.

from pathlib import Path
import argparse
import subprocess
import sys


# Automatically watch the following extra directories when --serve is used.
EXTRA_WATCH_DIRS = ["exts", "themes"]


def build_docs(root, builder, clear, serve, debug, offline):
    dest = root / "build"

    args = ["-b", builder, "-d", dest / "doctrees"]

    if offline:  
        args.append("-D")
        args.append("offline=1")
    if debug:
        # Disable parallel builds and show exceptions in debug mode.
        #
        # We can't show exceptions in parallel mode because in parallel mode
        # all exceptions will be swallowed up by Python's multiprocessing.
        # That's also why we don't show exceptions outside of debug mode.
        args += ["-j", "1", "-T"]
    else:
        # Enable parallel builds:
        args += ["-j", "auto"]
    if clear:
        args.append("-E")
    if serve:
        for extra_watch_dir in EXTRA_WATCH_DIRS:
            extra_watch_dir = root / extra_watch_dir
            if extra_watch_dir.exists():
                args += ["--watch", extra_watch_dir]
    else:
        # Error out at the *end* of the build if there are warnings:
        args += ["-W", "--keep-going"]

    try:
        subprocess.run(
            [
                "sphinx-autobuild" if serve else "sphinx-build",
                *args,
                root / "src",
                dest / builder,
            ],
            check=True,
        )
    except KeyboardInterrupt:
        exit(1)
    except subprocess.CalledProcessError:
        print("\nhint: if you see an exception, pass --debug to see the full traceback")
        exit(1)

    return dest / builder

def main(root):
    root = Path(root)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--clear", help="disable incremental builds", action="store_true"
    )
    parser.add_argument(
        "-o",
        "--offline",
        help="build in offline mode",
        action="store_true",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-s",
        "--serve",
        help="start a local server with live reload",
        action="store_true",
    )
    group.add_argument(
        "--check-links", help="Check whether all links are valid", action="store_true"
    )
    group.add_argument(
        "--xml", help="Generate Sphinx XML rather than HTML", action="store_true"
    )
    group.add_argument(
        "--debug",
        help="Debug mode for the extensions, showing exceptions",
        action="store_true",
    )
    args = parser.parse_args()

    rendered = build_docs(
        root, "xml" if args.xml else "html", args.clear, args.serve, args.debug, args.offline
    )

