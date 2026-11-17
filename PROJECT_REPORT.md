# PV CasePro — Project Report

## Abstract

PV CasePro is a local educational application demonstrating fictional pharmacovigilance case intake, assessment, quality review, follow-up and reporting using a Python and SQLite stack.

## Introduction and objectives

The project gives an entry-level candidate a demonstrable environment for learning ICSR processing concepts, data completeness, audit history and quality review. It uses synthetic records only and makes no claim of operational regulatory suitability.

## Methodology and architecture

Streamlit renders the interface; service modules handle validation, case operations, narrative generation and exports; SQLAlchemy maps normalized records to SQLite. Workflow changes and case creation are recorded in an audit table. Startup adds missing schema objects and seeds demo cases only when no case records exist.

## Database design

Tables include cases, patients, reporters, products, events, assessments, follow_ups, reference_safety_information, qc_reviews, audit_logs and training_assessments. One-to-one case detail tables use case foreign keys; follow-ups, QC and audit histories use case references. Case IDs are indexed and unique.

## Modules

The application provides dashboard, intake, assessment, terminology practice, fictional reference safety information, follow-up, narrative generation, QC, workflow, exports, knowledge quiz and local backup/demo cleanup.

## Testing results

Automated tests cover database persistence, case creation and update, duplicate assistance, minimum criteria, unknown values, date checks, seriousness helper, follow-up edits, dashboard calculations, quiz scoring, SQLite migration preservation, backup integrity, demo-reset confirmation, narrative and CSV/XLSX output. Latest run: **23 passed** with `python -m pytest -v`; `python -m compileall .` completed successfully. A local browser connection attempt was refused in the execution environment, so browser rendering is not verified.

## Screenshots

Screenshots can be added after local browser review. No screenshots are committed yet.

## Conclusion and future enhancements

The project demonstrates a complete local training workflow. Future work could add schema-version migrations, role-based access, richer event/product relationships, accessibility review and additional export formats. Such work would not by itself establish validated-system compliance.
