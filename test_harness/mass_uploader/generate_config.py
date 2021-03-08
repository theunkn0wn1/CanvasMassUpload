import click
import cattr
import toml

from .config import ConfigRoot
from .config.course import Course
from .config.submission import Submission
from .config.secrets import Secrets
from pathlib import Path
from urllib.parse import urlparse

from loguru import logger


@click.command()
def cli():
    print("===============================================")
    print("Unknown's Canvas mass-uploader, configuration helper")
    print("===============================================")

    print(
        "This helper script will help you generate a configuration file, "
        "this is necessary to keep track of some mandatory bits that only need be set once."
    )

    course = click.prompt(
        "Please give me the url to a sample assignment",
        default="https://canvas.saddleback.edu/courses/45192/assignments/948561",
    )
    parsed_uri = urlparse(course)
    if not parsed_uri.scheme == "https":
        logger.error("HTTPS is strictly enforced.")
        raise click.Abort

    base_uri = f"{parsed_uri.scheme}://{parsed_uri.hostname}"

    _, _, course_id, _, assignment_id, *bits = parsed_uri.path.rstrip(r"/").split("/")
    if bits:
        logger.warning(f"unparsed bits of provided URI (this is probably an error) :: {bits!r}")

    profile_uri = f"{base_uri}/profile/settings"
    print("Ok, for the next part you are going to need to generate an API key if you haven't already.")
    print(f"Unfortunately i can't do this for you, but here is the URL :: {profile_uri}")
    print("On that page, you will need to click the 'New access Token' button and fill in the prompt")
    print("Once thats done, copy the resulting key and feed it to me here ")
    api_key = click.prompt("Canvas API key (will not echo to terminal)", hide_input=True)

    secrets = Secrets(canvas_key=api_key, base_uri=base_uri)

    logger.info("Done with secrets module configuration. (1/3)")

    course = Course(id=course_id, assignment_id=assignment_id)

    logger.info("Done with default course module configuration. (2/3)")

    include_globs = click.prompt(
        "Ok, last step. Please enter a glob pattern for the filetypes to glob for.",
        default="*.txt *.java",
    ).split()
    submission = Submission(suffixes=include_globs, include_paths=[])

    logger.info("Done with basic submission module configuration. (3/3).")
    logger.debug("Generating configuration file...")
    root = ConfigRoot(secrets=secrets, course=course, submission=submission)

    raw = cattr.unstructure(root)

    logger.debug("emitting config file...")

    output = Path() / "mass_upload.toml"

    output.write_text(toml.dumps(raw))

    logger.success(
        f"Done! you can find the config file at {click.format_filename(str(output.absolute()))}"
    )


if __name__ == "__main__":
    cli()
