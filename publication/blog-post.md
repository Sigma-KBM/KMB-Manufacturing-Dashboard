# Building a Manufacturing Quality and Operations Dashboard in Power BI

## Introduction

KMB Manufacturing — Quality & Operations Analytics is a Power BI portfolio project built around a fictional manufacturer of industrial water-filtration modules. The project demonstrates how a shared semantic model can support executive, operational, tactical, and analytical decisions without duplicating business logic.

All companies, products, employees, suppliers, records, targets, and results in the project are synthetic. The ISO 9001:2015 reference establishes the fictional quality-management context; it is not an official certification claim.

## The reporting challenge

Manufacturing teams often need the same operational history presented at very different levels. Senior leaders need a concise view of enterprise performance. Line managers need actionable exceptions. Department heads need target recovery and corrective-action tracking. Analysts need enough detail to explore defects, process variation, and concentration.

The project addresses that challenge with four report pages connected to one governed semantic model:

1. **Leadership Quality & Operations** summarizes the most important quality, production, cost, and equipment indicators.
2. **Line Operations Control** focuses on line-level execution, containment, and daily operating exceptions.
3. **Tactical Performance Management** compares selected KPIs with governed targets over a rolling weekly horizon and connects performance gaps with open corrective actions.
4. **Advanced Quality Analytics** supports investigation through defect trends, Pareto concentration, process-and-line heatmaps, and detailed evidence tables.

## Data model and governance

The semantic model follows a star-schema approach. Shared dimensions for date, product, work center, employee, defect, and supplier filter production, inspection, MRB, corrective-action, training, and labor facts.

Targets are not repeated inside individual measures. `Fact_KpiTargets` stores the governed KPI name, reporting period, scope, target, direction, and tolerance. This makes status calculations consistent and allows the dashboard to distinguish KPIs where higher values are better from KPIs where lower values are better.

## Design decisions

The report uses navy and teal for normal information, with green, amber, and red reserved for status. Symbols and text accompany status colors so the dashboard does not rely on color alone. Monthly executive reporting uses closed months, while weekly analytical views exclude incomplete boundary weeks.

The project also distinguishes zero from missing information. Where a process-and-line combination is not configured or has no applicable value, the heatmap shows `N/A` instead of implying a measured zero.

## Reproducibility and portability

The repository includes a deterministic synthetic-data generator, an Excel source workbook, validation scripts, data contracts, a KPI catalog, and setup instructions. The distributed PBIP does not contain a personal path or a cloud dependency. A short PowerShell script configures the workbook path after the repository is cloned.

## What the project demonstrates

- Power BI Project, PBIR, and TMDL source control
- Star-schema modeling and reusable DAX measures
- Governed targets and direction-aware KPI status
- Power Query source portability
- Weekly and monthly time intelligence
- Executive, operational, tactical, and analytical page design
- Synthetic-data generation and automated data-quality controls
- Accessibility and publication hygiene for a public portfolio repository

## Explore the project

The complete project, source code, documentation, and reproduction steps are available here:

**GitHub repository:** https://github.com/Sigma-KBM/KMB-Manufacturing-Dashboard

Suggested publication images are available in `assets/screenshots/`: one tactical-management view and one advanced-analytics view.
