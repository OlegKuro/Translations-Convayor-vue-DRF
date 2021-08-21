# Translations-Convayor-vue-DRF

- set up your `.env` file in `docker` directory (look at `.env.example`)
- run `docker-compose up -d` from docker dir
- run `./bin/django-admin migrate` (you ought to make this file executable if it is not)
- create your superuser (`./bin/django-admin createsuperuser`)

---
- Frontend at http://localhost
- Backend is available at http://localhost/api/*
- HAProxy stats page at http://localhost:10001/stats

---
Notes:
- Before running make sure your 80, 4000 and 10001 ports are not allocated
- Only admin can create new tasks in "All tasks" section
