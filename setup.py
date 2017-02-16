#!/usr/bin/env python3

from setuptools import setup
from flyingcarpet import build
import pathlib
import logging
import iridescence

logger = iridescence.quick_setup(level=logging.DEBUG)
logger.name = __name__

pwd = pathlib.Path().resolve()
builder = build.FileBuilder(pwd / "build", pwd / "flyingcarpet_apps")

setup(name="flyingcarpet",
      version="0.1",
      author="Matthew Joyce",
      author_email="matsjoyce@gmail.com",
      data_files=[("share/applications", list(builder.generate_desktop_files())),
                  ("bin", list(builder.generate_launcher_files()))],
      package_data={"flyingcarpet_apps": list(builder.list_app_files())},
      packages=["flyingcarpet", "flyingcarpet.build", "flyingcarpet.ui", "flyingcarpet_apps"],
      entry_points={"console_scripts": ["flyingcarpet = flyingcarpet:main"]})

logger.info("Installed the following apps:")
for app in builder.apps:
    logger.info(f"    {app.NAME} - {'.'.join(map(str, app.VERSION))}")
