"""Validate KMB's synthetic workbook contracts and produce reproducible control totals."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

import pandas as pd
from openpyxl import load_workbook


ROOT = Path(__file__).resolve().parents[1]
WORKBOOK_PATH = ROOT / "data" / "kmb_synthetic_operations.xlsx"
REPORT_PATH = ROOT / "data" / "validation_report.json"
SOURCE_LABEL = "Synthetic KMB Demonstration"

PRIMARY_KEYS = {
    "Dim_Date": "DateKey", "Dim_Product": "ProductKey", "Dim_WorkCenter": "WorkCenterKey", "Dim_Employee": "EmployeeKey",
    "Dim_Defect": "DefectKey", "Dim_Supplier": "SupplierKey", "Fact_Production": "ProductionEventKey", "Fact_QualityInspection": "InspectionKey",
    "Fact_MRB": "MRBCaseKey", "Fact_CorrectiveAction": "ActionKey", "Fact_Training": "TrainingRecordKey", "Fact_Labor": "LaborRecordKey", "Fact_KpiTargets": "TargetKey",
}

FOREIGN_KEYS = [
    ("Fact_Production", "DateKey", "Dim_Date", "DateKey"), ("Fact_Production", "ProductKey", "Dim_Product", "ProductKey"), ("Fact_Production", "WorkCenterKey", "Dim_WorkCenter", "WorkCenterKey"),
    ("Fact_QualityInspection", "ProductionEventKey", "Fact_Production", "ProductionEventKey"), ("Fact_QualityInspection", "DateKey", "Dim_Date", "DateKey"), ("Fact_QualityInspection", "ProductKey", "Dim_Product", "ProductKey"), ("Fact_QualityInspection", "WorkCenterKey", "Dim_WorkCenter", "WorkCenterKey"), ("Fact_QualityInspection", "DefectKey", "Dim_Defect", "DefectKey"),
    ("Fact_MRB", "DateKey", "Dim_Date", "DateKey"), ("Fact_MRB", "ProductKey", "Dim_Product", "ProductKey"), ("Fact_MRB", "WorkCenterKey", "Dim_WorkCenter", "WorkCenterKey"), ("Fact_MRB", "SupplierKey", "Dim_Supplier", "SupplierKey"), ("Fact_MRB", "DefectKey", "Dim_Defect", "DefectKey"),
    ("Fact_CorrectiveAction", "MRBCaseKey", "Fact_MRB", "MRBCaseKey"), ("Fact_Training", "EmployeeKey", "Dim_Employee", "EmployeeKey"),
    ("Fact_Labor", "DateKey", "Dim_Date", "DateKey"), ("Fact_Labor", "EmployeeKey", "Dim_Employee", "EmployeeKey"), ("Fact_Labor", "WorkCenterKey", "Dim_WorkCenter", "WorkCenterKey"),
]


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def validate() -> dict:
    if not WORKBOOK_PATH.exists():
        raise FileNotFoundError(f"Missing generated source: {WORKBOOK_PATH}")
    workbook = load_workbook(WORKBOOK_PATH, read_only=False, data_only=False)
    expected = set(PRIMARY_KEYS)
    errors: list[str] = []
    if set(workbook.sheetnames) != expected:
        fail(errors, f"Workbook sheet set differs. Expected {sorted(expected)}, found {workbook.sheetnames}")
    for name in expected.intersection(workbook.sheetnames):
        if name not in workbook[name].tables:
            fail(errors, f"Missing named Excel table {name}")
    workbook.close()
    frames = pd.read_excel(WORKBOOK_PATH, sheet_name=None)
    for name, key in PRIMARY_KEYS.items():
        frame = frames[name]
        if key not in frame.columns:
            fail(errors, f"{name}: missing primary key {key}")
            continue
        if frame[key].isna().any():
            fail(errors, f"{name}: null primary key")
        duplicates = int(frame[key].duplicated().sum())
        if duplicates:
            fail(errors, f"{name}: {duplicates} duplicate primary keys")
    for fact, field, dimension, key in FOREIGN_KEYS:
        missing = set(frames[fact][field].dropna()) - set(frames[dimension][key].dropna())
        if missing:
            fail(errors, f"{fact}.{field}: {len(missing)} orphaned values against {dimension}.{key}")
    production = frames["Fact_Production"]
    if (production[["PlannedQty", "ProducedQty", "GoodQty", "ScrapQty", "ReworkQty"]] < 0).any().any():
        fail(errors, "Fact_Production: negative quantity")
    if (production["GoodQty"] + production["ScrapQty"] + production["ReworkQty"] > production["ProducedQty"]).any():
        fail(errors, "Fact_Production: quality quantities exceed produced quantity")
    if production[["PlannedCompletionDateTime", "ActualCompletionDateTime"]].isna().any().any():
        fail(errors, "Fact_Production: planned or actual completion timestamp is null")
    products = frames["Dim_Product"]
    if "StandardUnitCost" not in products.columns or (products["StandardUnitCost"] <= 0).any() or (products["StandardUnitCost"] > products["StandardUnitValue"]).any():
        fail(errors, "Dim_Product: standard unit cost must be positive and no greater than standard unit value")
    inspection = frames["Fact_QualityInspection"]
    if (inspection["DefectQty"] > inspection["InspectedQty"]).any() or (inspection[["DefectQty", "InspectedQty"]] < 0).any().any():
        fail(errors, "Fact_QualityInspection: invalid inspection quantities")
    mrb = frames["Fact_MRB"]
    open_cases = mrb["Status"] == "Open"
    closed_cases = mrb["Status"] == "Closed"
    if mrb.loc[open_cases, "CloseDate"].notna().any() or mrb.loc[closed_cases, "CloseDate"].isna().any():
        fail(errors, "Fact_MRB: status and close-date policy violated")
    if (pd.to_datetime(mrb.loc[closed_cases, "CloseDate"]) < pd.to_datetime(mrb.loc[closed_cases, "OpenDate"])).any():
        fail(errors, "Fact_MRB: close date precedes open date")
    actions = frames["Fact_CorrectiveAction"]
    closed_actions = actions["Status"] == "Closed"
    if actions.loc[closed_actions, "CompletionDate"].isna().any() or actions.loc[~closed_actions, "CompletionDate"].notna().any():
        fail(errors, "Fact_CorrectiveAction: status and completion-date policy violated")
    if (pd.to_datetime(actions["DueDate"]) < pd.to_datetime(actions["OpenDate"])).any():
        fail(errors, "Fact_CorrectiveAction: due date precedes open date")
    training = frames["Fact_Training"]
    if (pd.to_datetime(training["DueDate"]) < pd.to_datetime(training["AssignmentDate"])).any():
        fail(errors, "Fact_Training: due date precedes assignment")
    completed_training = training["CompletionDate"].notna()
    if (pd.to_datetime(training.loc[completed_training, "CompletionDate"]) < pd.to_datetime(training.loc[completed_training, "AssignmentDate"])).any():
        fail(errors, "Fact_Training: completion precedes assignment")
    targets = frames["Fact_KpiTargets"]
    target_dupes = targets.duplicated(["KPIName", "PeriodStart", "ScopeType", "ScopeKey"], keep=False).sum()
    if target_dupes:
        fail(errors, f"Fact_KpiTargets: {target_dupes} duplicate governance-grain rows")
    if not set(targets["Direction"]).issubset({"HigherIsBetter", "LowerIsBetter"}):
        fail(errors, "Fact_KpiTargets: invalid direction")
    source_columns = [name for name in frames if name.startswith("Fact_")]
    for name in source_columns:
        if "DataSource" not in frames[name].columns or not (frames[name]["DataSource"] == SOURCE_LABEL).all():
            fail(errors, f"{name}: DataSource does not prove synthetic provenance")
    content = "\n".join("\n".join(frame.astype(str).fillna("").values.flatten()) for frame in frames.values())
    prohibited = [r"@", r"C:\\Users\\", r"Denodo", r"VIN", r"password", r"token"]
    hits = [pattern for pattern in prohibited if re.search(pattern, content, re.IGNORECASE)]
    if hits:
        fail(errors, f"Synthetic content contains prohibited pattern(s): {hits}")
    inspected = int(inspection["InspectedQty"].sum())
    total_defects = int(inspection["DefectQty"].sum())
    produced = int(production["ProducedQty"].sum())
    control_totals = {
        "produced_qty": produced,
        "good_qty": int(production["GoodQty"].sum()),
        "scrap_qty": int(production["ScrapQty"].sum()),
        "rework_qty": int(production["ReworkQty"].sum()),
        "inspected_qty": inspected,
        "defect_qty": total_defects,
        "defects_per_1000_units": round(total_defects / inspected * 1000, 3) if inspected else None,
        "first_pass_yield_pct": round(production["GoodQty"].sum() / produced, 6) if produced else None,
        "scrap_rate_pct": round(production["ScrapQty"].sum() / produced, 6) if produced else None,
        "rework_rate_pct": round(production["ReworkQty"].sum() / produced, 6) if produced else None,
        "mrb_cases": int(len(mrb)),
        "open_mrb_cases": int((mrb["Status"] == "Open").sum()),
        "training_records": int(len(training)),
    }
    result = {"workbook": WORKBOOK_PATH.name, "sha256": hashlib.sha256(WORKBOOK_PATH.read_bytes()).hexdigest(), "row_counts": {name: int(len(frame)) for name, frame in frames.items()}, "control_totals": control_totals, "errors": errors, "status": "passed" if not errors else "failed"}
    REPORT_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


if __name__ == "__main__":
    result = validate()
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["status"] == "passed" else 1)
