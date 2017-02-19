import shlex
import shutil
import logging
import itertools
import stat

from . import categories

logger = logging.getLogger(__name__)


def app_command(app):
    if app.LAUNCHER_NAME is not None:
        return app.LAUNCHER_NAME
    return " ".join(map(shlex.quote, ["flyingcarpet", "run", str(app.PATH.name), app.NAME]))


def generate_desktop_file(app):
    return f"""
#!/usr/bin/env xdg-open
[Desktop Entry]
Type=Application
Name={'flyingcarpet::' if app.ADD_PREFIX else ''}{app.NAME}
Exec={app_command(app)}
GenericName={app.GENERIC_NAME}
Comment={app.DESCRIPTION}
Categories={categories.build_category_string(app.CATEGORIES, app.SUBCATEGORIES)}
Icon={app.ICON}
""".strip()


def generate_launcher(app):
    return f"""#!/usr/bin/env python3
import flyingcarpet
flyingcarpet.run_app({str(app.PATH.name) !r}, {app.NAME !r})
"""


def write_desktop_file(app, path, dryrun):
    fname = (path / ("flyingcarpet-" + app.NAME)).with_suffix(".desktop")
    logger.debug(f"Installing desktop file for {app.NAME} to {fname}")
    data = generate_desktop_file(app)
    if dryrun:
        return
    with fname.open("w") as f:
        f.write(data)


def write_launcher_file(app, path, dryrun):
    if app.LAUNCHER_NAME is None:
        return
    fname = path / app.LAUNCHER_NAME
    logger.debug(f"Installing launcher for {app.NAME} to {fname}")
    data = generate_launcher(app)
    if dryrun:
        return
    with fname.open("w") as f:
        f.write(data)
    fname.chmod(fname.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def recursive_list(path):
    if path.name == "__pycache__" or path.name.startswith("."):
        return
    elif path.is_dir():
        for subpath in path.iterdir():
            yield from recursive_list(subpath)
    elif path.is_file():
        yield path


def get_app_files(app):
    files = set().union(*[recursive_list(path) for path in itertools.chain([app.PATH], app.FILES)])
    for path in files:
        yield path, path.relative_to(app.PATH.parent)


def install_apps(apps, desktop_path, launcher_path, app_files_path, dryrun):
    if dryrun:
        logger.info("Dryrun!")
    if not app_files_path.exists():
        logger.info(f"Creating {app_files_path}")
        if not dryrun:
            app_files_path.mkdir(parents=True, exist_ok=False)
    app_files = set()
    for app in apps:
        logger.info(f"Processing app {app.NAME}")
        write_desktop_file(app, desktop_path, dryrun)
        write_launcher_file(app, launcher_path, dryrun)
        app_files.update(get_app_files(app))
    for path, relpath in app_files:
        dest = app_files_path / relpath
        if not dest.parent.exists():
            logger.debug(f"Creating {dest.parent}")
            if not dryrun:
                dest.parent.mkdir(parents=True, exist_ok=False)
        logger.debug(f"Copying {path} to {dest}")
        if not dryrun:
            shutil.copy(path, dest)
