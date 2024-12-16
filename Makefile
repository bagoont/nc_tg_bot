project_dir := .

.PHONY: lint
lint:
	ruff check $(project_dir)
	mypy $(project_dir) --strict

.PHONY: format
format:
	ruff check $(project_dir) --fix

.PHONY: migrate
migrate:
	alembic upgrade head

.PHONY: bot-build
bot-build:
	docker-compose -f docker-compose.build.yaml build

.PHONY: bot-run
bot-run:
	docker-compose stop
	docker-compose -f docker-compose.build.yaml up -d --remove-orphans

.PHONY: bot-run-db
bot-run-db:
	docker compose stop
	docker compose -f docker-compose.build.yaml up -d redis db --remove-orphans

.PHONY: bot-stop
bot-stop:
	docker-compose -f docker-compose.build.yaml stop

.PHONY: bot-down
bot-down:
	docker-compose -f docker-compose.build.yaml down

.PHONY: bot-destroy
bot-destroy:
	docker-compose -f docker-compose.build.yaml down -v --remove-orphans

.PHONY: bot-logs
bot-logs:
	docker-compose -f docker-compose.build.yaml logs -f bot
