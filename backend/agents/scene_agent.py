import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from typing import Dict, Any

from utils.logger import log
from utils.validators import validate_scene_json
from utils.schema import SceneJSONSchema

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

if not GOOGLE_API_KEY:
    raise EnvironmentError("Missing GOOGLE_API_KEY in .env file")

genai.configure(api_key=GOOGLE_API_KEY)

def generate_scene(parsed: dict) -> dict:
    """
    Generate a complete simulation scene JSON from parsed data.

    Args:
        parsed (dict): ParsedSpec produced by Parser Agent.

    Returns:
        dict: SceneJSON containing scene, environment, objects, and simulation keys.
    """
    log("SceneAgent", "Starting scene generation...", "info")

    try:
        prompt = f"""
        You are a Physics Simulation Scene Generator.

        Your job is to take structured physics data (ParsedSpec) and generate
        a complete 3D physics simulation configuration (SceneJSON) that can
        be rendered in Three.js + Cannon.js.

        ---

        🎯 INPUT FORMAT (ParsedSpec):
        {{
        "environment_type": "string (incline | plane | pulley | unknown)",
        "angle_deg": "float or null",
        "friction": "float or null",
        "objects": [{{ "type": "string", "mass_kg": "float or null" }}],
        "extra_terms": {{"key": "value"}},
        "source_text": "original problem text"
        }}

        ---

        🎨 OUTPUT FORMAT (SceneJSON):
        {{
        "scene": {{
            "gravity": {{"x": 0, "y": -9.81, "z": 0}},
            "camera": {{
            "position": {{"x": 5, "y": 5, "z": 10}},
            "lookAt": {{"x": 0, "y": 0, "z": 0}}
            }},
            "lighting": [
            {{"type": "ambient", "intensity": 0.5}},
            {{"type": "directional", "direction": {{"x": 0.5, "y": -1, "z": 0.5}}, "intensity": 0.8}}
            ]
        }},
        "environment": {{
            "type": "string (from environment_type)",
            "angle": "float (use angle_deg if available)",
            "material": {{"friction": "float (use friction if available)", "restitution": 0.2}}
        }},
        "objects": [
            {{
            "type": "string",
            "mass": "float",
            "size": {{"width": 1, "height": 1, "depth": 1}},
            "position": {{"x": 0, "y": 2, "z": 0}},
            "material": {{"color": "#E2562C", "friction": "float", "restitution": 0.3}}
            }}
        ],
        "simulation": {{
            "timestep": 0.016,
            "duration": 5.0,
            "solver": "Cannon"
        }}
        }}

        ---

        🧠 RULES:
        1. Use ParsedSpec values to guide physics setup.
        2. If environment_type = "incline", include "angle".
        3. If friction is missing, assume 0.3.
        4. If mass is missing, assume 1.
        5. Return only valid JSON, no markdown or text.
        6. Maintain physical realism — gravity must act downward (y = -9.81).
        7. Ensure each object rests correctly on its environment (e.g., above incline).
        8. Use lowercase for keywords.

        ---

        Here is the ParsedSpec input:
        \"\"\"{parsed}\"\"\"

        Return only the SceneJSON.
        """

        log("SceneAgent", "Sending prompt to Gemini model...", "info")
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)

        raw_output = response.text.strip()
        cleaned = raw_output.replace("```json", "").replace("```", "").strip()

        try:
            scene_json = json.loads(cleaned)
        except json.JSONDecodeError as e:
            log("SceneAgent", f"JSON parsing failed: {e}", "error")
            return {
                "error": "Invalid JSON from Gemini",
                "raw_output": raw_output,
                "parsed_spec": parsed,
            }
        
        is_valid, errors = validate_scene_json(scene_json)
        if not is_valid:
            log("SceneAgent", f"Validation failed: {errors}", "error")
            scene_json = {
                "scene": scene_json.get("scene", {
                    "gravity": {"x": 0, "y": -9.81, "z": 0},
                    "camera": {"position": {"x": 5, "y": 5, "z": 10}, "lookAt": {"x": 0, "y": 0, "z": 0}},
                    "lighting": [{"type": "ambient", "intensity": 0.5}],
                }),
                "environment": scene_json.get("environment", {
                    "type": parsed.get("environment_type", "unknown"),
                    "angle": parsed.get("angle_deg", 0),
                    "material": {"friction": parsed.get("friction", 0.3), "restitution": 0.2},
                }),
                "objects": scene_json.get("objects", parsed.get("objects", [])),
                "simulation": scene_json.get("simulation", {"timestep": 0.016, "duration": 5, "solver": "Cannon"}),
            }
        
        required_fields = ["scene", "environment", "objects", "simulation"]
        for field in required_fields:
            if field not in scene_json:
                scene_json[field] = {} if field != "objects" else []

        log("SceneAgent", "Scene JSON parsed successfully.", "success")
        return scene_json
    except Exception as e:
        log("SceneAgent", f"Error generating scene: {e}", "error")
        return {"error": str(e), "parsed_spec": parsed}


__all__ = ["generate_scene"]