# KPI Catalog

`Fact_KpiTargets` is the one authority for targets, direction, and status tolerances. DAX measures must retrieve governed values from that table and must not recreate a conflicting fixed target.

| Display name | Technical name | Definition | Direction | Synthetic target | Time scope | Owner |
|---|---|---|---|---:|---|---|
| On-Time Production % | `KPI OnTimeProductionPct` | Completed on/before planned production ÷ planned production | Higher | 95% | Closed months | Operations Director |
| First Pass Yield % | `KPI FirstPassYieldPct` | Good quantity without rework ÷ produced quantity | Higher | 98% | Closed months / full weeks | Quality Director |
| Defects per 1K Units | `KPI DefectsPer1K` | Defect quantity ÷ inspected quantity × 1,000 | Lower | 12 | Full weeks | Quality Director |
| Scrap Rate % | `KPI ScrapRatePct` | Scrap quantity ÷ produced quantity | Lower | 1.5% | Closed months | Operations Director |
| Rework Rate % | `KPI ReworkRatePct` | Rework quantity ÷ produced quantity | Lower | 3.0% | Full weeks | Operations Director |
| MRB Open Cases | `KPI MRBOpenCases` | Count of MRB cases with open status | Lower | 15 | Current-state | Quality Director |
| MRB Aging >30 Days | `KPI MRBAged30Cases` | Open MRB cases aged over 30 days as of model data-through date | Lower | 0 | Current-state | Quality Director |
| Cost of Poor Quality % | `KPI COPQPct` | (Scrap cost + rework cost + MRB material cost) ÷ production value | Lower | 2.2% | Closed months | Finance & Quality |
| OEE Proxy % | `KPI OEEProxyPct` | Availability × performance × quality using controlled synthetic inputs | Higher | 85% | Full weeks | Operations Director |
| Training On-Time % | `KPI TrainingOnTimePct` | Training completed by due date ÷ completed training | Higher | 95% | Closed months | HR & Quality |
| Training Compliance % | `KPI TrainingCompliancePct` | Completed active requirements ÷ active requirements | Higher | 98% | Current-state | HR & Quality |
| Corrective Action On-Time % | `KPI CorrectiveActionOnTimePct` | Actions closed on/before due date ÷ closed actions | Higher | 90% | Closed months | Quality Director |
| Target Attainment % | `KPI TargetAttainmentPct` | Evaluated KPI-periods meeting target ÷ evaluated KPI-periods | Higher | 90% | Rolling 13 weeks / monthly | Department Heads |
| Defect Recurrence Rate % | `KPI DefectRecurrencePct` | Repeated defect events ÷ defect events | Lower | 20% | Full weeks | Quality Analytics |

## Status convention

Status is communicated as an English label plus icon and color:

- `On Target` / check icon / green
- `Watch` / warning icon / amber
- `Off Target` / alert icon / red

For lower-is-better KPIs, a lower value is favorable. For higher-is-better KPIs, a higher value is favorable. Yellow and red tolerance logic comes only from `Fact_KpiTargets`.

## Baseline policy

Baseline values are accepted only after source validation and reconciliation against documented control totals. The current source hash and control totals are recorded in [`validation.md`](validation.md); the reproducible checks are implemented in `scripts/validate_project.py`.
