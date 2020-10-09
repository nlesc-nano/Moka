"""Test query functionality."""
from pathlib import Path

from pytest_mock import MockFixture, mocker

from moka.actions import query_properties
from moka.input_validation import validate_input

from .utils_test import PATH_TEST, read_mocked_reply


def test_query(mocker: MockFixture, tmp_path: Path):
    """Test the functionality to update jobs."""
    # Read and Validate user input
    path_input = PATH_TEST / "input_test_query.yml"
    opts = validate_input(path_input, "query")
    opts.output_file = (tmp_path / "output.csv").absolute().as_posix()

    # Mock the server call
    mocker.patch("moka.actions.query.query_server",
                 return_value=read_mocked_reply("query_mocked.json"))

    df = query_properties(opts)
    assert len(df) == 10