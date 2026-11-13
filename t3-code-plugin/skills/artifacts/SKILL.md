---
name: artifacts
description: Pinning files as T3 project artifacts. Use when adding, renaming or describing an artifact with t3_project_artifacts_add or t3_project_artifacts_update, or tidying a project's Artifacts list.
---

# Project artifacts

The Artifacts panel shows each artifact as one line: its label. The path and description appear only on hover. A label is a name the owner scans at a glance.

## Labels

- **One word**, the noun that tells this file apart from its neighbours in the same section: `Manuscript`, `Deck`, `Notebook`, `Results`. Two words only when one would be ambiguous within the section: `Paper 1`, `Cost screen`.
- The section already carries the shared context, so leave it out of the label. In section `Paper 1`, label the PDF `Manuscript`, not `Paper 1 — manuscript`.
- The panel shows the file name on hover, so leave out extensions, dates and version numbers unless they are what tells two files apart.

## Descriptions

- Optional. Add one only when the label leaves a real question, such as which run, what it covers, or who it's for.
- **At most eight words**, a fragment with no full stop: `Submitted draft, 27 Oct`; `Supervisor meeting slides`.

## Done when

Every artifact you add or touch has a label of one word, or two at most, and any description is eight words or fewer. When the owner asks to tidy a list, also rename existing artifacts to this standard with `t3_project_artifacts_update`, and report the old and new labels.
