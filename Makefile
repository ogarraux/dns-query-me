SHELL=/bin/bash

run:
	./dns.py

setup:
	virtualenv venv; \
	source venv/bin/activate; \
	pip install -r requirements.txt; \

docker:
	docker build -t i$(name):$(version) .

setupfly:
	flyctl launch --dockerfile Dockerfile-fly

deployfly:
	sudo flyctl deploy --local-only
