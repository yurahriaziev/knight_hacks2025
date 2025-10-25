"""
Shared validation functions used by the agents
- Check schema compliance for ParsedSpec and SceneJSON.
- Enforce numeric sanity (angle, friction, mass, etc.).
- Compare parsed and generated data for consistency.
- Clamp numeric values within safe ranges.
"""

from typing import Dict, Any, Tuple, List
from utils.schema import NUMERIC_BOUNDS, VALID_ENVIRONMENTS, VALID_OBJECT_TYPES

def validate_parsed_spec(parsed: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate the structure and basic sanity of a ParsedSpec dict.

    Args:
        parsed (dict): Output from Parser Agent.

    Returns:
        (bool, List[str]): (is_valid, list_of_errors)
    """
    required_fields = ["environment_type", "objects", "source_text"]
    errors = []

    for field in required_fields:
        if field not in parsed:
            errors.append(f"Missing required field: {field}")

    # type checks
    if "angle_deg" in parsed and parsed["angle_deg"] is not None:
        if not isinstance(parsed["angle_deg"], (int, float)):
            errors.append("angle_deg must be numeric")

    if "friction" in parsed and parsed["friction"] is not None:
        if not isinstance(parsed["friction"], (int, float)):
            errors.append("friction must be numeric")

    if "objects" in parsed and isinstance(parsed["objects"], list):
        for i, obj in enumerate(parsed["objects"]):
            if "type" not in obj:
                errors.append(f"Object {i} missing 'type'")
            if "mass_kg" in obj and not isinstance(obj["mass_kg"], (int, float, type(None))):
                errors.append(f"Object {i} mass_kg must be numeric")

    return (len(errors) == 0, errors)

def validate_scene_json(scene: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate SceneJSON structure for required keys and numeric ranges.

    Args:
        scene (dict): SceneJSON output from Scene Agent.

    Returns:
        (bool, List[str]): (is_valid, list_of_errors)
    """
    errors = []

    required_sections = ["scene", "environment", "objects", "simulation"]
    for section in required_sections:
        if section not in scene:
            errors.append(f"Missing top-level section: {section}")

    # Scene checks
    scene = scene.get("scene", {})
    if "gravity" not in scene:
        errors.append("Missing gravity in scene")
    if "camera" not in scene:
        errors.append("Missing camera in scene")

    # Environment checks
    env = scene.get("environment", {})
    if "type" not in env:
        errors.append("Missing environment type")
    if "material" not in env:
        errors.append("Missing environment material")

    # Objects list sanity check
    objs = scene.get("objects", [])
    if not isinstance(objs, list):
        errors.append("objects must be a list")
    elif len(objs) == 0:
        errors.append("objects list is empty")

    # Simulation block
    sim = scene.get("simulation", {})
    for key in ["timestep", "duration", "solver"]:
        if key not in sim:
            errors.append(f"Missing simulation parameter: {key}")

    return (len(errors) == 0, errors)

def compare_parsed_and_scene(parsed: Dict[str, Any], scene: Dict[str, Any]) -> Dict[str, str]:
    """
    Compare values from Parser Agent and Scene Agent outputs.

    Args:
        parsed (dict): ParsedSpec.
        scene (dict): SceneJSON.

    Returns:
        dict: { field_name: "mismatch description" } for any inconsistencies.
    """
    pass

def apply_numeric_bounds(value: float, key: str) -> float:
    """
    Clamp a numeric value to its allowed range defined in NUMERIC_BOUNDS.

    Args:
        value (float): The number to clamp.
        key (str): The numeric type key ('angle', 'friction', 'mass').

    Returns:
        float: Clamped numeric value.
    """
    pass

__all__ = [
    "validate_parsed_spec",
    "validate_scene_json",
    "compare_parsed_and_scene",
    "apply_numeric_bounds",
]