# Synthetic source data

`kmb_synthetic_operations.xlsx` is the repository's only report data source. It is generated reproducibly by `scripts/generate_synthetic_data.py`, validated by `scripts/validate_project.py`, and stored as Excel named tables rather than report logic.

Every fact row has `DataSource = Synthetic KMB Demonstration`. The workbook spans 2024-09-01 through 2026-08-31, a 24-month closed reporting period.

The synthetic data does not represent real personnel, suppliers, products, locations, throughput, costs, quality rates, capacity, or targets.

`kmb_synthetic_operations_manifest.json` records the generation seed, SHA-256 checksum, reporting period, and row counts. `validation_report.json` records the latest validation result and control totals.
