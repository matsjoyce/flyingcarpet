import runpy
import pathlib
import logging
import sys

from . import app


logger = logging.getLogger(__name__)


def find_paths(path):
    if path.name == "__pycache__" or path.name.startswith("."):
        return
    elif path.is_dir():
        if (path / "__main__.py").exists():
            yield path
        else:
            for subpath in path.iterdir():
                yield from find_paths(subpath)
    elif path.suffix == ".py":
        yield path


def extract_apps(path):
    path = path.resolve()
    logger.debug(f"Loading {path} as {path.stem}")
    sys.path.insert(0, str(path.parent))
    try:
        namespace = runpy.run_module(path.stem, alter_sys=True)
    except Exception as exc:
        logger.warning(f"Loading {path} failed, imported as {module_name}", exc_info=True)
        return []
    else:
        apps = [cls for _, cls in sorted(namespace.items())
                if isinstance(cls, type) and issubclass(cls, app.App)]
        if len(apps) != len({i.NAME for i in apps}):
            raise ValueError("Duplicated app names")
        for a in apps:
            a.PATH = path
        logger.debug(f"Loading successful, found {len(apps)} apps")
        return apps
    finally:
        sys.path.remove(str(path.parent))


def find_apps(search_path, exact):
    if exact:
        yield from extract_apps(search_path)
        return
    for path in find_paths(search_path):
        logger.info(f"Searching {path}")
        yield from extract_apps(path)
