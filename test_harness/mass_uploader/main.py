from pathlib import Path
from typing import Tuple

from loguru import logger

from .config import load_config
from .uploader import acquire_canvas_handle, mass_upload, submit_assignment, acquire_assignment
import os
import click


@click.command()
@click.argument("config", type=click.Path(file_okay=True, dir_okay=False, exists=True))
@click.option(
    "--include",
    "-i",
    multiple=True,
    type=click.Path(file_okay=False, dir_okay=True, exists=True),
    default=None,
)
@click.option("--course", type=int, default=None)
@click.option("-assignment", type=int, default=None)
def main(config, include: Tuple[os.PathLike], course: int, assignment: int):
    cfg_path = Path(config)
    logger.info(f"include paths :== {include}")

    if not cfg_path.exists() or not cfg_path.is_file():
        logger.error("The specified configuration does not exist / is not a file.")
        raise click.Abort()

    logger.info(f"loading config at {cfg_path.resolve()} ...")
    try:
        config = load_config(cfg_path)
    except Exception as exc:  # ugly except block is ugly to make things more humanfriendly.
        logger.exception("Failed to load configuration file.")
        raise click.Abort from exc

        # CLI flags override configuration
    if course is not None:
        config.course.id = course

    if assignment is not None:
        config.course.assignment_id = assignment

    if include:
        config.submission.include_paths = include

    logger.info("enumerating files...")
    paths = [Path(path) for path in config.submission.include_paths]
    logger.debug(f"i have {len(paths)} paths ")
    files = []

    for path in paths:
        if not path.exists() or not path.is_dir():
            logger.warning(f"configured path {path} does not resolve to a directory, skipping!")
            continue
        for suffix in config.submission.suffixes:
            files.extend(path.glob(suffix))

    if not files:
        logger.error("No files to upload (check include directories and glob patterns).")
        raise click.Abort("No files to upload. aborting.")

    logger.debug(f"I have {len(files)} files to upload. ")
    click.confirm("Connect to canvas to fetch assignment info?", abort=True)

    canvas = acquire_canvas_handle(config)

    assignment = acquire_assignment(canvas, config)

    logger.info(course)
    logger.info(assignment)

    files_str = "\n".join(click.format_filename(os.fspath(file)) for file in files)
    logger.info(f"preparing to upload files: \n {files_str}")

    # give user one last chance to abort.
    click.confirm("Upload specified files? (last chance to abort)", abort=True)

    # do mass upload
    file_ids = mass_upload(assignment=assignment, files=files)

    logger.debug(f"uploaded file IDs : {file_ids}")

    click.confirm(f"Submit assignment with {len(file_ids)} files?", abort=True)
    # if we got this far, we good.

    submit_assignment(assignment, file_ids)

    logger.success("Assignment submitted!")


if __name__ == "__main__":
    main()
