"""OCR utilities using Google Vision API.
In this prototype we stub out the API call as the environment lacks network access.
"""
from typing import Optional

# In a real implementation, you would import from google.cloud import vision


def extract_text_from_file(path: str) -> Optional[str]:
    """Extract text from an image or PDF using OCR.

    Parameters
    ----------
    path : str
        Path to the file.

    Returns
    -------
    Optional[str]
        The extracted text or None if extraction failed.
    """
    try:
        # Placeholder: In production, call Google Vision API here
        with open(path, 'rb') as f:
            _ = f.read(10)
        return "Stubbed OCR text from {}".format(path)
    except Exception as exc:
        print(f"OCR failed: {exc}")
        return None
