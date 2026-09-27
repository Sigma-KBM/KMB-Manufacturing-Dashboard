# Semantic Model and Report Boundaries

## Intended star schema

```text
Dim_Date ───────────┬─ Fact_Production ───── Fact_QualityInspection
Dim_Product ────────┼─ Fact_Production ───── Fact_MRB
Dim_WorkCenter ─────┼─ Fact_Production ───── Fact_Labor
Dim_Defect ─────────┼─ Fact_QualityInspection / Fact_MRB
Dim_Supplier ───────└─ Fact_MRB
Dim_Employee ───────┬─ Fact_Labor
                    └─ Fact_Training
Fact_MRB ───────────── Fact_CorrectiveAction
Dim_Date ───────────── Fact_KpiTargets
_Measures ──────────── dedicated measure table
```

## Relationship rules

- Dimensions filter facts one-to-many and in a single direction.
- Technical keys are hidden from report authors.
- `Fact_CorrectiveAction` relates to MRB by a one-to-many case/action relationship; date-role measures must use explicit inactive-date logic or dedicated date dimensions when required.
- `Fact_KpiTargets` has explicit target grain: KPI + period start + scope type + scope key. It is never a substitute for transaction facts.
- No many-to-many relationship is authorized without a documented, reviewed business grain.

## Report boundaries

Each report owns only its pages, navigation, bookmarks, alt text, tab order, and report-specific visual configuration. The semantic model owns tables, relationships, measures, formats, display folders, and governed KPI logic.

The shared-model PBIP reference is a proof-of-concept item. It must be created and tested from Power BI Desktop before it is treated as portable.
