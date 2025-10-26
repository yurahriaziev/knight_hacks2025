from agents.parser_agent import parse_problem
from agents.scene_agent import generate_scene
from agents.validator_agent import validate_and_refine
from utils.logger import log

test_problems = [
    # "A 5 kg sphere rolls down a 30° incline without friction.",
    "A 2 kg box slides down a 45 degree ramp with friction coefficient 0.2.",
    # "A ball is dropped from a height of 10 meters.",
]

for i, problem in enumerate(test_problems, start=1):
    log("IntegrationTest", f"================= TEST {i} =================", "info")
    log("IntegrationTest", f"Problem: {problem}", "info")

    # Step 1 — Parser Agent
    parsed = parse_problem(problem)
    log("IntegrationTest", f"ParsedSpec: {parsed}", "success")

    # Step 2 — Scene Agent
    scene = generate_scene(parsed)
    log("IntegrationTest", f"SceneJSON (raw): {scene}", "info")

    # Step 3 — Validator Agent
    refined = validate_and_refine(scene, parsed, problem)
    log("IntegrationTest", f"Final SceneJSON (refined): {refined}", "success")

    print("\n" + "=" * 100 + "\n")
