import json
import os
from typing import Any, Dict

import google.generativeai as genai
from dotenv import load_dotenv
from utils.logger import log
from utils.validators import validate_parsed_spec

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise EnvironmentError("Missing GOOGLE_API_KEY in .env file")

genai.configure(api_key=GOOGLE_API_KEY)


def parse_problem(text: str) -> Dict[str, Any]:
    """
    Parse a raw physics word problem into structured data.

    Args:
        text (str): Full word problem.

    Returns:
        dict: ParsedSpec with keys:
              environment_type, angle_deg, friction, objects, extra_terms, source_text
    """
    log("ParserAgent", "Starting problem parsing...", "info")

    try:
        prompt = f"""
        You are a Physics Problem Parser.
        Your job is to read a natural-language physics problem and extract all key details
        for building a 3D physics simulation.

        ---

        OUTPUT FORMAT (must always be valid JSON):
        {{
        "environment_type": "string (incline | plane | pulley | unknown)",
        "angle_deg": "float or null",
        "friction": "float or null",
        "objects": [
            {{
            "type": "string (e.g., box, sphere, ball)",
            "mass_kg": "float or null"
            }}
        ],
        "extra_terms": {{ "key": "value" }},
        "source_text": "original input text"
        }}

        ---

        RULES:
        1. Output only JSON, no explanations or markdown.
        2. All keywords and types should be lowercase.
        3. Use null if a value is not explicitly stated.
        4. Detect angles (in degrees) and friction coefficients.
        5. Detect object masses and assign them to "mass_kg".
        6. Recognize environment context (incline, plane, pulley, etc.).
        7. Use conservative defaults — do not assume values not mentioned.
        8. Include "source_text" identical to the given problem.
        9. Return nothing except the final JSON object.

        ---

        EXAMPLE:
        Problem:
        "A 5 kg box slides down a 30° incline with friction coefficient 0.2."

        Expected Output:
        {{
        "environment_type": "incline",
        "angle_deg": 30,
        "friction": 0.2,
        "objects": [
            {{ "type": "box", "mass_kg": 5 }}
        ],
        "extra_terms": {{}},
        "source_text": "A 5 kg box slides down a 30° incline with friction coefficient 0.2."
        }}

        ---

        Now, process the following problem carefully:

        Problem:
        \"\"\"{text}\"\"\"

        Return only the JSON.
        """

        log("ParserAgent", "Sending prompt to Gemini model...", "info")
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)

        raw_output = response.text.strip()
        cleaned = raw_output.replace("```json", "").replace("```", "").strip()

        try:
            parsed = json.loads(cleaned)
        except json.JSONDecodeError as e:
            log("ParserAgent", f"JSON parsing failed: {e}", "error")
            return {
                "error": "Invalid JSON from model",
                "raw_output": raw_output,
                "source_text": text,
            }

        is_valid, errors = validate_parsed_spec(parsed)
        if not is_valid:
            log("ParserAgent", f"Validation failed: {errors}", "error")
            parsed = {
                "environment_type": parsed.get("environment_type", "unknown"),
                "angle_deg": parsed.get("angle_deg"),
                "friction": parsed.get("friction"),
                "objects": parsed.get("objects", []),
                "extra_terms": parsed.get("extra_terms", {}),
                "source_text": text,
            }

        required_fields = [
            "environment_type",
            "angle_deg",
            "friction",
            "objects",
            "extra_terms",
            "source_text",
        ]
        for field in required_fields:
            if field not in parsed:
                parsed[field] = None if field != "objects" else []

        log("ParserAgent", "Parsing completed successfully.", "success")
        return parsed
    except Exception as e:
        log("ParserAgent", f"Error parsing problem: {e}", "error")
        return {"error": str(e), "source_text": text}


__all__ = ["parse_problem"]
