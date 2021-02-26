import attr


@attr.dataclass
class Secrets:
    canvas_key: str
    base_uri: str
