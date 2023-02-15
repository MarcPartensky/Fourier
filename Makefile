run:
	poetry run python .
publish: update
	poetry
	poetry --build publish
update:
	poetry update
	poetry export -f requirements.txt --output requirements.txt
docker:
	docker compose build
	docker compose push
