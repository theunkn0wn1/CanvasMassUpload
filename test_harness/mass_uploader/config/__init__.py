from pathlib import Path
import cattr
import toml
from .configroot import ConfigRoot


def load_config(path: Path) -> ConfigRoot:
    raw = toml.loads(path.read_text())
    return cattr.structure(raw, ConfigRoot)
