"""
Write tests here proving:
  1. Happy path: running the check against fixtures/plan.json correctly flags the resources
     missing `landlord_account_id` (listing_media, mls_feed_sync) and passes the ones that
     have it (landlord_media[0], screening_report_export). The fixture also has a "no-op"
     entry and a "delete" entry with no `after` block at all — neither should appear in the
     output or crash the check.
  2. Idempotency: running the check twice against the same plan file produces the same
     result both times, with no duplicated output.

check_plan() takes a file path, not a dict — for a case that needs its own plan contents
instead of the shared fixture, write one with pytest's `tmp_path` rather than editing
fixtures/plan.json. You don't need to shell out to the real script for every case.
"""
import json
from pathlib import Path

import pytest

from scripts.cost_tag_check import check_plan


PLAN_FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "plan.json"


def write_plan(tmp_path, resources):
    plan_path = tmp_path / "plan.json"
    plan_path.write_text(json.dumps({"resource_changes": resources}), encoding="utf-8")
    return str(plan_path)


def resource_change(address, actions, tags):
    resource_type, name = address.rsplit(".", 1)
    return {
        "address": address,
        "type": resource_type,
        "name": name,
        "change": {"actions": actions, "after": {"tags": tags}},
    }


def test_fixture_reports_exactly_the_two_missing_billing_tags(capsys):
    result = check_plan(str(PLAN_FIXTURE))
    captured = capsys.readouterr()
    output = captured.out + captured.err

    assert result != 0
    expected = {
        "aws_s3_bucket.listing_media",
        "aws_lambda_function.mls_feed_sync",
    }
    plan = json.loads(PLAN_FIXTURE.read_text(encoding="utf-8"))
    for resource in plan["resource_changes"]:
        address = resource["address"]
        assert output.count(address) == (1 if address in expected else 0)


@pytest.mark.parametrize("actions", [["create"], ["update"]])
def test_correctly_tagged_actionable_resource_passes(tmp_path, capsys, actions):
    address = "aws_sqs_queue.billing_events"
    plan_path = write_plan(tmp_path, [resource_change(
        address, actions, {"landlord_account_id": "la-001"}
    )])

    assert check_plan(plan_path) == 0
    captured = capsys.readouterr()
    assert address not in captured.out + captured.err


@pytest.mark.parametrize("actions", [["no-op"], ["read"], ["delete"]])
def test_non_actionable_resource_is_skipped(tmp_path, capsys, actions):
    address = "aws_sqs_queue.untagged_unchanged"
    resource = resource_change(address, actions, {})
    if actions == ["delete"]:
        del resource["change"]["after"]
    plan_path = write_plan(tmp_path, [resource])

    assert check_plan(plan_path) == 0
    captured = capsys.readouterr()
    assert address not in captured.out + captured.err


@pytest.mark.parametrize("actions", [["delete", "create"], ["create", "delete"]])
@pytest.mark.parametrize("tagged", [False, True])
def test_replacement_checks_the_after_tags(tmp_path, capsys, actions, tagged):
    address = "aws_sns_topic.replaced_notifications"
    tags = {"landlord_account_id": "la-002"} if tagged else {}
    resource = resource_change(address, actions, tags)
    # Opposite before-tags ensure the check validates the proposed replacement.
    resource["change"]["before"] = {
        "tags": {} if tagged else {"landlord_account_id": "la-002"}
    }
    plan_path = write_plan(tmp_path, [resource])

    result = check_plan(plan_path)
    captured = capsys.readouterr()
    output = captured.out + captured.err
    if tagged:
        assert result == 0
        assert address not in output
    else:
        assert result != 0
        assert output.count(address) == 1


@pytest.mark.parametrize("actions", [["create"], ["update"]])
@pytest.mark.parametrize("address", [
    "aws_sqs_queue.unlisted_queue",
    "aws_dynamodb_table.unlisted_table",
])
def test_other_types_and_names_are_checked(tmp_path, capsys, actions, address):
    plan_path = write_plan(tmp_path, [resource_change(
        address, actions, {"tenant_id": "ten-001"}
    )])

    assert check_plan(plan_path) != 0
    captured = capsys.readouterr()
    assert (captured.out + captured.err).count(address) == 1


def test_repeated_calls_have_identical_exit_code_and_output(capsys):
    first_result = check_plan(str(PLAN_FIXTURE))
    first_output = capsys.readouterr()
    second_result = check_plan(str(PLAN_FIXTURE))
    second_output = capsys.readouterr()

    assert first_result != 0
    assert second_result == first_result
    assert second_output.out == first_output.out
    assert second_output.err == first_output.err
    output = first_output.out + first_output.err
    assert output.count("aws_s3_bucket.listing_media") == 1
    assert output.count("aws_lambda_function.mls_feed_sync") == 1


def test_duplicate_full_addresses_are_reported_once(tmp_path, capsys):
    first_address = 'module.east.aws_sqs_queue.events["la-001"]'
    second_address = 'module.west.aws_sqs_queue.events["la-001"]'
    first = {
        "address": first_address,
        "type": "aws_sqs_queue",
        "name": "events",
        "change": {"actions": ["create"], "after": {"tags": {}}},
    }
    second = {**first, "address": second_address}
    plan_path = write_plan(tmp_path, [first, second, first, second])

    assert check_plan(plan_path) != 0
    captured = capsys.readouterr()
    output = captured.out + captured.err
    assert output.count(first_address) == 1
    assert output.count(second_address) == 1
