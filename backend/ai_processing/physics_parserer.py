from dotenv import load_dotenv
import os
import json
import re
from typing import Optional, Literal

import google.generativeai as genai

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

OBJECT_WORDS = {
    'spehere':['sphere', 'ball'],
    'box':['box', 'block', 'cube', 'crate']
}

def pre_extract(problem: str):
    text = problem.lower()

    angle = None
    m = re.search(r'(\d+(?:\.\d+)?)\s*(?:°|degrees?)', text)
    if m: angle = float(m.group(1))
    if angle is None:
        m  = re.search(r'angle\s*(?:of|=)?\s*(\d+(?:\.\d+)?)', text)
        if m: angle = float(m.group(1))

    mass = None
    m = re.search(r'(\d+(?:\.\d+)?)\s*kg\b', text)
    if m: mass = float(m.group(1))

    friction = None
    m = re.search(r'(?:μ|mu|coefficient of friction|friction coefficient|mu=|μ=)\s*(\d+(?:\.\d+)?)', text)
    if m: friction = float(m.group(1))
    if friction is None and ("no friction" in text or "frictionless" in text or "smooth" in text):
        friction = 0.0

    obj_type: Optional[Literal['sphere', 'box']] = None
    for t, words in OBJECT_WORDS.items():
        if any(w in text for w in words):
            obj_type = t
            break

    is_incline = any(w in text for w in ["incline", "ramp", "slope", "angle"]) or (angle is not None)

    return {
        'angle_deg': angle,
        "mass_kg": mass,
        "friction": friction,
        "object_type": obj_type,
        "is_incline": is_incline
    }

# for m in genai.list_models():
#     print(m.name)

def extract_simulation_data(problem: str):
    constraints = pre_extract(problem)

    system_rules = f"""
    You convert physics word problems into a JSON scene for a 3D simulation.
    You MUST honor the provided constraints EXACTLY when present:

    CONSTRAINTS (use these values verbatim if not null):
    {json.dumps(constraints)}

    Rules:
    - If constraints.angle_deg is not null -> environment.type = "incline" and environment.angle = that exact number.
    - If constraints.is_incline is true and angle_deg is null -> still use "incline" but omit angle.
    - If constraints.object_type is not null -> objects[0].type = that exact value.
    - If constraints.mass_kg is not null -> objects[0].mass = that exact value.
    - If constraints.friction is not null -> set BOTH environment.material.friction and objects[0].material.friction to that exact value.
    - Always use gravity -9.81 on Y.
    - Use meters, kilograms, seconds.
    - Return ONLY JSON (no markdown, no text).

    The JSON MUST have these keys: scene, environment, objects, simulation.
    """

    # Define a strict response schema the model must follow
    response_schema = {
        "type": "object",
        "properties": {
            "scene": {
                "type": "object",
                "properties": {
                    "gravity": {"type": "object","properties":{"x":{"type":"number"},"y":{"type":"number"},"z":{"type":"number"}},"required":["x","y","z"]},
                    "camera": {"type":"object","properties":{"position":{"type":"object","properties":{"x":{"type":"number"},"y":{"type":"number"},"z":{"type":"number"}},"required":["x","y","z"]},"lookAt":{"type":"object","properties":{"x":{"type":"number"},"y":{"type":"number"},"z":{"type":"number"}},"required":["x","y","z"]}},"required":["position","lookAt"]},
                    "lighting": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "type": {"type": "string"},
                                "intensity": {"type": "number"}
                            },
                            "required": ["type", "intensity"]
                        }
                    }
                },
                "required": ["gravity","camera","lighting"]
            },
            "environment": {
                "type":"object",
                "properties":{
                    "type":{"type":"string"},
                    "angle":{"type":"number"},
                    "dimensions":{"type":"object","properties":{"width":{"type":"number"},"depth":{"type":"number"},"height":{"type":"number"}}},
                    "material":{"type":"object","properties":{"color":{"type":"string"},"friction":{"type":"number"},"restitution":{"type":"number"}}}
                },
                "required":["type"]
            },
            "objects": {
                "type":"array",
                "items":{
                    "type":"object",
                    "properties":{
                        "type":{"type":"string"},
                        "mass":{"type":"number"},
                        "size": {
                            "type": "object",
                            "properties": {
                                "width": {"type": "number"},
                                "height": {"type": "number"},
                                "depth": {"type": "number"},
                                "radius": {"type": "number"}
                            }
                        },
                        "position":{"type":"object","properties":{"x":{"type":"number"},"y":{"type":"number"},"z":{"type":"number"}},"required":["x","y","z"]},
                        "material":{"type":"object","properties":{"color":{"type":"string"},"friction":{"type":"number"},"restitution":{"type":"number"}}}
                    },
                    "required":["type","mass","position"]
                },
            },
            "simulation": {
                "type":"object",
                "properties":{"timestep":{"type":"number"},"duration":{"type":"number"},"solver":{"type":"string"},"notes":{"type":"string"}},
                "required":["timestep","duration","solver"]
            }
        },
        "required": ["scene","environment","objects","simulation"]
    }

    generation_config = {
        "response_mime_type": "application/json",
        "response_schema": response_schema
    }

    model = genai.GenerativeModel(model_name="models/gemini-2.5-flash", generation_config=generation_config)

    prompt = f"""{system_rules}

    Problem:
    \"\"\"{problem}\"\"\"
    """

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        data = json.loads(text)
    except Exception as e:
        return {"error": f"AI generation/parsing failed: {str(e)}"}
    
    env = data.get('environment', {})
    obj0 = (data.get('objects') or [{}])[0]

    if constraints.get('angle_deg') is not None:
        env["type"] = "incline"
        env["angle"] = constraints["angle_deg"]
    elif constraints.get("is_incline"):
        env["type"] = "incline"

    if constraints.get("object_type") is not None:
        obj0["type"] = constraints["object_type"]

    if constraints.get("mass_kg") is not None:
        obj0["mass"] = constraints["mass_kg"]

    if constraints.get("friction") is not None:
        f = constraints["friction"]
        env.setdefault("material", {})["friction"] = f
        obj0.setdefault("material", {})["friction"] = f

    if 'objects' in data and data['objects']:
        data['objects'][0] = obj0
    data['environment'] = env

    return data