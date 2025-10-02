up:
	docker compose -f docker-compose.dev.yml up --build -d

down:
	docker compose -f docker-compose.dev.yml down

test:
	docker compose -f docker-compose.dev.yml exec api python manage.py test

logs:
	docker compose -f docker-compose.dev.yml logs -f api

migrate:
	docker compose -f docker-compose.dev.yml exec api python manage.py migrate

shell:
	docker compose -f docker-compose.dev.yml exec api python manage.py shell

makemigrations_figures:
	docker compose -f docker-compose.dev.yml exec api python manage.py makemigrations figures

migrate_figures:
	docker compose -f docker-compose.dev.yml exec api python manage.py migrate figures

makemigrations_timeline:
	docker compose -f docker-compose.dev.yml exec api python manage.py makemigrations timeline

migrate_timeline:
	docker compose -f docker-compose.dev.yml exec api python manage.py migrate timeline

verify_indexes:
	docker compose -f docker-compose.dev.yml exec api python manage.py verify_indexes

precommit:
	docker compose -f docker-compose.dev.yml exec api pre-commit run --all-files

load_mvp_data:
	docker compose -f docker-compose.dev.yml exec api python manage.py load_mvp_data
