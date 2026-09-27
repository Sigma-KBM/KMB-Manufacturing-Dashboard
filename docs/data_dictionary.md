# Data Contracts

All fields, values, identifiers, and records are synthetic. Keys are integer surrogate keys unless identified otherwise. Source owner for every table is **KMB Synthetic Data Generator**.

## Dimensions

| Table | Grain and key | Required columns and types | Contract validations |
|---|---|---|---|
| `Dim_Date` | One calendar date; `DateKey` | `Date` date, `Year` int, `MonthNumber` int, `Month` text, `WeekStartDate` date, `IsCompleteWeek` boolean | Unique continuous dates; 2024-09-01 to 2026-08-31; valid calendar parts. |
| `Dim_Product` | One sellable SKU; `ProductKey` | `ProductCode` text, `ProductFamily` text, `ProductName` text, `StandardCycleMinutes` decimal, `StandardUnitValue` decimal | Unique product codes; family in Standard/High-Flow/Chemical-Resistant; positive numeric values. |
| `Dim_WorkCenter` | One controlled work center; `WorkCenterKey` | `WorkCenterCode` text, `Line` text, `Process` text, `Department` text | Unique codes; process is Cutting, Assembly, Leak Test, Final Inspection, or Packout. |
| `Dim_Employee` | One fictional employee; `EmployeeKey` | `EmployeeCode` text, `Role` text, `Department` text, `Shift` text, `HireDate` date, `IsActive` boolean | Unique codes; no real PII; valid department and shift. |
| `Dim_Defect` | One defect classification; `DefectKey` | `DefectCode` text, `DefectName` text, `Category` text, `Severity` text | Unique codes; severity in Critical/High/Medium/Low. |
| `Dim_Supplier` | One fictional supplier; `SupplierKey` | `SupplierCode` text, `SupplierName` text, `Commodity` text, `Status` text | Unique codes; all names fictional. |

## Facts

| Table | Grain and key | Required columns and types | Contract validations |
|---|---|---|---|
| `Fact_Production` | One product/work-center/shift/day production event; `ProductionEventKey` | `DateKey`, `ProductKey`, `WorkCenterKey`, `Shift`, `PlannedQty`, `ProducedQty`, `GoodQty`, `ScrapQty`, `ReworkQty` ints; `LaborHours`, `DowntimeMinutes`, `ProductionValue` decimals | Foreign keys resolve; quantities nonnegative; `GoodQty + ScrapQty + ReworkQty <= ProducedQty`; planned and produced positive. |
| `Fact_QualityInspection` | One production-event inspection; `InspectionKey` | `ProductionEventKey`, `DateKey`, `ProductKey`, `WorkCenterKey`, `DefectKey`, `InspectedQty`, `DefectQty` ints; `InspectionResult` text | Foreign keys resolve; `0 <= DefectQty <= InspectedQty`; result allowed. |
| `Fact_MRB` | One nonconforming-material case; `MRBCaseKey` | `DateKey`, `ProductKey`, `WorkCenterKey`, `SupplierKey`, `DefectKey` ints; `OpenDate` date, `CloseDate` nullable date, `Quantity`, `MaterialCost` decimal, `Disposition`, `Status` text | Foreign keys resolve; positive quantity/cost; closed case has close date not before open date; open case has no close date. |
| `Fact_CorrectiveAction` | One corrective action; `ActionKey` | `MRBCaseKey`, `OpenDate`, `DueDate`, `CompletionDate` nullable date, `OwnerDepartment`, `Status`, `EffectivenessVerified` boolean | MRB key resolves; due date >= open date; closed actions have completion date. |
| `Fact_Training` | One assigned employee/course requirement; `TrainingRecordKey` | `EmployeeKey`, `CourseName`, `AssignmentDate`, `DueDate`, `CompletionDate` nullable date, `Status`, `ScorePct` nullable decimal | Employee resolves; due >= assignment; completion >= assignment; score 0–100. |
| `Fact_Labor` | One employee/day labor record; `LaborRecordKey` | `DateKey`, `EmployeeKey`, `WorkCenterKey`, `RegularHours`, `OvertimeHours`, `AbsenceHours` decimals | Foreign keys resolve; hours nonnegative; total hours <= 24. |
| `Fact_KpiTargets` | One KPI, period, and scope target; `TargetKey` | `KPIName`, `PeriodStart`, `ScopeType`, `ScopeKey`, `TargetValue`, `Direction`, `YellowTolerancePct`, `RedTolerancePct` | Exactly one active row per KPI/period/scope; target positive; direction is HigherIsBetter or LowerIsBetter. |

## Null and deduplication policy

- Primary keys and required foreign keys cannot be null.
- `CloseDate`, `CompletionDate`, and `ScorePct` may be blank only when their status supports an incomplete/open record.
- A duplicate primary key fails validation. No automated deduplication is permitted; the generator must be fixed and data regenerated.
- Unknown categories and orphaned foreign keys fail validation.
