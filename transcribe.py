#!/usr/bin/env python3
"""Thin shim: `python transcribe.py ...` behaves exactly as before.

The real implementation lives in the `transcribe/` package; this file
only hands off to it. It loads the package by path because a file named
`transcribe.py` would otherwise shadow the `transcribe/` package on the
import path.

Usage:
    python transcribe.py samples/OSR_us_000_0010_8k.wav
    python transcribe.py my-audio.mp3 --model base --language en
"""

import importlib.util
import sys
from pathlib import Path


def _load_package_main():
    pkg_dir = Path(__file__).resolve().parent / "transcribe"
    spec = importlib.util.spec_from_file_location(
        "transcribe",
        pkg_dir / "__init__.py",
        submodule_search_locations=[str(pkg_dir)],
    )
    package = importlib.util.module_from_spec(spec)
    sys.modules["transcribe"] = package
    spec.loader.exec_module(package)
    from transcribe.cli import main

    return main


if __name__ == "__main__":
    raise SystemExit(_load_package_main()())
