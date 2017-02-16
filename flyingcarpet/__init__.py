"""
Usage:
    flyingcarpet run <module> <name>
    flyingcarpet info [<module> [<name>]]
"""


import docopt
import logging
import iridescence
import pathlib
import itertools

from .app import App
from .categories import Category, SubCategory
from .build import FileBuilder

logger = iridescence.quick_setup(level=logging.DEBUG)
logger.name = __name__


def normalize_path(fname):
    path = (FileBuilder.APPS_DIR / fname).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Path {path} does not exist")
    if FileBuilder.APPS_DIR not in path.parents:
        raise ValueError(f"Path {path} is not a child of {FileBuilder.APPS_DIR}")
    return path


def load_apps(fname, name=None):
    try:
        path = normalize_path(fname)
    except Exception:
        logger.critical("Path normalization failed", exc_info=True)
        return
    apps = FileBuilder.extract_apps(path)
    if name:
        apps = {i.NAME: i for i in apps}

        if name not in apps:
            logger.critical(f"{name} cannot be found at {path}. Apps are {', '.join(apps)}")
            return

        return apps[name]
    return apps


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
    print(f"{'Name' :20}{'Version'}")
    print(f"{'----' :20}{'-------'}")
    for app in apps:
        print(f"{app.NAME :20}{'.'.join(map(str, app.VERSION))}")


def info_app(fname, name):
    app = load_apps(fname, name)
    if app is None:
        return
    for key, value in app.app_data():
        print(f"{key:20}{value}")


def info_all():
    fb = FileBuilder(FileBuilder.APPS_DIR, FileBuilder.APPS_DIR)
    key = lambda app: app.PATH
    for path, apps in itertools.groupby(sorted(fb.apps, key=key), key=key):
        print(f"In {path}:", ", ".join(app.NAME for app in apps))


def main():
    args = docopt.docopt(__doc__)
    try:
        if args["run"]:
            run_app(args["<module>"], args["<name>"])
        elif args["info"]:
            if args["<name>"]:
                info_app(args["<module>"], args["<name>"])
            elif args["<module>"]:
                info_module(args["<module>"])
            else:
                info_all()
    except:
        logger.critical("Unhandled exception", exc_info=True)
