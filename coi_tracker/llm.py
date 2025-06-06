"""LLM integration using OpenAI or Gemini.
This module provides a stub for semantic analysis of text.
"""
from typing import List

# In real code, integrate with openai or google generative language API

def analyze_compliance(text: str, rules: List[str]) -> List[str]:
    """Check if given text complies with rules.

    Parameters
    ----------
    text : str
        The text extracted from the COI.
    rules : List[str]
        A list of textual rules to match.

    Returns
    -------
    List[str]
        A list of rules that were not satisfied.
    """
    # Placeholder: This naive implementation simply checks rule substrings
    missing = [rule for rule in rules if rule.lower() not in text.lower()]
    return missing
