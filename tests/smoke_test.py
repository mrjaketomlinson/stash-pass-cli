import pytest

import importlib
from typing import List, Tuple
import typer
from typer.testing import CliRunner


def _find_typer_apps() -> List[Tuple[str, str, typer.Typer]]:
    """
    Try to import expected CLI modules and return any Typer app objects found.
    Returns a list of tuples (module_name, attribute_name, app_object).
    """
    candidates = [
        "stash_pass.cli",
        "stash_pass.settings.cli",
        "stash_pass.vault.cli",
    ]
    found = []
    for module_name in candidates:
        try:
            mod = importlib.import_module(module_name)
        except Exception:
            continue
        for attr_name in dir(mod):
            try:
                val = getattr(mod, attr_name)
            except Exception:
                continue
            if isinstance(val, typer.Typer):
                found.append((module_name, attr_name, val))
    return found


APPS = _find_typer_apps()


def test_found_at_least_one_typer_app():
    assert (
        APPS
    ), "No typer.Typer apps found in stash_pass.cli / settings.cli / vault.cli"


@pytest.mark.parametrize("module_name,attr_name,app", APPS)
def test_help_runs_and_outputs_text(module_name, attr_name, app):
    runner = CliRunner()
    result = runner.invoke(app, ["--help"])
    assert (
        result.exit_code == 0
    ), f"{module_name}.{attr_name} --help exited {result.exit_code}\n{result.output}"
    assert result.output and result.output.strip(), "Help output was empty"
