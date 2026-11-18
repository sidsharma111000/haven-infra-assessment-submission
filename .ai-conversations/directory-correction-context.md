# Earlier directory correction — original context

This occurred before B2 and is retained as genuine correction context, without portraying it as a B2 implementation bug.

## User

````text
now i need to complete a assessment&#x20;
fro that i will run all terminal commands, include terraform
do not excute any cmnds and install anything&#x20;

first i want u to inspect the repo without changing anything&#x20;
lets start with readme.rd first adn then all markdown, application and test terraform and files&#x20;

also please try to explain the domain flow and the correct access boundary
check the correct billing tag
also which file we need to keep safe and untouched
also what b0,b1 and b2 require and difference between current repor and our assesment



````

## Assistant

````text
I’ll inspect the repository read-only, starting with the README, and won’t run terminal commands, Terraform, or installations. I’ll use the files to explain the domain flow, access boundaries, billing tag, protected files, and B0/B1/B2 requirements.


````

## Assistant

````text
I’ll keep the review read-only. I won’t run terminal commands, Terraform, tests, installations, or change files.

The current workspace contains only `outputs/` and `work/`; no repository is attached. Please share the repository’s local folder path and the assessment brief, if it’s separate from the repo.

Once available, I’ll review:

1. `README.rd` or `README.md` first, then the remaining Markdown.
2. Application code, tests, Terraform, and configuration.
3. Domain flow and intended versus implemented access boundaries.
4. Required billing tag and where it is applied.
5. Files that must remain untouched or contain sensitive information.
6. B0, B1, and B2 requirements, with a comparison against the current repository.

I’ll distinguish documented requirements from findings in the code and anything that cannot be verified without running commands.
````

## User

````text
i hope u are checking on the current and correct dir
/Users/siddharthsharma/Documents/haven-infra-assessment\

````

## Assistant

````text
I checked the chat’s default workspace earlier, not this repository. I’ll now inspect `/Users/siddharthsharma/Documents/haven-infra-assessment`, starting with the README. I won’t run commands or change files.

````

## Assistant

````text
Yes—I’ve now inspected **`/Users/siddharthsharma/Documents/haven-infra-assessment`**, starting with `README.md`, then all remaining Markdown, application files, tests, Terraform, the plan fixture, and seeded state.

**No terminal commands, Terraform, tests, or installations were run. No files were changed.** This is a static review.

The domain flow is:

```text
LandlordAccount ← billing and access boundary
  └── Property
        └── Tenant
              └── ScreeningReport

PropertyManager → belongs to exactly one LandlordAccount
```

To authorize report access, follow `report.tenant_id → Tenant.property_id → Property.landlord_account_id`, then compare that account ID with `actor.landlord_account_id`. Allow only a match. If the tenant or property is missing, return `False`.

For the supplied data, `pm-001` can access `rep-001` but must be denied `rep-002`. A manager’s ID, tenant ID, or property ID alone does not establish the account boundary. Billing tags also do not enforce authorization.

The correct billing tag is **`landlord_account_id`**, because the landlord account pays for everything underneath it. A `tenant_id` tag can provide extra context, but cannot replace it.

| Resource in `fixtures/plan.json` | Required outcome |
|---|---|
| `aws_s3_bucket.landlord_media[0]` | Pass: has `landlord_account_id` |
| `aws_s3_bucket.listing_media` | Fail: only has `tenant_id` |
| `aws_lambda_function.mls_feed_sync` | Fail: empty tags |
| `aws_lambda_function.screening_report_export` | Pass: has `landlord_account_id` |
| `aws_s3_bucket.archive_media` | Skip: `no-op` |
| `aws_s3_bucket.decommissioned_media` | Skip: deletion with `after: null` |

The fixture and Terraform source are separate assessment inputs: for example, the fixture gives `listing_media` a `tenant_id` tag, while `lifecycle.tf` gives that bucket no tags at all. Neither currently supplies the required billing tag.

**These four files must remain untouched**, explicitly required by the README:

- `app/models.py`
- `app/seed_data.py`
- `fixtures/plan.json`
- `terraform/terraform.tfstate`

The state is deliberately committed assessment data representing four existing buckets. Do not delete, regenerate, or manually edit it. For additional test scenarios, create temporary fixtures rather than editing the supplied plan or seed data. During this inspection, every file remained untouched.

Here is the difference between the current repository and the required assessment outcome:

| Part | Current repository | Required outcome |
|---|---|---|
| **B0 — resource identity** | Buckets use positional `count` indices; `B0.md` is unanswered | Explain the removal cascade, its risk, and a stable identity fix |
| **B1 — archive economics** | Photos transition to `GLACIER` after 30 days; `B1.md` is unanswered | Explain early deletion charges and propose a lifecycle that respects deletion deadlines |
| **B2 — authorization** | `can_access_screening_report()` raises `NotImplementedError` | Implement account-scoped access with missing-data denial, plus tests |
| **B2 — billing check** | `check_plan()` raises `NotImplementedError` | Check create/update resources, report missing billing tags, return an appropriate exit code, and produce repeatable output |
| **B2 — evidence** | Test files contain instructions but no test functions; design answers are blank | Add the required tests, explain idempotency, and record AI assistance |

For **B0**, removing `la-002` shifts the remaining list positions:

| Address | Seeded bucket | New desired bucket | Expected consequence |
|---|---|---|---|
| `[0]` | `la-001` | `la-001` | Unchanged |
| `[1]` | `la-002` | `la-003` | Replacement |
| `[2]` | `la-003` | `la-004` | Replacement |
| `[3]` | `la-004` | None | Destruction |

This puts surviving accounts’ buckets at risk of destructive replacement or failed operations. The fix is `for_each` keyed by stable landlord account IDs. **Existing indexed resources also need an explicit migration mapping**, typically `moved` blocks; changing to `for_each` alone does not preserve their Terraform identities. The supplied state should remain unchanged.

The repository specifies `terraform plan -refresh=false` for reproducing B0 against its dummy state. I have not run it, so the table describes expected behavior rather than observed plan output.

For **B1**, `GLACIER` means Glacier Flexible Retrieval, with a **90-day minimum storage duration**. A photo archived on day 30 and deleted on day 40 has spent only 10 days there, leaving approximately **80 days of minimum-duration storage charges**, alongside applicable transition charges. Deletion does not require restoring the object.

A request on day 40 must be fulfilled by day 70. Waiting until day 120 to avoid the archive minimum would violate that deadline. A redesign should keep deletion-prone content in a suitable storage class and archive only content whose expected retention justifies the minimum duration. Simply moving the transition later does not eliminate early-deletion risk.

There is another implementation gap: the lifecycle rule says “sold listings” in its description, but has **no filter or sold-status condition**. Its transition timing is based on object age, not the date a listing sold.

For **B2**, the intended deduplication key should be the resource’s full Terraform **`address`**, including any module path and instance index/key. A per-run set can ensure each offending address prints once. Reinitializing that set on every invocation and using deterministic output makes repeated checks **idempotent**, without storing history between runs. Create/update detection should also account for replacement action lists containing `create`.

Required tests include cross-account denial, same-account allowance, the fixture’s two missing-tag resources, skipped changes, and identical results across two runs. Missing tenant/property denial should also be covered.

Finally, `.ai-conversations/README.md` requests an AI conversation record for B2. Since we are discussing B2, retain this exchange or a written summary for submission. Its reference to recording guidance in `DESIGN_NOTES.md` is incomplete—the current file contains idempotency and decision sections, but no detailed AI-record instructions.
````
