# Power BI project

This folder contains the complete Power BI Project (`PBIP`) used by the portfolio dashboard.

## Contents

- `KMB_SemanticModel.pbip` — project entry point.
- `KMB_SemanticModel.Report` — four-page Power BI report definition.
- `KMB_SemanticModel.SemanticModel` — shared tabular model, Power Query expressions, relationships, and DAX measures.

## Open locally

From the repository root, configure the synthetic workbook path before opening the project:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\set_local_source.ps1
```

Then open `KMB_SemanticModel.pbip`, refresh the model, and verify all four pages. Restore the portable source placeholder before committing local changes:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\set_local_source.ps1 -Reset
```

The distributed project contains no Power BI Desktop cache or local-settings folders.
