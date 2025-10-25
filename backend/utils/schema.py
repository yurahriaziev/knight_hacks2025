"""
data contracts shared amongst all agents
- ParsedSpecSchema: structure returned by Parser Agent
- SceneJSONSchema: structure produced and refined by Scene + Validator Agents
- Shared constants: valid categories, numeric bounds, etc.
"""

from typing import Dict, List, Optional, Union

ParsedSpecSchema: Dict[str, str] = {
    "environment_type": "str",
    "angle_deg": "float | None",
    "friction": "float | None",
    "objects": "list[dict]",
    "extra_terms": "dict | None",
    "source_text": "str",      
}

SceneJSONSchema: Dict[str, Union[str, Dict, Dict]] = {
     "scene": {
        "gravity": "dict",
        "camera": "dict",
        "lighting": "list",
    },
    "environment": {
        "type": "str",
        "angle": "float",
        "material": "dict",
    },
    "objects": "list[dict]",
    "simulation": {
        "timestep": "float",
        "duration": "float",
        "solver": "str",
    }
}

VALID_ENVIRONMENTS: List[str] = ["incline", "plane", "pulley", "unknown"]
VALID_OBJECT_TYPES: List[str] = ["box", "sphere", "ball", "block", "cart", "crate", "cube"]

NUMERIC_BOUNDS: Dict[str, tuple] = {
    "angle": (0, 90),
    "friction": (0.0, 1.0),
    "mass": (0.01, 1000.0),
}

__all__ = [
    "ParsedSpecSchema",
    "SceneJSONSchema",
    "VALID_ENVIRONMENTS",
    "VALID_OBJECT_TYPES",
    "NUMERIC_BOUNDS",
]