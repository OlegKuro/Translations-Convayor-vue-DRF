# Translations-Convayor-vue-DRF

- set up your `.env` file
- run `docker-compose up -d` from docker dir
- run `./bin/django-admin migrate` (you ought to make this file executable if it is not)
- create your superuser (`./bin/django-admin createsuperuser`)

---
- Frontend at localhost
- Backend is available at http://localhost/api/*
- HAProxy stats page at http://localhost:10001/stats