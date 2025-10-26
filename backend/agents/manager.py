from agents.parser_agent import parse_problem
from agents.scene_agent import generate_scene
from agents.validator_agent import validate_and_refine
from utils.logger import log

import time

REFINEMENT_DELAY = 2

def scene_is_valid(scene: dict) -> bool:
    required = ["scene", "environment", "objects", "simulation"]
    return all(k in scene and scene[k] for k in required)

def run_autonomous_simulation(problem_text: str, max_refinements: int = 3) -> dict:
    """
    Run a full autonomous simulation loop with Parser → Scene → Validator.
    Retries up to `max_refinements` times if validation fails.
    """
    log("Manager", f"Starting autonomous loop for: {problem_text}", "info")

    parsed = parse_problem(problem_text)
    log("Manager", f"ParsedSpec: {parsed}", "success")

    current_scene = None
    final_scene = None

    history = []
    for round in range(1, max_refinements+1):
        log("Manager", f"--- Round {round} ---", "info")

        current_scene = generate_scene(parsed)
        log("Manager", "Scene generated. Passing to Validator...", "info")

        validated = validate_and_refine(current_scene, parsed, problem_text)

        history.append({
            'round':round,
            'scene':current_scene,
            'validated':validated
        })

        if scene_is_valid(validated):
            log("Manager", f"Validation successful at round {round}.", "success")
            final_scene = validated
            break
        else:
            log("Manager", f"Validation still failing — retrying (Round {round})", "warn")
            time.sleep(REFINEMENT_DELAY)

    if final_scene is None:
        log("Manager", "Max refinements reached. Returning last known scene.", "warn")
        final_scene = current_scene

    log("Manager", "Autonomous simulation completed.", "success")
    return {
        "final_scene": final_scene,
        "attempts": len(history),
        "history": history
    }

__all__ = ["run_autonomous_simulation"]