from agents.parser_agent import parse_problem

test_cases = [
    "A 5 kg box slides down a 30 degree incline with friction coefficient 0.2.",
    "A 2 kg sphere rolls down a 45° ramp with no friction.",
    "A block of unknown mass rests on a horizontal plane.",
    "Two pulleys connected by a rope lift a 10 kg weight.",
]

for i, case in enumerate(test_cases, 1):
    print(f"\n================= TEST {i} =================")
    result = parse_problem(case)
    print(result)