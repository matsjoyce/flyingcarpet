#!/usr/bin/env python3

from setuptools import setup

setup(name="flyingcarpet",
      version="0.1",
      author="Matthew Joyce",
      author_email="matsjoyce@gmail.com",
      packages=["flyingcarpet", "flyingcarpet.ui"],
      entry_points={"console_scripts": ["flyingcarpet = flyingcarpet:main"]})
