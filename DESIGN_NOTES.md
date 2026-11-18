# Design Notes

## B2 — idempotency key

The exact deduplication key is the **full Terraform resource address**, taken unchanged from each resource_changes entry's `address` field. This includes module paths and any instance index or account-ID key. For example, module.east.aws_sqs_queue.events["la-001"] and module.west.aws_sqs_queue.events["la-001"] are distinct resources even though their type and name match.

The check implements **idempotency** without keeping a record between runs. Each check_plan() call creates a fresh local set of violating addresses, examines every actionable entry, then prints the set in sorted order. Duplicate violations for an address print once. An unchanged readable input produces the same unique violations, the same output order, and the same exit code. No global set, cache, or persistent deduplication file affects subsequent calls.

All entries are inspected before deduplicating output. If duplicated entries disagree, an actionable violation in any entry keeps that address in the violation set; a compliant duplicate cannot hide it. A malformed entry instead fails the run as invalid input.

A global seen-address set was rejected because one call could suppress a later call's output or change its result. Deduplicating by resource type, name, tenant ID, or landlord account ID was rejected because different infrastructure resources can share those values. Printing the set directly was rejected because set iteration does not provide the intended sorted output order.

## Any other decision with a non-obvious alternative

### Billing and action selection

The required billing tag is landlord_account_id: LandlordAccount is the billing unit. tenant_id is insufficient. The checker uses proposed change.after.tags, rather than before-tags, and checks every resource whose actions contain create or update. Membership handles both replacement orders, ["delete", "create"] and ["create", "delete"]. Comparing actions only with ["create"] would miss replacements.

Changes without create/update are skipped before accessing after, including no-op, read, and delete-only changes with null or absent after. No resource-type or resource-name allowlist is used. This follows the assessment's generic policy; provider-specific support for tags is not inferred.

### Empty values, malformed input, and exit codes

A billing tag must be a non-blank string. Missing/null/empty tags and a missing/null/blank/non-string landlord_account_id are violations. Checking key presence alone was rejected because a present but empty value does not identify a billing account. The checker does not validate that a non-blank ID exists in a separate account registry, and does not enforce an la- prefix.

Unreadable files, decoding failures, invalid JSON, and invalid required structure return 2 with an stderr diagnostic. Examples include a non-object plan, missing/non-list resource_changes, missing/blank addresses, invalid change/actions, absent/non-object after for an actionable change, and a non-object, non-null tags value.

Return 0 means compliance; return 1 means tag violations; return 2 means invalid input. An explicit empty resource_changes list passes. Missing resource_changes is deliberately rejected rather than silently treated as an empty plan. This is stricter than accepting Terraform JSON variants that omit the field for no changes; supporting those variants would require a deliberate contract change.

Input errors abort before any partial violation list is printed. This distinguishes a completed billing check from an incomplete inspection. The checker validates the structures it consumes, not the entire Terraform JSON schema; action strings are not checked against a complete Terraform enum. Unknown/computed billing tags without a concrete usable after-value do not pass. These are implementation boundaries, not claims of full plan validation.

### Access-control boundary

Report → matching Tenant → matching Property resolves the owning landlord_account_id. Access is allowed only when that ID equals actor.landlord_account_id. Missing tenant or property returns False. IDs are matched through their relationships, not by list position, naming conventions, or billing tags. The current model assumes unique record IDs and an already-authenticated, trusted actor; the function does not implement authentication or account-registry validation.

### Tests and evidence

Tests use the existing domain fixtures without mutating them. Custom plans use tmp_path; fixtures/plan.json remains unchanged. The user supplied successful runs of 4 access-control tests and 16 cost-tag tests, separately. Initial stub failures are retained as actual evidence, not described as unexpected bugs.

Two manual checker runs printed the same two sorted addresses and each returned 1, correctly indicating fixture violations. The supplied diff returned 0. The original exit-code comparison accidentally compared rc1 with itself; the user's subsequent corrected comparison of rc1 with rc2 returned 0. Both versions are preserved in terminal_log.md.

The 16 checker cases do not directly test every empty-value or malformed-input policy, an empty plan, sorted output across reordered plans, or conflicting duplicate entries. The four access tests do not cover every manager/report combination or duplicate domain IDs. These gaps are explicit; no additional execution is claimed.

See terminal_log.md for supplied terminal evidence and its gaps. See .ai-conversations/B2-transcript.md and accompanying source records for actual prompts, replies, and code-change records. No assistant-run terminal commands, tests, installations, Terraform operations, or protected-file edits were performed.
