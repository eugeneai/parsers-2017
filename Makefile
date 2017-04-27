.PHONY: run clean

run: clean
	python calc.py


clean:
	rm -f *.out
