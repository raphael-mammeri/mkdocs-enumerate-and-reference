from pathlib import Path


def test_build_command(run, tmp_docs_path):
    assert run.exit_code == 0, "mkdocs build failed"
    assert Path.exists(tmp_docs_path / "site")
    index_file = tmp_docs_path / "site/index.html"
    assert index_file.exists(), f"{index_file} does not exist"
