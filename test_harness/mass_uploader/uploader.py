from typing import List

import canvasapi
from canvasapi.assignment import Assignment
from canvasapi.canvas import Canvas
from pathlib import Path

from humanfriendly.terminal.spinners import AutomaticSpinner

from .config import load_config, ConfigRoot
from loguru import logger


def acquire_canvas_handle(config: ConfigRoot) -> Canvas:
    logger.info(f"Acquiring canvas at uri {config.secrets.base_uri!r}...")

    # step one, acquire handle to canvas. Requires secrets config
    return canvasapi.Canvas(base_url=config.secrets.base_uri, access_token=config.secrets.canvas_key)


def acquire_assignment(canvas: Canvas, config: ConfigRoot) -> Assignment:
    logger.debug(f"Acquiring course by id {config.course.id}...")
    # step two, acquire the course. requires course config.
    course = canvas.get_course(config.course.id)

    logger.debug(f"Acquiring assignment by ID {config.course.assignment_id} ...")
    # step three, acquire the assignment handle. requires course config.
    assignment = course.get_assignment(config.course.assignment_id)

    return assignment


def mass_upload(assignment: Assignment, files: List[Path]) -> List[int]:
    upload_ids = []
    # step four: upload all relevant files to the submission that doesn't exist yet and enumerate the
    # IDs you get back
    with AutomaticSpinner(label="Uploading assets..."):
        for path in files:
            logger.debug(f"uploading asset {path} ...")
            success, response = assignment.upload_to_submission(f"{path}")
            if not success:
                logger.error(f"failed to upload asset {path} :: {response}")
                raise ConnectionError
            file_id = response["id"]
            logger.success(f"file id {file_id}")
            upload_ids.append(file_id)
    return upload_ids


def submit_assignment(assignment: Assignment, file_ids: List[int]):
    # step 5: call `assignment.submit` and pass the file IDs acquired from step 4
    assignment.submit({"file_ids": file_ids, "submission_type": "online_upload"})
