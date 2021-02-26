from typing import List

import attr


@attr.dataclass
class Submission:
    include_paths: List[str] = attr.ib(factory=list)
    suffixes: List[str] = attr.ib(factory=list)
