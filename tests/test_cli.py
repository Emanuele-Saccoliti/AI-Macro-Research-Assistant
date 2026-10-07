from unittest.mock import Mock

import pytest
from pydantic import ValidationError

from ai_macro_research_v2 import cli
from ai_macro_research_v2.config import Settings


@pytest.mark.parametrize("value", ["-1", "0", "101", "1.5", "invalid"])
def test_parser_rejects_invalid_max_articles(value, capsys):
    with pytest.raises(SystemExit) as exc:
        cli.build_parser().parse_args(["query", "--max-articles", value])

    assert exc.value.code == 2
    assert "--max-articles must be between 1 and 100" in capsys.readouterr().err


@pytest.mark.parametrize("value", [1, 2, 3, 30, 100])
def test_parser_and_settings_accept_valid_max_articles(value):
    args = cli.build_parser().parse_args(["query", "--max-articles", str(value)])

    assert args.max_articles == value
    assert Settings(max_articles=value, _env_file=None).max_articles == value


@pytest.mark.parametrize("value", [-1, 0, 101])
def test_settings_reject_invalid_max_articles(value):
    with pytest.raises(ValidationError):
        Settings(max_articles=value, _env_file=None)


def test_parser_leaves_omitted_max_articles_unset():
    assert cli.build_parser().parse_args(["query"]).max_articles is None


def test_invalid_max_articles_stops_before_prompt_or_workflow(monkeypatch):
    prompt = Mock()
    settings = Mock()
    workflow = Mock()
    monkeypatch.setattr("builtins.input", prompt)
    monkeypatch.setattr(cli, "get_settings", settings)
    monkeypatch.setattr(cli, "DynamicMacroResearchWorkflow", workflow)

    with pytest.raises(SystemExit) as exc:
        cli.main(["--max-articles", "0"])

    assert exc.value.code == 2
    prompt.assert_not_called()
    settings.assert_not_called()
    workflow.assert_not_called()
