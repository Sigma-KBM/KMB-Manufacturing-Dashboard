# Validation summary

Validation was completed on September 26, 2026 against the publication-ready repository copy.

## Result

The source workbook, Power BI project structure, semantic-model references, report resources, and publication files passed the automated and static checks described below. No DAX measures, Power Query transformations, relationships, visual layouts, or report interactions were changed during publication cleanup.

## Data checks

- The synthetic workbook passed `scripts/validate_project.py` with no errors.
- All 13 required tables, required columns, primary keys, foreign keys, and documented business rules passed.
- The workbook contains 47 package entries, no macros, no external workbook links, no connection definitions, no hidden sheets, no formulas, and no custom XML.
- Workbook metadata identifies the creator as `KMB BI Portfolio` and contains no personal author or last-modified-by value.
- Canonical workbook SHA-256: `c171e240b3e09602aa939aae65ecaa7bab25bffa5c186976dae5866ba0032600`.

### Control totals

| Control | Result |
|---|---:|
| Produced units | 486,740 |
| Good units | 472,232 |
| Scrap units | 5,655 |
| Rework units | 8,853 |
| Inspected units | 486,740 |
| Recorded defects | 10,416 |
| Defects per 1,000 units | 21.4 |
| First-pass yield | 97.0194% |
| Scrap rate | 1.1618% |
| Rework rate | 1.8188% |
| MRB cases | 717 |
| Open MRB cases | 96 |
| Training records | 909 |

## Power BI project checks

- 327 JSON definition files parsed successfully with no errors.
- The TMDL semantic model deserialized successfully.
- The model contains 13 tables, 147 measures, and 18 active relationships.
- No invalid many-to-one relationship direction was detected.
- All 635 report field references resolve to model objects.
- All three registered resources and all eight image references resolve to files in the project.
- Four report pages are present with unique names.
- The Process & Line Quality Heatmap is bound to dynamic background and font-color measures; blank cells render with the documented neutral treatment.
- KPI status icon color logic is present across the report. Thirteen icon-bearing visuals use the governed status-color measure, while the remaining scorecard uses explicit rules.
- The only functional-definition edits made for publication were the portable source placeholder and the removal of an external-tool name from one embedded calendar asset and its four references. The calendar image binary is unchanged.

### Open visual finding

Two scorecard rule sets compare the Off Target symbol with the ASCII character `x`, while their DAX measures emit the multiplication symbol `×`. The icon value and status label remain correct, but the Off Target icon can retain the default font color instead of red. This was documented rather than changed because the publication cleanup was required not to alter dashboard behavior. Confirm the rendered result in Power BI Desktop before publishing screenshots.

## Repository hygiene checks

- No credentials, tokens, personal-data paths, local Power BI cache, or local Power BI settings are included.
- No internal working notes, handoff records, or temporary repair scripts remain.
- Duplicate source data, obsolete audit notes, temporary development scripts, and redundant files were removed.
- Public Markdown links and relative repository paths were checked.

## Final desktop smoke test

Static validation cannot reproduce Power BI Desktop rendering or every interactive state. Before publishing screenshots or a live report, perform this short check on a clean clone:

1. Run `scripts\set_local_source.ps1`.
2. Open `powerbi\KMB_SemanticModel.pbip` in a current Power BI Desktop release.
3. Refresh with no errors.
4. Visit all four pages and exercise representative reporting-period, line, KPI, product-family, and defect-category selections.
5. Confirm tooltips, dynamic colors, axes, queues, and cross-filtering behave as documented.
6. Save, close, reopen, and refresh once more.
7. Run `scripts\set_local_source.ps1 -Reset` before committing.

The repository deliberately does not include a license. The owner should choose and add one before granting reuse rights.
