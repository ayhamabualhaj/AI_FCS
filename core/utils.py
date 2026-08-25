import json
import re


def parse_json_output(raw_string: str) -> dict:
    """
    Strips markdown fences (e.g., ```json ... ```) from the LLM output
    and parses it into a Python dictionary.
    """
    # Strip leading markdown fences (e.g., ```json or ```)
    clean_text = re.sub(r"^```(?:json)?\n?", "", raw_string.strip(), flags=re.IGNORECASE)

    # Strip trailing markdown fences
    clean_text = re.sub(r"\n?```$", "", clean_text.strip())

    try:
        return json.loads(clean_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON from AI output. Error: {e}\nRaw output: {raw_string}")