run:
	docker-compose up

run-build:
	docker-compose up --build

migrate:
	docker exec -it backend-web-1 aerich migrate

upgrade:
	docker exec -it backend-web-1 aerich upgrade

init:
	docker exec -it backend-web-1 aerich init -t app.config.TORTOISE_ORM

init-db:
	docker exec -it backend-web-1 aerich init-db

initall: init init-db

runall: migrate upgrade

format:
	black . -l 79

lint: 
	flake8 .

check: format lint
