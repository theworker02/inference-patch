"""Regression tests for malformed system-description validation."""

import logging
from types import SimpleNamespace

from submission_checker.checks.system_check import SystemCheck
from submission_checker.loader import SubmissionLogs


def test_null_status_is_reported_as_invalid_instead_of_raising(caplog):
    """Submission metadata is untrusted and a required status must be text."""
    submission_logs = SubmissionLogs(
        system_json={"status": None},
        loader_data={"submitter": "example", "division": "closed"},
    )
    check = SystemCheck(
        logging.getLogger("test.system_check"),
        "/submission/systems/example.json",
        SimpleNamespace(skip_meaningful_fields_emptiness_check=False),
        submission_logs,
    )

    with caplog.at_level(logging.ERROR):
        assert check.availability_check() is False

    assert "status must be a string" in caplog.text
