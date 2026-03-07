.PHONY: run_infra migrate makemigrations createsuperuser run

run_infra:
	docker compose up -d

##@ Example app

migrate:
	cd example_app && uv run python manage.py migrate

makemigrations:
	cd example_app && uv run python manage.py makemigrations

createsuperuser:
	cd example_app && DJANGO_SUPERUSER_PASSWORD=admin uv run python manage.py createsuperuser --username admin --email admin@example.com --noinput

run:
	cd example_app && uv run granian --interface wsgi example_app.wsgi:application --blocking-threads 2 --reload
