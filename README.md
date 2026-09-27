# KMB Manufacturing — Quality & Operations Analytics

![KMB Manufacturing](assets/kmb-manufacturing-logo.png)

A four-page Power BI portfolio project that demonstrates executive, operational, tactical, and analytical reporting for a fictional manufacturing company operating within an ISO 9001:2015 quality-management scenario.

> KMB Manufacturing, its products, employees, suppliers, identifiers, targets, and transactions are entirely fictional. The ISO reference is part of the demonstration scenario and is not an official certification mark.

## Dashboard pages

| Page | Audience | Decision supported |
|---|---|---|
| Leadership Quality & Operations | Directors and senior leaders | Identify enterprise priorities, quality risk, and operational performance gaps |
| Line Operations Control | Line managers and supervisors | Monitor production execution, containment needs, and line-level exceptions |
| Tactical Performance Management | Department heads | Manage weekly recovery against governed KPI targets and corrective-action commitments |
| Advanced Quality Analytics | Analysts and quality specialists | Investigate defect trends, concentration, process variation, and potential drivers |

## Portfolio highlights

- Shared star-schema semantic model across four audience-specific report pages.
- Governed KPI targets, tolerances, direction, and status logic sourced from `Fact_KpiTargets`.
- Dynamic monthly and weekly reporting periods with closed-period controls.
- KPI-aware DAX formatting for percentages, counts, rates, and target variance.
- Pareto, trend, heatmap, scorecard, queue, and detailed investigation views.
- Synthetic, reproducible source data with documented contracts and validation totals.
- Portable PBIP structure without SharePoint, OneDrive, corporate, or user-profile dependencies.
- Accessible color semantics supported by labels and symbols rather than color alone.

## Technology

- Power BI Project (`.pbip`)
- Power BI report definition (`PBIR`)
- Tabular Model Definition Language (`TMDL`)
- Power Query M
- DAX
- Python, pandas, and openpyxl for reproducible synthetic data and validation

## Repository structure

```text
assets/       Repository images
data/         Synthetic Excel source, manifest, and validation results
docs/         Scope, model, KPI, data-contract, design, and validation documentation
powerbi/      Power BI Project, report definition, and semantic model
publication/  Draft copy for the accompanying blog and LinkedIn posts
scripts/      Synthetic-data generation, validation, and local source configuration
theme/        Importable Power BI theme
```

## Open the project

### Prerequisites

- A recent version of Power BI Desktop with PBIP and TMDL support.
- Windows PowerShell.
- Python 3.10 or newer only if you want to regenerate or validate the synthetic workbook.

### Steps

1. Clone or download the repository to a short local path.
2. From the repository root, configure the local workbook path:

   ```powershell
   powershell -ExecutionPolicy Bypass -File .\scripts\set_local_source.ps1
   ```

3. Open `powerbi\KMB_SemanticModel.pbip` in Power BI Desktop.
4. Refresh the model and verify the four report pages.
5. Save, close, reopen, and refresh once more before evaluating the project.

The setup script changes only the local `pSourceFile` parameter. Before committing changes, restore the portable placeholder:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\set_local_source.ps1 -Reset
```

## Reproduce the synthetic data

Create an isolated Python environment and install the two required libraries:

```powershell
python -m pip install -r requirements.txt
python .\scripts\generate_synthetic_data.py
python .\scripts\validate_project.py
```

The generator uses a fixed seed. The validation script checks table structure, keys, relationships, required fields, business rules, privacy patterns, row counts, and control totals.

## Documentation

- [Project scope](docs/scope.md)
- [Semantic model](docs/model.md)
- [KPI catalog](docs/kpi_catalog.md)
- [Data dictionary](docs/data_dictionary.md)
- [Power Query and portability](docs/power_query.md)
- [Design and accessibility system](docs/design_system.md)
- [Validation summary](docs/validation.md)

## Publication and privacy

The included workbook contains synthetic demonstration data only. The repository contains no personal data, credentials, live connections, SharePoint or OneDrive routes, local user-profile paths, cache files, or Power BI Desktop local settings.

Power BI **Publish to web** is not required to evaluate this project and should only be used after a separate public-data and security review.

## License

This project is released under the [MIT License](LICENSE).
