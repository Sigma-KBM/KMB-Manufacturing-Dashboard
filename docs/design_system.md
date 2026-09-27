# KMB Design and Accessibility System

## Visual language

- Canvas: 16:9; white or near-white background; consistent outer margin and 12-column grid.
- Typography: Segoe UI or Arial; minimum 12 pt body labels, 16 pt chart titles, 24 pt page titles.
- Normal data: navy `#1F4E78` and teal `#0F6B78`.
- Neutral comparison: slate `#5B6770`.
- Status only: green `#1B7F3A`, amber `#A65D00`, red `#B42318`.
- Never use red as an ordinary data-series color.

## Standard page anatomy

1. English page title and decision question.
2. `Data through` date and explicit scope note.
3. Visible global filters and Reset action.
4. KPI row: Actual, Target, Gap, Status text/icon.
5. Trend or comparator visual.
6. Driver, action, or detailed table.
7. Plain-language note for partial-week exclusions, current-state queues, or exploratory analysis.

## Accessibility requirements

- Alt text format: `Visual type + metric + dimension/period + filter behavior.`
- Example: `Weekly First Pass Yield trend against its governed target; responds to product family, line, shift, and full-week filters.`
- Every status displays English label plus an icon and color.
- Decorative shapes/images do not receive tab focus.
- Tab order: page navigation, filters, reset, KPI cards, trends, detailed analysis, supporting notes.
- Validate contrast and keyboard order after every visual move or addition.

## Report-specific page plan

| Report | Initial pages |
|---|---|
| Leadership | Executive Overview; Quality & COPQ; Operational Performance; Workforce Readiness; Improvement Priorities |
| Line Operations | Daily Production Control; Quality & Defect Pareto; MRB & Nonconformance Queue; Training Compliance; Shift & Work Center Detail |
| Tactical | Tactical Scorecard; Target Attainment; Action Plan Tracking; Department Drilldown; Capacity & Readiness |
| Advanced Analytics | Trend Explorer; Defect Pattern Analysis; Process & Shift Comparison; MRB Root-Cause Exploration; Training & Quality Association; Outlier Investigation |
