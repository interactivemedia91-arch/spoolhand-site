"""Copy the app's reference data and golden vectors into data/, so the site's tests run on committed copies.

Usage: python3 -I tools/sync.py [--app ~/Code/pipefitter]
"""

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILES = {
    "Packages/SpoolCore/Sources/SpoolCore/Resources/reference-data.json": "data/reference-data.json",
    "Packages/SpoolCore/Tests/SpoolCoreTests/Golden/fit.json": "data/golden/fit.json",
    "Packages/SpoolCore/Tests/SpoolCoreTests/Golden/fit/offset.json": "data/golden/offset.json",
    "Packages/SpoolCore/Tests/SpoolCoreTests/Golden/fit/rolling-offset.json": "data/golden/rolling-offset.json",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--app", default=str(Path.home() / "Code/pipefitter"))
    app = Path(parser.parse_args().app)
    for source, target in FILES.items():
        destination = ROOT / target
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(app / source, destination)
        print(f"synced {target}")


if __name__ == "__main__":
    main()
