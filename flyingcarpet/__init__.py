"""
Usage:
    flyingcarpet run <module> <name>
    flyingcarpet info [<module> [<name>]]
    flyingcarpet install [<path>] [--dryrun]
"""


import docopt
import logging
import iridescence
import pathlib
import itertools

from .app import App
from .categories import Category, SubCategory
from . import build, search

APP_FILES_PATH = pathlib.Path("/usr/share/flyingcarpet/apps/")
DESKTOP_PATH = pathlib.Path("/usr/share/applications/")
LAUNCHER_PATH = pathlib.Path("/usr/bin/")

logger = iridescence.quick_setup(level=logging.DEBUG)
logger.name = __name__


def normalize_path(fname):
    if isinstance(fname, str):
        if fname.startswith("."):
            path = pathlib.Path(fname)
        else:
            path = APP_FILES_PATH / fname
    else:
        path = fname
    if not path.exists():
        raise FileNotFoundError(f"Path {path} does not exist")
    return path


def load_apps(fname, name=None):
    try:
        path = normalize_path(fname)
    except Exception:
        logger.critical("Path normalization failed", exc_info=True)
        return
    if name:
        apps = {i.NAME: i for i in search.find_apps(path, exact=True)}

        if name not in apps:
            logger.critical(f"{name} cannot be found at {path}. Apps are {', '.join(apps)}")
            return

        return apps[name]
    return list(search.find_apps(path, exact=False))


def run_app(fname, name):
    app = load_apps(fname, name)
    if app is None:
        return
    try:
        app().run()
    except Exception as e:
        logger.critical("Running app failed", exc_info=True)
        return


def info_module(fname):
    apps = load_apps(fname)
    if apps is None:
        return
    key = lambda app: app.PATH
    for path, apps in itertools.groupby(sorted(apps, key=key), key=key):
        print(f"In {path}:")
        for app in apps:
            print(f"    {app.NAME :20}{'.'.join(map(str, app.VERSION))}")
        print()


def info_app(fname, name):
    app = load_apps(fname, name)
    if app is None:
        return
    for key, value in app.app_data():
        print(f"{key:20}{value}")


def install(fname, dryrun):
    path = normalize_path(fname)
    apps = load_apps(fname)
    build.install_apps(apps, DESKTOP_PATH, LAUNCHER_PATH, APP_FILES_PATH, dryrun)


def main():
    args = docopt.docopt(__doc__)
    try:
        if args["run"]:
            run_app(args["<module>"], args["<name>"])
        elif args["info"]:
            if args["<name>"]:
                info_app(args["<module>"], args["<name>"])
            else:
                info_module(args["<module>"] or APP_FILES_PATH)
        elif args["install"]:
            install(args["<path>"] or ".", args["--dryrun"])
    except Exception:
        logger.critical("Unhandled exception", exc_info=True)
