import pathlib
import sys
import runpy
import traceback
import shlex
import stat
import logging

from .. import app, categories


logger = logging.getLogger(__name__)


class FileBuilder:
    APPS_DIR = (pathlib.Path(__file__).parent.parent.parent / "flyingcarpet_apps").resolve()

    def __init__(self, pwd, search):
        self.search = search
        self.pwd = pwd
        self.apps = []

        self.load()

    @classmethod
    def extract_apps(cls, path):
        relpath = path.relative_to(cls.APPS_DIR.parent)
        module_name = ".".join(relpath.parts[:-1] + (relpath.stem,))
        try:
            namespace = runpy.run_module(module_name, alter_sys=True)
        except Exception as exc:
            logger.info(f"Loading {path} failed, imported as {module_name}", exc_info=True)
            return []
        else:
            apps = [cls for _, cls in sorted(namespace.items())
                    if isinstance(cls, type) and issubclass(cls, app.App)]
            if len(apps) != len({i.NAME for i in apps}):
                raise ValueError("Duplicated app names")
            for a in apps:
                a.PATH = path.relative_to(cls.APPS_DIR)
            return apps

    def load(self):
        if not self.pwd.exists():
            self.pwd.mkdir()

        sys.path.insert(0, str(self.pwd))
        for path in self.search.iterdir():
            if path.name.startswith("__") or path.name.startswith("."):
                continue
            logger.info(f"Searching {path}")
            self.apps.extend(self.extract_apps(path))

        sys.path.pop(0)

    def generate_desktop_files(self):
        for a in self.apps:
            fname = (self.pwd / ("flyingcarpet-" + a.NAME)).with_suffix(".desktop")
            with fname.open("w") as f:
                f.write(self.desktop_text(a))
            yield str(fname)

    def generate_launcher_files(self):
        for a in self.apps:
            if a.LAUNCHER_NAME is None:
                continue
            fname = self.pwd / a.LAUNCHER_NAME
            with fname.open("w") as f:
                f.write(self.launcher_text(a))
            fname.chmod(fname.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
            yield str(fname)

    def list_app_files(self, dir=None):
        if dir is None:
            dir = self.search
        for f in dir.iterdir():
            if f.is_dir():
                yield from self.list_app_files(f)
            elif f.suffix not in (".pyc",):
                yield f

    def desktop_text(self, app):
        return f"""
#!/usr/bin/env xdg-open
[Desktop Entry]
Type=Application
Name={'flyingcarpet::' if app.ADD_PREFIX else ''}{app.NAME}
Exec={self.app_command(app)}
GenericName={app.GENERIC_NAME}
Comment={app.DESCRIPTION}
Categories={categories.build_category_string(app.CATEGORIES, app.SUBCATEGORIES)}
Icon={app.ICON}
""".strip()

    def app_command(self, app):
        if app.LAUNCHER_NAME is not None:
            return app.LAUNCHER_NAME
        return " ".join(map(shlex.quote, ["flyingcarpet", "run", str(app.PATH), app.NAME]))

    def launcher_text(self, app):
        return f"""#!/usr/bin/env python3
import flyingcarpet
flyingcarpet.run_app({str(app.PATH) !r}, {app.NAME !r})
"""
