docker-compose down -v
bash ./run.sh -z

curl http://localhost:5000/login -d "username=hamza&password=5f4dcc3b5aa765d61d8327deb882cf99" -X POST
