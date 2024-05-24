from __future__ import annotations

from pathlib import Path


def test_build(run, tmp_docs_path):
    assert run.exit_code == 0
    assert Path.exists(tmp_docs_path / "site")
    index_file = tmp_docs_path / "site/index.html"
    assert index_file.exists()
