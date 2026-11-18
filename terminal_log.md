# Terminal log — supplied evidence

## Provenance and gaps

These are actual user-supplied records from this chat and the two attached failure transcripts. Text is retained as supplied, including Markdown formatting, HTML entities, shell prompts, misspellings, and accidental pasted fragments. This is not a fresh execution or a reconstructed clean terminal session. The assistant ran no terminal commands. No app terminal session was attached when read-only capture was attempted.

Evidence gaps:
- No successful setup transcript was supplied for virtual-environment creation/activation, dependency installation, or terraform init. The errors below are available setup-related evidence, not proof of successful initialization.
- Pytest output supplies Python/pytest environment details and pass/fail summaries, but no shell exit-code captures for those test commands. No numeric pytest exit codes are asserted.
- The two passing suites were run separately; no combined full-suite output is available.
- No actual terminal runs cover the additional malformed-input/empty-value policies, empty plans, conflicting duplicates, or reordered-plan sorting.
- The original manual comparison contains a self-comparison typo; the later correction is preserved separately.
- No protected-file baseline/hash or Git diff/status output was supplied to prove unchanged contents independently.
- No apply or live AWS verification is evidenced or claimed.

## Setup-related output actually supplied

````text
((.venv) ) siddharthsharma@siddharths-MacBook-Pro haven-infra-assessment % terraform plan -refresh=false -input=false -var='landlord_accounts=["la-001","la-003","la-004"]'

╷

│ **Error: No configuration files**

│ 

│ Plan requires configuration to be present. Planning without a configuration

│ would mark everything for destruction, which is normally not what is desired.

│ If you would like to destroy everything, run plan with the -destroy option.

│ Otherwise, create a Terraform configuration file (.tf file) and try again.

╵

((.venv) ) siddharthsharma@siddharths-MacBook-Pro haven-infra-assessment % terraform plan -refresh=false -input=false -var='landlord_accounts=["la-001","la-003","la-004"]'

````


````text
((.venv) ) siddharthsharma@siddharths-MacBook-Pro haven-infra-assessment % terraform -chdir=terraform plan -refresh=false -input=false -var='landlord_accounts=["la-001","la-003","la-004"]'

╷

│ **Error: Inconsistent dependency lock file**

│ 

│ The following dependency selections recorded in the lock file are

│ inconsistent with the current configuration:

│   - provider registry.terraform.io/hashicorp/aws: required by this configuration but no version is selected

│ 

│ To make the initial dependency selections that will initialize the dependency

│ lock file, run:

│   terraform init

╵

((.venv) ) siddharthsharma@siddhar

````


## B2 access-control tests — initial stub failures

````text
((.venv) ) siddharthsharma@siddharths-MacBook-Pro haven-infra-assessment % python -m pytest tests/test_access_control.py -v
============================= test session starts ==============================
platform darwin -- Python 3.12.16, pytest-9.2.0, pluggy-1.7.0 -- /Users/siddharthsharma/Documents/haven-infra-assessment/.venv/bin/python
cachedir: .pytest_cache
rootdir: /Users/siddharthsharma/Documents/haven-infra-assessment
collected 4 items                                                              

tests/test_access_control.py::test_pm_001_cannot_access_rep_002 FAILED   [ 25%]
tests/test_access_control.py::test_pm_001_can_access_rep_001 FAILED      [ 50%]
tests/test_access_control.py::test_missing_report_tenant_denies_access FAILED [ 75%]
tests/test_access_control.py::test_missing_tenant_property_denies_access FAILED [100%]

=================================== FAILURES ===================================
______________________ test_pm_001_cannot_access_rep_002 _______________________

property_managers = [PropertyManager(id='pm-001', name='Asha Rao', landlord_account_id='la-001'), PropertyManager(id='pm-002', name='Leo Fontaine', landlord_account_id='la-002')]
properties = [Property(id='prop-001', landlord_account_id='la-001', address='12 Maple St'), Property(id='prop-002', landlord_account_id='la-002', address='88 Birch Ave')]
tenants = [Tenant(id='ten-001', name='J. Alvarez', property_id='prop-001'), Tenant(id='ten-002', name='S. Okafor', property_id='prop-002')]
screening_reports = [ScreeningReport(id='rep-001', tenant_id='ten-001', ssn_last4='1234', credit_score=710), ScreeningReport(id='rep-002', tenant_id='ten-002', ssn_last4='5678', credit_score=690)]

    def test_pm_001_cannot_access_rep_002(
        property_managers, properties, tenants, screening_reports
    ):
        actor = next(manager for manager in property_managers if manager.id == "pm-001")
        report = next(report for report in screening_reports if report.id == "rep-002")
    
>       assert can_access_screening_report(
            actor, report, properties=properties, tenants=tenants
        ) is False

tests/test_access_control.py:20: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

actor = PropertyManager(id='pm-001', name='Asha Rao', landlord_account_id='la-001')
report = ScreeningReport(id='rep-002', tenant_id='ten-002', ssn_last4='5678', credit_score=690)
properties = [Property(id='prop-001', landlord_account_id='la-001', address='12 Maple St'), Property(id='prop-002', landlord_account_id='la-002', address='88 Birch Ave')]
tenants = [Tenant(id='ten-001', name='J. Alvarez', property_id='prop-001'), Tenant(id='ten-002', name='S. Okafor', property_id='prop-002')]

    def can_access_screening_report(
        actor: PropertyManager,
        report: ScreeningReport,
        *,
        properties: list[Property],
        tenants: list[Tenant],
    ) -> bool:
        """
        actor: the PropertyManager requesting access
        report: the ScreeningReport they're trying to view
        properties: all known Property records
        tenants: all known Tenant records
    
        Return True if actor may view report, False otherwise. Fail closed — if anything needed to
        make this determination is missing (tenant not found, property not found), return False.
        """
>       raise NotImplementedError("Implement this.")
E       NotImplementedError: Implement this.

app/access_control.py:29: NotImplementedError
________________________ test_pm_001_can_access_rep_001 ________________________

property_managers = [PropertyManager(id='pm-001', name='Asha Rao', landlord_account_id='la-001'), PropertyManager(id='pm-002', name='Leo Fontaine', landlord_account_id='la-002')]
properties = [Property(id='prop-001', landlord_account_id='la-001', address='12 Maple St'), Property(id='prop-002', landlord_account_id='la-002', address='88 Birch Ave')]
tenants = [Tenant(id='ten-001', name='J. Alvarez', property_id='prop-001'), Tenant(id='ten-002', name='S. Okafor', property_id='prop-002')]
screening_reports = [ScreeningReport(id='rep-001', tenant_id='ten-001', ssn_last4='1234', credit_score=710), ScreeningReport(id='rep-002', tenant_id='ten-002', ssn_last4='5678', credit_score=690)]

    def test_pm_001_can_access_rep_001(
        property_managers, properties, tenants, screening_reports
    ):
        actor = next(manager for manager in property_managers if manager.id == "pm-001")
        report = next(report for report in screening_reports if report.id == "rep-001")
    
>       assert can_access_screening_report(
            actor, report, properties=properties, tenants=tenants
        ) is True

tests/test_access_control.py:31: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

actor = PropertyManager(id='pm-001', name='Asha Rao', landlord_account_id='la-001')
report = ScreeningReport(id='rep-001', tenant_id='ten-001', ssn_last4='1234', credit_score=710)
properties = [Property(id='prop-001', landlord_account_id='la-001', address='12 Maple St'), Property(id='prop-002', landlord_account_id='la-002', address='88 Birch Ave')]
tenants = [Tenant(id='ten-001', name='J. Alvarez', property_id='prop-001'), Tenant(id='ten-002', name='S. Okafor', property_id='prop-002')]

    def can_access_screening_report(
        actor: PropertyManager,
        report: ScreeningReport,
        *,
        properties: list[Property],
        tenants: list[Tenant],
    ) -> bool:
        """
        actor: the PropertyManager requesting access
        report: the ScreeningReport they're trying to view
        properties: all known Property records
        tenants: all known Tenant records
    
        Return True if actor may view report, False otherwise. Fail closed — if anything needed to
        make this determination is missing (tenant not found, property not found), return False.
        """
>       raise NotImplementedError("Implement this.")
E       NotImplementedError: Implement this.

app/access_control.py:29: NotImplementedError
___________________ test_missing_report_tenant_denies_access ___________________

property_managers = [PropertyManager(id='pm-001', name='Asha Rao', landlord_account_id='la-001'), PropertyManager(id='pm-002', name='Leo Fontaine', landlord_account_id='la-002')]
properties = [Property(id='prop-001', landlord_account_id='la-001', address='12 Maple St'), Property(id='prop-002', landlord_account_id='la-002', address='88 Birch Ave')]
tenants = [Tenant(id='ten-001', name='J. Alvarez', property_id='prop-001'), Tenant(id='ten-002', name='S. Okafor', property_id='prop-002')]
screening_reports = [ScreeningReport(id='rep-001', tenant_id='ten-001', ssn_last4='1234', credit_score=710), ScreeningReport(id='rep-002', tenant_id='ten-002', ssn_last4='5678', credit_score=690)]

    def test_missing_report_tenant_denies_access(
        property_managers, properties, tenants, screening_reports
    ):
        actor = next(manager for manager in property_managers if manager.id == "pm-001")
        report = next(report for report in screening_reports if report.id == "rep-001")
        remaining_tenants = [tenant for tenant in tenants if tenant.id != report.tenant_id]
    
>       assert can_access_screening_report(
            actor, report, properties=properties, tenants=remaining_tenants
        ) is False

tests/test_access_control.py:43: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

actor = PropertyManager(id='pm-001', name='Asha Rao', landlord_account_id='la-001')
report = ScreeningReport(id='rep-001', tenant_id='ten-001', ssn_last4='1234', credit_score=710)
properties = [Property(id='prop-001', landlord_account_id='la-001', address='12 Maple St'), Property(id='prop-002', landlord_account_id='la-002', address='88 Birch Ave')]
tenants = [Tenant(id='ten-002', name='S. Okafor', property_id='prop-002')]

    def can_access_screening_report(
        actor: PropertyManager,
        report: ScreeningReport,
        *,
        properties: list[Property],
        tenants: list[Tenant],
    ) -> bool:
        """
        actor: the PropertyManager requesting access
        report: the ScreeningReport they're trying to view
        properties: all known Property records
        tenants: all known Tenant records
    
        Return True if actor may view report, False otherwise. Fail closed — if anything needed to
        make this determination is missing (tenant not found, property not found), return False.
        """
>       raise NotImplementedError("Implement this.")
E       NotImplementedError: Implement this.

app/access_control.py:29: NotImplementedError
__________________ test_missing_tenant_property_denies_access __________________

property_managers = [PropertyManager(id='pm-001', name='Asha Rao', landlord_account_id='la-001'), PropertyManager(id='pm-002', name='Leo Fontaine', landlord_account_id='la-002')]
properties = [Property(id='prop-001', landlord_account_id='la-001', address='12 Maple St'), Property(id='prop-002', landlord_account_id='la-002', address='88 Birch Ave')]
tenants = [Tenant(id='ten-001', name='J. Alvarez', property_id='prop-001'), Tenant(id='ten-002', name='S. Okafor', property_id='prop-002')]
screening_reports = [ScreeningReport(id='rep-001', tenant_id='ten-001', ssn_last4='1234', credit_score=710), ScreeningReport(id='rep-002', tenant_id='ten-002', ssn_last4='5678', credit_score=690)]

    def test_missing_tenant_property_denies_access(
        property_managers, properties, tenants, screening_reports
    ):
        actor = next(manager for manager in property_managers if manager.id == "pm-001")
        report = next(report for report in screening_reports if report.id == "rep-001")
        tenant = next(tenant for tenant in tenants if tenant.id == report.tenant_id)
        remaining_properties = [
            property_ for property_ in properties if property_.id != tenant.property_id
        ]
    
>       assert can_access_screening_report(
            actor, report, properties=remaining_properties, tenants=tenants
        ) is False

tests/test_access_control.py:58: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

actor = PropertyManager(id='pm-001', name='Asha Rao', landlord_account_id='la-001')
report = ScreeningReport(id='rep-001', tenant_id='ten-001', ssn_last4='1234', credit_score=710)
properties = [Property(id='prop-002', landlord_account_id='la-002', address='88 Birch Ave')]
tenants = [Tenant(id='ten-001', name='J. Alvarez', property_id='prop-001'), Tenant(id='ten-002', name='S. Okafor', property_id='prop-002')]

    def can_access_screening_report(
        actor: PropertyManager,
        report: ScreeningReport,
        *,
        properties: list[Property],
        tenants: list[Tenant],
    ) -> bool:
        """
        actor: the PropertyManager requesting access
        report: the ScreeningReport they're trying to view
        properties: all known Property records
        tenants: all known Tenant records
    
        Return True if actor may view report, False otherwise. Fail closed — if anything needed to
        make this determination is missing (tenant not found, property not found), return False.
        """
>       raise NotImplementedError("Implement this.")
E       NotImplementedError: Implement this.

app/access_control.py:29: NotImplementedError
=========================== short test summary info ============================
FAILED tests/test_access_control.py::test_pm_001_cannot_access_rep_002 - NotImplementedError: Implement this.
FAILED tests/test_access_control.py::test_pm_001_can_access_rep_001 - NotImplementedError: Implement this.
FAILED tests/test_access_control.py::test_missing_report_tenant_denies_access - NotImplementedError: Implement this.
FAILED tests/test_access_control.py::test_missing_tenant_property_denies_access - NotImplementedError: Implement this.
============================== 4 failed in 0.04s ===============================
((.venv) ) siddharthsharma@siddharths-MacBook-Pro haven-infra-assessment % 

````


## B2 access-control tests — passing run

````text
((.venv) ) siddharthsharma@siddharths-MacBook-Pro haven-infra-assessment % 

((.venv) ) siddharthsharma@siddharths-MacBook-Pro haven-infra-assessment %                                                                                 python -m pytest tests/test_access_control.py -v

**============================= test session starts ==============================**&#x6E; -m pytest tests/test_access_control.py -v

platform darwin -- Python 3.12.16, pytest-9.2.0, pluggy-1.7.0 -- /Users/siddharthsharma/Documents/haven-infra-assessment/.venv/bin/python

cachedir: .pytest_cache

rootdir: /Users/siddharthsharma/Documents/haven-infra-assessment

**collected 4 items                                                             &#xA0;**

tests/test_access_control.py::test_pm_001_cannot_access_rep_002 PASSED   [ 25%]

tests/test_access_control.py::test_pm_001_can_access_rep_001 PASSED      [ 50%]

tests/test_access_control.py::test_missing_report_tenant_denies_access PASSED [ 75%]

tests/test_access_control.py::test_missing_tenant_property_denies_access PASSED [100%]

\============================== **4 passed** in 0.01s ===============================

((.venv) ) siddharthsharma@siddharths-MacBook-Pro haven-infra-assessment % 

````


## B2 cost-tag tests — initial stub failures

````text
((.venv) ) siddharthsharma@siddharths-MacBook-Pro haven-infra-assessment %                                                                                 python -m pytest tests/test_cost_tag_check.py -v
============================= test session starts ==============================n -m pytest tests/test_cost_tag_check.py -v
platform darwin -- Python 3.12.16, pytest-9.2.0, pluggy-1.7.0 -- /Users/siddharthsharma/Documents/haven-infra-assessment/.venv/bin/python
cachedir: .pytest_cache
rootdir: /Users/siddharthsharma/Documents/haven-infra-assessment
collected 16 items                                                             

tests/test_cost_tag_check.py::test_fixture_reports_exactly_the_two_missing_billing_tags FAILED [  6%]
tests/test_cost_tag_check.py::test_correctly_tagged_actionable_resource_passes[actions0] FAILED [ 12%]
tests/test_cost_tag_check.py::test_correctly_tagged_actionable_resource_passes[actions1] FAILED [ 18%]
tests/test_cost_tag_check.py::test_non_actionable_resource_is_skipped[actions0] FAILED [ 25%]
tests/test_cost_tag_check.py::test_non_actionable_resource_is_skipped[actions1] FAILED [ 31%]
tests/test_cost_tag_check.py::test_non_actionable_resource_is_skipped[actions2] FAILED [ 37%]
tests/test_cost_tag_check.py::test_replacement_checks_the_after_tags[False-actions0] FAILED [ 43%]
tests/test_cost_tag_check.py::test_replacement_checks_the_after_tags[False-actions1] FAILED [ 50%]
tests/test_cost_tag_check.py::test_replacement_checks_the_after_tags[True-actions0] FAILED [ 56%]
tests/test_cost_tag_check.py::test_replacement_checks_the_after_tags[True-actions1] FAILED [ 62%]
tests/test_cost_tag_check.py::test_other_types_and_names_are_checked[aws_sqs_queue.unlisted_queue-actions0] FAILED [ 68%]
tests/test_cost_tag_check.py::test_other_types_and_names_are_checked[aws_sqs_queue.unlisted_queue-actions1] FAILED [ 75%]
tests/test_cost_tag_check.py::test_other_types_and_names_are_checked[aws_dynamodb_table.unlisted_table-actions0] FAILED [ 81%]
tests/test_cost_tag_check.py::test_other_types_and_names_are_checked[aws_dynamodb_table.unlisted_table-actions1] FAILED [ 87%]
tests/test_cost_tag_check.py::test_repeated_calls_have_identical_exit_code_and_output FAILED [ 93%]
tests/test_cost_tag_check.py::test_duplicate_full_addresses_are_reported_once FAILED [100%]

=================================== FAILURES ===================================
__________ test_fixture_reports_exactly_the_two_missing_billing_tags ___________

capsys = <_pytest.capture.CaptureFixture object at 0x10895f440>

    def test_fixture_reports_exactly_the_two_missing_billing_tags(capsys):
>       result = check_plan(str(PLAN_FIXTURE))
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

tests/test_cost_tag_check.py:43: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

plan_path = '/Users/siddharthsharma/Documents/haven-infra-assessment/fixtures/plan.json'

    def check_plan(plan_path: str) -> int:
        """
        Returns an exit code: 0 if every resource being created or updated has
        `landlord_account_id`, non-zero otherwise.
        """
>       raise NotImplementedError("Implement this.")
E       NotImplementedError: Implement this.

scripts/cost_tag_check.py:30: NotImplementedError
__________ test_correctly_tagged_actionable_resource_passes[actions0] __________

tmp_path = PosixPath('/private/var/folders/dx/76wx5_z55t1gyx0xzql12rzm0000gn/T/pytest-of-siddharthsharma/pytest-0/test_correctly_tagged_actionab0')
capsys = <_pytest.capture.CaptureFixture object at 0x1089a3f80>
actions = ['create']

    @pytest.mark.parametrize("actions", [["create"], ["update"]])
    def test_correctly_tagged_actionable_resource_passes(tmp_path, capsys, actions):
        address = "aws_sqs_queue.billing_events"
        plan_path = write_plan(tmp_path, [resource_change(
            address, actions, {"landlord_account_id": "la-001"}
        )])
    
>       assert check_plan(plan_path) == 0
               ^^^^^^^^^^^^^^^^^^^^^

tests/test_cost_tag_check.py:65: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

plan_path = '/private/var/folders/dx/76wx5_z55t1gyx0xzql12rzm0000gn/T/pytest-of-siddharthsharma/pytest-0/test_correctly_tagged_actionab0/plan.json'

    def check_plan(plan_path: str) -> int:
        """
        Returns an exit code: 0 if every resource being created or updated has
        `landlord_account_id`, non-zero otherwise.
        """
>       raise NotImplementedError("Implement this.")
E       NotImplementedError: Implement this.

scripts/cost_tag_check.py:30: NotImplementedError
__________ test_correctly_tagged_actionable_resource_passes[actions1] __________

tmp_path = PosixPath('/private/var/folders/dx/76wx5_z55t1gyx0xzql12rzm0000gn/T/pytest-of-siddharthsharma/pytest-0/test_correctly_tagged_actionab1')
capsys = <_pytest.capture.CaptureFixture object at 0x1089fdb50>
actions = ['update']

    @pytest.mark.parametrize("actions", [["create"], ["update"]])
    def test_correctly_tagged_actionable_resource_passes(tmp_path, capsys, actions):
        address = "aws_sqs_queue.billing_events"
        plan_path = write_plan(tmp_path, [resource_change(
            address, actions, {"landlord_account_id": "la-001"}
        )])
    
>       assert check_plan(plan_path) == 0
               ^^^^^^^^^^^^^^^^^^^^^

tests/test_cost_tag_check.py:65: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

plan_path = '/private/var/folders/dx/76wx5_z55t1gyx0xzql12rzm0000gn/T/pytest-of-siddharthsharma/pytest-0/test_correctly_tagged_actionab1/plan.json'

    def check_plan(plan_path: str) -> int:
        """
        Returns an exit code: 0 if every resource being created or updated has
        `landlord_account_id`, non-zero otherwise.
        """
>       raise NotImplementedError("Implement this.")
E       NotImplementedError: Implement this.

scripts/cost_tag_check.py:30: NotImplementedError
______________ test_non_actionable_resource_is_skipped[actions0] _______________

tmp_path = PosixPath('/private/var/folders/dx/76wx5_z55t1gyx0xzql12rzm0000gn/T/pytest-of-siddharthsharma/pytest-0/test_non_actionable_resource_i0')
capsys = <_pytest.capture.CaptureFixture object at 0x1089fdca0>
actions = ['no-op']

    @pytest.mark.parametrize("actions", [["no-op"], ["read"], ["delete"]])
    def test_non_actionable_resource_is_skipped(tmp_path, capsys, actions):
        address = "aws_sqs_queue.untagged_unchanged"
        resource = resource_change(address, actions, {})
        if actions == ["delete"]:
            del resource["change"]["after"]
        plan_path = write_plan(tmp_path, [resource])
    
>       assert check_plan(plan_path) == 0
               ^^^^^^^^^^^^^^^^^^^^^

tests/test_cost_tag_check.py:78: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

plan_path = '/private/var/folders/dx/76wx5_z55t1gyx0xzql12rzm0000gn/T/pytest-of-siddharthsharma/pytest-0/test_non_actionable_resource_i0/plan.json'

    def check_plan(plan_path: str) -> int:
        """
        Returns an exit code: 0 if every resource being created or updated has
        `landlord_account_id`, non-zero otherwise.
        """
>       raise NotImplementedError("Implement this.")
E       NotImplementedError: Implement this.

scripts/cost_tag_check.py:30: NotImplementedError
______________ test_non_actionable_resource_is_skipped[actions1] _______________

tmp_path = PosixPath('/private/var/folders/dx/76wx5_z55t1gyx0xzql12rzm0000gn/T/pytest-of-siddharthsharma/pytest-0/test_non_actionable_resource_i1')
capsys = <_pytest.capture.CaptureFixture object at 0x10895cfb0>
actions = ['read']

    @pytest.mark.parametrize("actions", [["no-op"], ["read"], ["delete"]])
    def test_non_actionable_resource_is_skipped(tmp_path, capsys, actions):
        address = "aws_sqs_queue.untagged_unchanged"
        resource = resource_change(address, actions, {})
        if actions == ["delete"]:
            del resource["change"]["after"]
        plan_path = write_plan(tmp_path, [resource])
    
>       assert check_plan(plan_path) == 0
               ^^^^^^^^^^^^^^^^^^^^^

tests/test_cost_tag_check.py:78: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

plan_path = '/private/var/folders/dx/76wx5_z55t1gyx0xzql12rzm0000gn/T/pytest-of-siddharthsharma/pytest-0/test_non_actionable_resource_i1/plan.json'

    def check_plan(plan_path: str) -> int:
        """
        Returns an exit code: 0 if every resource being created or updated has
        `landlord_account_id`, non-zero otherwise.
        """
>       raise NotImplementedError("Implement this.")
E       NotImplementedError: Implement this.

scripts/cost_tag_check.py:30: NotImplementedError
______________ test_non_actionable_resource_is_skipped[actions2] _______________

tmp_path = PosixPath('/private/var/folders/dx/76wx5_z55t1gyx0xzql12rzm0000gn/T/pytest-of-siddharthsharma/pytest-0/test_non_actionable_resource_i2')
capsys = <_pytest.capture.CaptureFixture object at 0x1089ff020>
actions = ['delete']

    @pytest.mark.parametrize("actions", [["no-op"], ["read"], ["delete"]])
    def test_non_actionable_resource_is_skipped(tmp_path, capsys, actions):
        address = "aws_sqs_queue.untagged_unchanged"
        resource = resource_change(address, actions, {})
        if actions == ["delete"]:
            del resource["change"]["after"]
        plan_path = write_plan(tmp_path, [resource])
    
>       assert check_plan(plan_path) == 0
               ^^^^^^^^^^^^^^^^^^^^^

tests/test_cost_tag_check.py:78: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

plan_path = '/private/var/folders/dx/76wx5_z55t1gyx0xzql12rzm0000gn/T/pytest-of-siddharthsharma/pytest-0/test_non_actionable_resource_i2/plan.json'

    def check_plan(plan_path: str) -> int:
        """
        Returns an exit code: 0 if every resource being created or updated has
        `landlord_account_id`, non-zero otherwise.
        """
>       raise NotImplementedError("Implement this.")
E       NotImplementedError: Implement this.

scripts/cost_tag_check.py:30: NotImplementedError
____________ test_replacement_checks_the_after_tags[False-actions0] ____________

tmp_path = PosixPath('/private/var/folders/dx/76wx5_z55t1gyx0xzql12rzm0000gn/T/pytest-of-siddharthsharma/pytest-0/test_replacement_checks_the_af0')
capsys = <_pytest.capture.CaptureFixture object at 0x1089fdaf0>
actions = ['delete', 'create'], tagged = False

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
    
>       result = check_plan(plan_path)
                 ^^^^^^^^^^^^^^^^^^^^^

tests/test_cost_tag_check.py:95: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

plan_path = '/private/var/folders/dx/76wx5_z55t1gyx0xzql12rzm0000gn/T/pytest-of-siddharthsharma/pytest-0/test_replacement_checks_the_af0/plan.json'

    def check_plan(plan_path: str) -> int:
        """
        Returns an exit code: 0 if every resource being created or updated has
        `landlord_account_id`, non-zero otherwise.
        """
>       raise NotImplementedError("Implement this.")
E       NotImplementedError: Implement this.

scripts/cost_tag_check.py:30: NotImplementedError
____________ test_replacement_checks_the_after_tags[False-actions1] ____________

tmp_path = PosixPath('/private/var/folders/dx/76wx5_z55t1gyx0xzql12rzm0000gn/T/pytest-of-siddharthsharma/pytest-0/test_replacement_checks_the_af1')
capsys = <_pytest.capture.CaptureFixture object at 0x1089fe660>
actions = ['create', 'delete'], tagged = False

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
    
>       result = check_plan(plan_path)
                 ^^^^^^^^^^^^^^^^^^^^^

tests/test_cost_tag_check.py:95: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

plan_path = '/private/var/folders/dx/76wx5_z55t1gyx0xzql12rzm0000gn/T/pytest-of-siddharthsharma/pytest-0/test_replacement_checks_the_af1/plan.json'

    def check_plan(plan_path: str) -> int:
        """
        Returns an exit code: 0 if every resource being created or updated has
        `landlord_account_id`, non-zero otherwise.
        """
>       raise NotImplementedError("Implement this.")
E       NotImplementedError: Implement this.

scripts/cost_tag_check.py:30: NotImplementedError
____________ test_replacement_checks_the_after_tags[True-actions0] _____________

tmp_path = PosixPath('/private/var/folders/dx/76wx5_z55t1gyx0xzql12rzm0000gn/T/pytest-of-siddharthsharma/pytest-0/test_replacement_checks_the_af2')
capsys = <_pytest.capture.CaptureFixture object at 0x1089fea80>
actions = ['delete', 'create'], tagged = True

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
    
>       result = check_plan(plan_path)
                 ^^^^^^^^^^^^^^^^^^^^^

tests/test_cost_tag_check.py:95: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

plan_path = '/private/var/folders/dx/76wx5_z55t1gyx0xzql12rzm0000gn/T/pytest-of-siddharthsharma/pytest-0/test_replacement_checks_the_af2/plan.json'

    def check_plan(plan_path: str) -> int:
        """
        Returns an exit code: 0 if every resource being created or updated has
        `landlord_account_id`, non-zero otherwise.
        """
>       raise NotImplementedError("Implement this.")
E       NotImplementedError: Implement this.

scripts/cost_tag_check.py:30: NotImplementedError
____________ test_replacement_checks_the_after_tags[True-actions1] _____________

tmp_path = PosixPath('/private/var/folders/dx/76wx5_z55t1gyx0xzql12rzm0000gn/T/pytest-of-siddharthsharma/pytest-0/test_replacement_checks_the_af3')
capsys = <_pytest.capture.CaptureFixture object at 0x1089fcd10>
actions = ['create', 'delete'], tagged = True

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
    
>       result = check_plan(plan_path)
                 ^^^^^^^^^^^^^^^^^^^^^

tests/test_cost_tag_check.py:95: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

plan_path = '/private/var/folders/dx/76wx5_z55t1gyx0xzql12rzm0000gn/T/pytest-of-siddharthsharma/pytest-0/test_replacement_checks_the_af3/plan.json'

    def check_plan(plan_path: str) -> int:
        """
        Returns an exit code: 0 if every resource being created or updated has
        `landlord_account_id`, non-zero otherwise.
        """
>       raise NotImplementedError("Implement this.")
E       NotImplementedError: Implement this.

scripts/cost_tag_check.py:30: NotImplementedError
_ test_other_types_and_names_are_checked[aws_sqs_queue.unlisted_queue-actions0] _

tmp_path = PosixPath('/private/var/folders/dx/76wx5_z55t1gyx0xzql12rzm0000gn/T/pytest-of-siddharthsharma/pytest-0/test_other_types_and_names_are0')
capsys = <_pytest.capture.CaptureFixture object at 0x1089fe930>
actions = ['create'], address = 'aws_sqs_queue.unlisted_queue'

    @pytest.mark.parametrize("actions", [["create"], ["update"]])
    @pytest.mark.parametrize("address", [
        "aws_sqs_queue.unlisted_queue",
        "aws_dynamodb_table.unlisted_table",
    ])
    def test_other_types_and_names_are_checked(tmp_path, capsys, actions, address):
        plan_path = write_plan(tmp_path, [resource_change(
            address, actions, {"tenant_id": "ten-001"}
        )])
    
>       assert check_plan(plan_path) != 0
               ^^^^^^^^^^^^^^^^^^^^^

tests/test_cost_tag_check.py:116: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

plan_path = '/private/var/folders/dx/76wx5_z55t1gyx0xzql12rzm0000gn/T/pytest-of-siddharthsharma/pytest-0/test_other_types_and_names_are0/plan.json'

    def check_plan(plan_path: str) -> int:
        """
        Returns an exit code: 0 if every resource being created or updated has
        `landlord_account_id`, non-zero otherwise.
        """
>       raise NotImplementedError("Implement this.")
E       NotImplementedError: Implement this.

scripts/cost_tag_check.py:30: NotImplementedError
_ test_other_types_and_names_are_checked[aws_sqs_queue.unlisted_queue-actions1] _

tmp_path = PosixPath('/private/var/folders/dx/76wx5_z55t1gyx0xzql12rzm0000gn/T/pytest-of-siddharthsharma/pytest-0/test_other_types_and_names_are1')
capsys = <_pytest.capture.CaptureFixture object at 0x108a11c10>
actions = ['update'], address = 'aws_sqs_queue.unlisted_queue'

    @pytest.mark.parametrize("actions", [["create"], ["update"]])
    @pytest.mark.parametrize("address", [
        "aws_sqs_queue.unlisted_queue",
        "aws_dynamodb_table.unlisted_table",
    ])
    def test_other_types_and_names_are_checked(tmp_path, capsys, actions, address):
        plan_path = write_plan(tmp_path, [resource_change(
            address, actions, {"tenant_id": "ten-001"}
        )])
    
>       assert check_plan(plan_path) != 0
               ^^^^^^^^^^^^^^^^^^^^^

tests/test_cost_tag_check.py:116: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

plan_path = '/private/var/folders/dx/76wx5_z55t1gyx0xzql12rzm0000gn/T/pytest-of-siddharthsharma/pytest-0/test_other_types_and_names_are1/plan.json'

    def check_plan(plan_path: str) -> int:
        """
        Returns an exit code: 0 if every resource being created or updated has
        `landlord_account_id`, non-zero otherwise.
        """
>       raise NotImplementedError("Implement this.")
E       NotImplementedError: Implement this.

scripts/cost_tag_check.py:30: NotImplementedError
_ test_other_types_and_names_are_checked[aws_dynamodb_table.unlisted_table-actions0] _

tmp_path = PosixPath('/private/var/folders/dx/76wx5_z55t1gyx0xzql12rzm0000gn/T/pytest-of-siddharthsharma/pytest-0/test_other_types_and_names_are2')
capsys = <_pytest.capture.CaptureFixture object at 0x108a112e0>
actions = ['create'], address = 'aws_dynamodb_table.unlisted_table'

    @pytest.mark.parametrize("actions", [["create"], ["update"]])
    @pytest.mark.parametrize("address", [
        "aws_sqs_queue.unlisted_queue",
        "aws_dynamodb_table.unlisted_table",
    ])
    def test_other_types_and_names_are_checked(tmp_path, capsys, actions, address):
        plan_path = write_plan(tmp_path, [resource_change(
            address, actions, {"tenant_id": "ten-001"}
        )])
    
>       assert check_plan(plan_path) != 0
               ^^^^^^^^^^^^^^^^^^^^^

tests/test_cost_tag_check.py:116: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

plan_path = '/private/var/folders/dx/76wx5_z55t1gyx0xzql12rzm0000gn/T/pytest-of-siddharthsharma/pytest-0/test_other_types_and_names_are2/plan.json'

    def check_plan(plan_path: str) -> int:
        """
        Returns an exit code: 0 if every resource being created or updated has
        `landlord_account_id`, non-zero otherwise.
        """
>       raise NotImplementedError("Implement this.")
E       NotImplementedError: Implement this.

scripts/cost_tag_check.py:30: NotImplementedError
_ test_other_types_and_names_are_checked[aws_dynamodb_table.unlisted_table-actions1] _

tmp_path = PosixPath('/private/var/folders/dx/76wx5_z55t1gyx0xzql12rzm0000gn/T/pytest-of-siddharthsharma/pytest-0/test_other_types_and_names_are3')
capsys = <_pytest.capture.CaptureFixture object at 0x108a11a90>
actions = ['update'], address = 'aws_dynamodb_table.unlisted_table'

    @pytest.mark.parametrize("actions", [["create"], ["update"]])
    @pytest.mark.parametrize("address", [
        "aws_sqs_queue.unlisted_queue",
        "aws_dynamodb_table.unlisted_table",
    ])
    def test_other_types_and_names_are_checked(tmp_path, capsys, actions, address):
        plan_path = write_plan(tmp_path, [resource_change(
            address, actions, {"tenant_id": "ten-001"}
        )])
    
>       assert check_plan(plan_path) != 0
               ^^^^^^^^^^^^^^^^^^^^^

tests/test_cost_tag_check.py:116: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

plan_path = '/private/var/folders/dx/76wx5_z55t1gyx0xzql12rzm0000gn/T/pytest-of-siddharthsharma/pytest-0/test_other_types_and_names_are3/plan.json'

    def check_plan(plan_path: str) -> int:
        """
        Returns an exit code: 0 if every resource being created or updated has
        `landlord_account_id`, non-zero otherwise.
        """
>       raise NotImplementedError("Implement this.")
E       NotImplementedError: Implement this.

scripts/cost_tag_check.py:30: NotImplementedError
___________ test_repeated_calls_have_identical_exit_code_and_output ____________

capsys = <_pytest.capture.CaptureFixture object at 0x108a13f50>

    def test_repeated_calls_have_identical_exit_code_and_output(capsys):
>       first_result = check_plan(str(PLAN_FIXTURE))
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

tests/test_cost_tag_check.py:122: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

plan_path = '/Users/siddharthsharma/Documents/haven-infra-assessment/fixtures/plan.json'

    def check_plan(plan_path: str) -> int:
        """
        Returns an exit code: 0 if every resource being created or updated has
        `landlord_account_id`, non-zero otherwise.
        """
>       raise NotImplementedError("Implement this.")
E       NotImplementedError: Implement this.

scripts/cost_tag_check.py:30: NotImplementedError
_______________ test_duplicate_full_addresses_are_reported_once ________________

tmp_path = PosixPath('/private/var/folders/dx/76wx5_z55t1gyx0xzql12rzm0000gn/T/pytest-of-siddharthsharma/pytest-0/test_duplicate_full_addresses_0')
capsys = <_pytest.capture.CaptureFixture object at 0x108a137d0>

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
    
>       assert check_plan(plan_path) != 0
               ^^^^^^^^^^^^^^^^^^^^^

tests/test_cost_tag_check.py:148: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

plan_path = '/private/var/folders/dx/76wx5_z55t1gyx0xzql12rzm0000gn/T/pytest-of-siddharthsharma/pytest-0/test_duplicate_full_addresses_0/plan.json'

    def check_plan(plan_path: str) -> int:
        """
        Returns an exit code: 0 if every resource being created or updated has
        `landlord_account_id`, non-zero otherwise.
        """
>       raise NotImplementedError("Implement this.")
E       NotImplementedError: Implement this.

scripts/cost_tag_check.py:30: NotImplementedError
=========================== short test summary info ============================
FAILED tests/test_cost_tag_check.py::test_fixture_reports_exactly_the_two_missing_billing_tags - NotImplementedError: Implement this.
FAILED tests/test_cost_tag_check.py::test_correctly_tagged_actionable_resource_passes[actions0] - NotImplementedError: Implement this.
FAILED tests/test_cost_tag_check.py::test_correctly_tagged_actionable_resource_passes[actions1] - NotImplementedError: Implement this.
FAILED tests/test_cost_tag_check.py::test_non_actionable_resource_is_skipped[actions0] - NotImplementedError: Implement this.
FAILED tests/test_cost_tag_check.py::test_non_actionable_resource_is_skipped[actions1] - NotImplementedError: Implement this.
FAILED tests/test_cost_tag_check.py::test_non_actionable_resource_is_skipped[actions2] - NotImplementedError: Implement this.
FAILED tests/test_cost_tag_check.py::test_replacement_checks_the_after_tags[False-actions0] - NotImplementedError: Implement this.
FAILED tests/test_cost_tag_check.py::test_replacement_checks_the_after_tags[False-actions1] - NotImplementedError: Implement this.
FAILED tests/test_cost_tag_check.py::test_replacement_checks_the_after_tags[True-actions0] - NotImplementedError: Implement this.
FAILED tests/test_cost_tag_check.py::test_replacement_checks_the_after_tags[True-actions1] - NotImplementedError: Implement this.
FAILED tests/test_cost_tag_check.py::test_other_types_and_names_are_checked[aws_sqs_queue.unlisted_queue-actions0] - NotImplementedError: Implement this.
FAILED tests/test_cost_tag_check.py::test_other_types_and_names_are_checked[aws_sqs_queue.unlisted_queue-actions1] - NotImplementedError: Implement this.
FAILED tests/test_cost_tag_check.py::test_other_types_and_names_are_checked[aws_dynamodb_table.unlisted_table-actions0] - NotImplementedError: Implement this.
FAILED tests/test_cost_tag_check.py::test_other_types_and_names_are_checked[aws_dynamodb_table.unlisted_table-actions1] - NotImplementedError: Implement this.
FAILED tests/test_cost_tag_check.py::test_repeated_calls_have_identical_exit_code_and_output - NotImplementedError: Implement this.
FAILED tests/test_cost_tag_check.py::test_duplicate_full_addresses_are_reported_once - NotImplementedError: Implement this.
============================== 16 failed in 0.07s ==============================
((.venv) ) siddharthsharma@siddharths-MacBook-Pro haven-infra-assessment % 

````


## B2 cost-tag tests — passing run

````text
((.venv) ) siddharthsharma@siddharths-MacBook-Pro haven-infra-assessment % 

((.venv) ) siddharthsharma@siddharths-MacBook-Pro haven-infra-assessment %                                                                                 python -m pytest tests/test_cost_tag_check.py -v

**============================= test session starts ==============================**&#x6E; -m pytest tests/test_cost_tag_check.py -v

platform darwin -- Python 3.12.16, pytest-9.2.0, pluggy-1.7.0 -- /Users/siddharthsharma/Documents/haven-infra-assessment/.venv/bin/python

cachedir: .pytest_cache

rootdir: /Users/siddharthsharma/Documents/haven-infra-assessment

**collected 16 items                                                            &#xA0;**

tests/test_cost_tag_check.py::test_fixture_reports_exactly_the_two_missing_billing_tags PASSED [  6%]

tests/test_cost_tag_check.py::test_correctly_tagged_actionable_resource_passes[actions0] PASSED [ 12%]

tests/test_cost_tag_check.py::test_correctly_tagged_actionable_resource_passes[actions1] PASSED [ 18%]

tests/test_cost_tag_check.py::test_non_actionable_resource_is_skipped[actions0] PASSED [ 25%]

tests/test_cost_tag_check.py::test_non_actionable_resource_is_skipped[actions1] PASSED [ 31%]

tests/test_cost_tag_check.py::test_non_actionable_resource_is_skipped[actions2] PASSED [ 37%]

tests/test_cost_tag_check.py::test_replacement_checks_the_after_tags[False-actions0] PASSED [ 43%]

tests/test_cost_tag_check.py::test_replacement_checks_the_after_tags[False-actions1] PASSED [ 50%]

tests/test_cost_tag_check.py::test_replacement_checks_the_after_tags[True-actions0] PASSED [ 56%]

tests/test_cost_tag_check.py::test_replacement_checks_the_after_tags[True-actions1] PASSED [ 62%]

tests/test_cost_tag_check.py::test_other_types_and_names_are_checked[aws_sqs_queue.unlisted_queue-actions0] PASSED [ 68%]

tests/test_cost_tag_check.py::test_other_types_and_names_are_checked[aws_sqs_queue.unlisted_queue-actions1] PASSED [ 75%]

tests/test_cost_tag_check.py::test_other_types_and_names_are_checked[aws_dynamodb_table.unlisted_table-actions0] PASSED [ 81%]

tests/test_cost_tag_check.py::test_other_types_and_names_are_checked[aws_dynamodb_table.unlisted_table-actions1] PASSED [ 87%]

tests/test_cost_tag_check.py::test_repeated_calls_have_identical_exit_code_and_output PASSED [ 93%]

tests/test_cost_tag_check.py::test_duplicate_full_addresses_are_reported_once PASSED [100%]

\============================== **16 passed** in 0.02s ==============================

((.venv) ) siddharthsharma@siddharths-MacBook-Pro haven-infra-assessment % 

````


## Manual checker runs — original supplied record

Both checker runs explicitly captured exit code 1. The second printf label also says "first exit code", but it prints rc2. The diff comparison returned 0. The final test in this original record compares rc1 to itself and does not establish equality between rc1 and rc2.

````text
siddharthsharma@siddharths-MacBook-Pro haven-infra-assessment % python scripts/cost_tag_check.py fixtures/plan.json > /tmp/haven-cost-1.txt

siddharthsharma@siddharths-MacBook-Pro haven-infra-assessment % rc1=$?

siddharthsharma@siddharths-MacBook-Pro haven-infra-assessment % cat /tmp/haven-cost-1.txt 

aws_lambda_function.mls_feed_sync: missing or empty landlord_account_id

aws_s3_bucket.listing_media: missing or empty landlord_account_id

siddharthsharma@siddharths-MacBook-Pro haven-infra-assessment % printf 'first exit code: %s\n' "$rc1"

first exit code: 1

siddharthsharma@siddharths-MacBook-Pro haven-infra-assessment % python scripts/cost_tag_check.py fixtures/plan.json > /tmp/haven-cost-2.txt

siddharthsharma@siddharths-MacBook-Pro haven-infra-assessment % rc2=$?

siddharthsharma@siddharths-MacBook-Pro haven-infra-assessment % cat /tmp/haven-cost-2.txt 

aws_lambda_function.mls_feed_sync: missing or empty landlord_account_id

aws_s3_bucket.listing_media: missing or empty landlord_account_id

siddharthsharma@siddharths-MacBook-Pro haven-infra-assessment % 

siddharthsharma@siddharths-MacBook-Pro haven-infra-assessment % printf 'first exit code: %s\n' "$rc2"

first exit code: 1

siddharthsharma@siddharths-MacBook-Pro haven-infra-assessment % diff -u /tmp/haven-cost-1.txt /tmp/haven-cost-2.txt 

siddharthsharma@siddharths-MacBook-Pro haven-infra-assessment % printf 'output comapre exit  code: %s\n' "$?"  

output comapre exit  code: 0

siddharthsharma@siddharths-MacBook-Pro haven-infra-assessment % test "$rc1" -eq "$rc1"

siddharthsharma@siddharths-MacBook-Pro haven-infra-assessment % printf 'exit  code comparison: %s\n' "$?"  

exit  code comparison: 0

siddharthsharma@siddharths-MacBook-Pro haven-infra-assessment % 






````


## Manual comparison — user's actual correction

The following later record compares rc1 to rc2 and explicitly reports comparison exit code 0. It supplements the original record; it does not replace or sanitize it.

````text
yeah please mark all the gaps and i corrected that type also&#x20;
siddharthsharma@siddharths-MacBook-Pro haven-infra-assessment % test "$rc1" -eq "$rc2"

siddharthsharma@siddharths-MacBook-Pro haven-infra-assessment % printf 'exit  code comparison: %s\n' "$?" 

exit  code comparison: 0

siddharthsharma@siddharths-MacBook-Pro haven-infra-assessment % 

````


## Interpretation

The manual checker return code 1 is expected for the supplied noncompliant fixture. It is not a test-suite failure. Both outputs list aws_lambda_function.mls_feed_sync and aws_s3_bucket.listing_media, once each and in sorted order. The recorded output comparison and corrected return-code comparison both succeed.
