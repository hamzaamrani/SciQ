web: gunicorn web.run_prod:app
migrate: python web.run_prod db migrate
upgrade: python web.run_prod db upgrade