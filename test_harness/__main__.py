from pathlib import Path
import itertools
from typing import Dict, List
import logging
import click


@click.command()
@click.argument("source", type=click.Path(exists=True, file_okay=True, dir_okay=False))
def main(source):
    print(f"parsing {source}...")
    source = Path(source)
    out = parse(source.read_text())

    for key in out:
        target = OUTDIR / f"{key}.txt"
        print(f"emitting output file {target}")
        target.write_text("\n".join(out[key]))


TEST_START_MARKER = ">>>"

END_OF_TEST_MARKER = "<<<"

OUTDIR = Path() / "generated"

if not OUTDIR.exists():
    OUTDIR.mkdir()


def parse(raw: str) -> Dict[str, List[str]]:
    lines = raw.split("\n")
    data: Dict[str, List[str]] = {}
    lines_iter = iter(lines)
    while True:
        try:
            label = next(lines_iter)
            if not label:
                break
            if TEST_START_MARKER not in label:
                logging.fatal(f"the line {label!r} failed the sanity check (missing test marker)")
                raise AssertionError("sanity check failed.")
            label = label.replace(">", "")
            # take every line that isnt an end-of-test deliminator.
            data[label] = list(itertools.takewhile(lambda l: END_OF_TEST_MARKER not in l, lines_iter))
        except StopIteration:
            break

    return data
print("calling main...")
main()