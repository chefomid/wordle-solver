"""Export utilities for PDF and Excel."""
from pathlib import Path
from typing import Iterable

import pandas as pd

from .models import CertificateOfInsurance


def export_to_excel(cois: Iterable[CertificateOfInsurance], path: Path):
    data = [
        {
            'ID': c.id,
            'Tenant': c.tenant,
            'Issue Date': c.issue_date,
            'Expiration Date': c.expiration_date,
            'Matched': c.matched,
            'Mismatches': '; '.join(c.mismatches)
        }
        for c in cois
    ]
    df = pd.DataFrame(data)
    df.to_excel(path, index=False)


def export_to_pdf(cois: Iterable[CertificateOfInsurance], path: Path):
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
    except ImportError:
        raise RuntimeError('reportlab is required for PDF export')

    c = canvas.Canvas(str(path), pagesize=letter)
    y = 750
    for coi in cois:
        c.drawString(50, y, f"COI {coi.id} for {coi.tenant} - Matched: {coi.matched}")
        y -= 20
        if y < 50:
            c.showPage()
            y = 750
    c.save()
