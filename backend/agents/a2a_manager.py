
from agents.a2a_sim import AgentNode
from agents.parser_agent import parse_problem
from agents.scene_agent import generate_scene
from agents.validator_agent import validate_and_refine
from utils.logger import log


def run_a2a_simulation(problem_text: str) -> dict:
    """
    Simulate agent-to-agent (A2A) collaboration.
    Each agent communicates sequentially: Parser → Scene → Validator.
    """

    log("A2A Orchestrator", f"Starting A2A simulation for problem: {problem_text}", "info")

    parser = AgentNode(
        name='ParserAgent',
        role='Extracts structured parameters from text',
        handler=lambda text: parse_problem(text)
    )

    scene = AgentNode(
        name='SceneAgent',
        role='Generates a physics simulation scene',
        handler=lambda parsed: generate_scene(parsed)
    )

    validator = AgentNode(
        name='ValidatorAgent',
        role="Ensures physical realism and fixes missing values",
        handler=lambda scene: validate_and_refine(scene, parsed_result, problem_text)
    )

    log("A2A Orchestrator", "Sending problem to ParserAgent...", "info")
    parsed_result = parser.send(problem_text)

    log("A2A Orchestrator", "Forwarding parsed output to SceneAgent...", "info")
    scene_result = scene.send(parsed_result)

    log("A2A Orchestrator", "Passing generated scene to ValidatorAgent...", "info")
    validated_scene = validator.send(scene_result)

    # Step 3 — Final result
    log("A2A Orchestrator", "A2A simulation completed successfully.", "success")

    return {
        "problem": problem_text,
        "parsed": parsed_result,
        "scene": scene_result,
        "validated": validated_scene
    }

__all__ = ["run_a2a_simulation"]