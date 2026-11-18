"""
Write tests here proving:
  1. A PropertyManager scoped to la-001 (pm-001) is DENIED access to la-002's tenant's
     screening report (rep-002).
  2. The same PropertyManager (pm-001) IS allowed access to their own account's screening
     report (rep-001).

Use the `property_managers`, `properties`, `tenants`, and `screening_reports` fixtures from
conftest.py — don't re-invent the seed data here.
"""
from app.access_control import can_access_screening_report


def test_pm_001_cannot_access_rep_002(
    property_managers, properties, tenants, screening_reports
):
    actor = next(manager for manager in property_managers if manager.id == "pm-001")
    report = next(report for report in screening_reports if report.id == "rep-002")

    assert can_access_screening_report(
        actor, report, properties=properties, tenants=tenants
    ) is False


def test_pm_001_can_access_rep_001(
    property_managers, properties, tenants, screening_reports
):
    actor = next(manager for manager in property_managers if manager.id == "pm-001")
    report = next(report for report in screening_reports if report.id == "rep-001")

    assert can_access_screening_report(
        actor, report, properties=properties, tenants=tenants
    ) is True


def test_missing_report_tenant_denies_access(
    property_managers, properties, tenants, screening_reports
):
    actor = next(manager for manager in property_managers if manager.id == "pm-001")
    report = next(report for report in screening_reports if report.id == "rep-001")
    remaining_tenants = [tenant for tenant in tenants if tenant.id != report.tenant_id]

    assert can_access_screening_report(
        actor, report, properties=properties, tenants=remaining_tenants
    ) is False


def test_missing_tenant_property_denies_access(
    property_managers, properties, tenants, screening_reports
):
    actor = next(manager for manager in property_managers if manager.id == "pm-001")
    report = next(report for report in screening_reports if report.id == "rep-001")
    tenant = next(tenant for tenant in tenants if tenant.id == report.tenant_id)
    remaining_properties = [
        property_ for property_ in properties if property_.id != tenant.property_id
    ]

    assert can_access_screening_report(
        actor, report, properties=remaining_properties, tenants=tenants
    ) is False
