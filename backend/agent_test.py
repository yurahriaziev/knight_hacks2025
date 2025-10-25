from agents.parser_agent import parse_problem
from agents.scene_agent import generate_scene
from utils.logger import log

test_cases = [
    "A 5 kg sphere rolls down a 30° incline without friction.",
]

for i, problem in enumerate(test_cases, start=1):
    log("IntegrationTest", f"================= TEST {i} =================", "info")
    log("IntegrationTest", f"Problem: {problem}", "info")

    # Step 1 — parse the word problem
    parsed = parse_problem(problem)
    log("IntegrationTest", f"ParsedSpec: {parsed}", "success")

    # Step 2 — generate a scene from parsed data
    scene_json = generate_scene(parsed)
    log("IntegrationTest", f"SceneJSON: {scene_json}", "success")

    print("\n" + "=" * 80 + "\n")
