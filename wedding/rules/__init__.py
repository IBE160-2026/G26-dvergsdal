"""Pure rule functions: no Django, no database and no other project code (AD-2).

Rules take plain values, including an explicit `now`, and return plain values.
`tests/test_rules_purity.py` fails if anything here imports Django or the project.
"""
