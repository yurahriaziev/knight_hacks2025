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
    pass

def validate_scene_json(scene: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate SceneJSON structure for required keys and numeric ranges.

    Args:
        scene (dict): SceneJSON output from Scene Agent.

    Returns:
        (bool, List[str]): (is_valid, list_of_errors)
    """
    pass

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