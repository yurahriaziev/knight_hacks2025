import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from typing import Dict, Any

from utils.logger import log
from utils.validators import validate_scene_json

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise EnvironmentError("Missing GOOGLE_API_KEY in .env file")

genai.configure(api_key=GOOGLE_API_KEY)

def validate_and_refine(scene: dict, parsed: dict, problem_text: str) -> dict:
    """
    Validate and, if necessary, refine a generated scene JSON.

    Args:
        scene (dict): SceneJSON from Scene Agent.
        parsed (dict): ParsedSpec from Parser Agent.
        problem_text (str): Original user prompt text.

    Returns:
        dict: Final validated SceneJSON ready for frontend rendering.
    """
    log("ValidatorAgent", "Starting scene validation and refinement...", "info")

    try:
        is_valid, errors = validate_scene_json(scene)
        if is_valid:
            log("ValidatorAgent", "Scene JSON passed base validation.", "success")
            return scene
        else:
            log("ValidatorAgent", f"Base validation failed: {errors}", "warn")

        log("ValidatorAgent", "Preparing to request AI-based refinement...", "info")

        prompt = f"""
You are a Physics Simulation Validator and Refiner.
Your task is to ensure a simulation JSON accurately represents
a given word problem and parsed specification.

---

INPUTS
1. Problem Text: the full physics word problem
2. ParsedSpec: structured description (environment, friction, mass, etc.)
3. SceneJSON: proposed simulation setup for Three.js + Cannon.js

---

YOUR JOB
- Verify that SceneJSON matches the ParsedSpec.
- Fix missing or incorrect fields.
- Ensure consistency with physical reality.

---

CHECKLIST
1. Does environment.type match ParsedSpec.environment_type?
2. If environment_type = "incline", ensure angle is present and numeric.
3. If friction is missing or unrealistic (<0 or >1), replace with 0.3.
4. If object mass or type is missing, use ParsedSpec.objects values.
5. Ensure each object has a valid position (above environment).
6. Add default camera, lighting, and gravity if missing.
7. Simulation block must include: timestep, duration, solver.
8. All numbers must be floats, not strings.
9. Return only valid JSON (no text, no comments).

---

Here are the inputs:

Problem Text:
\"\"\"{problem_text}\"\"\"

ParsedSpec:
\"\"\"{json.dumps(parsed, indent=2)}\"\"\"

SceneJSON:
\"\"\"{json.dumps(scene, indent=2)}\"\"\"

---

Return only the corrected SceneJSON.
        """

        log("ValidatorAgent", "Sending scene for AI-based refinement...", "info")

        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)

        raw_output = response.text.strip()
        cleaned = raw_output.replace("```json", "").replace("```", "").strip()
        
        try:
            refined = json.loads(cleaned)
            log("ValidatorAgent", "Refined SceneJSON parsed successfully.", "success")
        except json.JSONDecodeError as e:
            log("ValidatorAgent", f"JSON parsing failed: {e}", "error")
            refined = scene

        is_valid, errors = validate_scene_json(refined)
        if not is_valid:
            log("ValidatorAgent", f"Post-refinement validation failed: {errors}", "warn")
        else:
            log("ValidatorAgent", "SceneJSON validated successfully after refinement.", "success")

        return refined
    except Exception as e:
        log("ValidatorAgent", f"Error during validation: {e}", "error")
        return {"error": str(e), "scene_json": scene}
    
__all__ = ["validate_and_refine"]