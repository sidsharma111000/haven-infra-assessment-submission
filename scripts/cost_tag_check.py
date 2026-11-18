"""
B2, part 2 — implement the cost-tagging check.

Read fixtures/plan.json for the shape of a `terraform show -json` plan: a `resource_changes`
list, where each entry has a `type`, an `address`, and `change.after.tags`.

Implement check_plan() so it:
  - Looks at every resource being created or updated (skip anything whose change.actions
    isn't "create" or "update" — a "no-op"/"read" change, or a "delete" with no `after`
    block at all).
  - Fails (returns a non-zero exit code) if the resource is missing the tag that identifies
    the real billing unit, per README.md's domain model — not whatever tag the resource
    happens to already carry.
  - Is idempotent: running this twice against the same plan file produces the same result,
    with no duplicate output and no flipped pass/fail. This is about a single run being
    stable and repeatable — it does not require remembering anything between runs.
  - Prints which specific resource address(es) are missing the tag.

Run manually: python scripts/cost_tag_check.py fixtures/plan.json
"""
import json
import sys


def check_plan(plan_path: str) -> int:
    """
    Return 0 for compliance, 1 for billing-tag violations, or 2 for invalid input.

    Require a non-blank string landlord_account_id in proposed after.tags.
    Deduplicate violations by full resource address within this call only.
    """
    violations: set[str] = set()
    try:
        with open(plan_path, encoding="utf-8") as plan_file:
            plan = json.load(plan_file)

        if not isinstance(plan, dict):
            raise ValueError("plan must be a JSON object")
        resources = plan.get("resource_changes")
        if not isinstance(resources, list):
            raise ValueError("resource_changes must be a list (use [] for no changes)")

        for index, resource in enumerate(resources):
            if not isinstance(resource, dict):
                raise ValueError(f"resource_changes[{index}] must be an object")
            address = resource.get("address")
            if not isinstance(address, str) or not address.strip():
                raise ValueError(f"resource_changes[{index}] needs a non-blank address")
            change = resource.get("change")
            if not isinstance(change, dict):
                raise ValueError(f"{address}: change must be an object")
            actions = change.get("actions")
            if (
                not isinstance(actions, list)
                or not actions
                or not all(isinstance(action, str) and action for action in actions)
            ):
                raise ValueError(f"{address}: actions must be a non-empty list of strings")

            # Membership checks include both replacement action orders.
            if "create" not in actions and "update" not in actions:
                continue

            after = change.get("after")
            if not isinstance(after, dict):
                raise ValueError(f"{address}: actionable change needs an after object")
            tags = after.get("tags")
            if tags is None:
                tags = {}
            if not isinstance(tags, dict):
                raise ValueError(f"{address}: tags must be an object or null")
            account_id = tags.get("landlord_account_id")
            if not isinstance(account_id, str) or not account_id.strip():
                violations.add(address)

    except (OSError, UnicodeError, ValueError) as error:
        print(f"Invalid plan: {error}", file=sys.stderr)
        return 2

    for address in sorted(violations):
        print(f"{address}: missing or empty landlord_account_id")
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(check_plan(sys.argv[1]))
