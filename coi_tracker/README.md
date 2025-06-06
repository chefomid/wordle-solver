# COI Tracker Prototype

This folder contains a minimal prototype for a Certificate of Insurance (COI) tracker application. The goal is to showcase the core architecture for uploading certificates, configuring compliance rules, running OCR and LLM checks, and viewing results.

## Features

- **Upload & Preview**: Users can upload PDF or image-based COIs and see a preview in the left panel.
- **Rule Configuration**: Define required policy limits, description language, and additional insured entries.
- **OCR & LLM Stubs**: Text extraction and rule matching are stubbed to demonstrate how external services would be integrated.
- **Results**: Display pass/fail status along with mismatched rules.
- **SQLite Storage**: Uploaded certificates are stored in a local SQLite database.
- **Export Utilities**: Functions to export results to Excel or PDF using `pandas` and `reportlab`.

Run the app with:

```bash
python -m coi_tracker.main
```

This prototype focuses on structure and is not production ready. OCR and LLM functions need real API calls for full functionality.
