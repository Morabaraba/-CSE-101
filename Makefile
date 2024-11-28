.PHONY: pewpew-run pew-pygame-install pew-pygame-%

PYTHON3=python

pewpew-run:
	./pewpew-games/format-f-cp-py.bat

pew-pygame-install:
	git clone https://github.com/pewpew-game/pew-pygame.git && \
	cd pew-pygame && \
	$(PYTHON3) -m pip install -r ./pew-pygame/requirements.txt

pew-pygame-%:
	@set PYTHONPATH=./pew-pygame && $(PYTHON3) ./pew-pygame/autoloader.py ./pewpew-games/$*.py
