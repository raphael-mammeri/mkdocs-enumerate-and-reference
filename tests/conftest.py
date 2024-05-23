from __future__ import annotations

import os
import shutil
from contextlib import contextmanager
from pathlib import Path

import pytest
from click.testing import CliRunner
from mkdocs.__main__ import build_command
from mkdocs.config import load_config
from mkdocs.structure.files import get_files
from mkdocs.structure.nav import get_navigation


@contextmanager
def ch_dir(path):
    """
    Context manager for directory change.
    """
    prev_cwd = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)


@pytest.fixture()
def tmp_docs_path(tmp_path: Path):
    path = tmp_path / "docs"
    shutil.copytree("tests/fixtures/demo", path)
    return path


@pytest.fixture()
def config(tmp_docs_path: Path):
    config_path = str(tmp_docs_path / "mkdocs.yml")
    return load_config(config_path)


@pytest.fixture()
def nav(config):
    files = get_files(config)
    nav = get_navigation(files, config)
    config.plugins.on_nav(nav=nav, files=files, config=config)
    return nav


@pytest.fixture()
def run(tmp_docs_path: Path):
    """
    Run mkdocs build command
    """
    with ch_dir(tmp_docs_path):
        return CliRunner().invoke(build_command)
