import attr
from .secrets import Secrets
from .course import Course
from .submission import Submission


@attr.dataclass
class ConfigRoot:
    secrets: Secrets
    course: Course
    submission: Submission
