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
