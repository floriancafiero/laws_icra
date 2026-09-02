figures:
	python src/icra_evaluation.py

check:
	python -m unittest tests/test_pilot_logic.py
	python pilot/validate.py
