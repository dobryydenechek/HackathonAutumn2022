# HackathonAutumn2022
## backend
### Create .env
echo > .env
```
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432

PGADMIN_DEFAULT_EMAIL=user@mail.com
PGADMIN_DEFAULT_PASSWORD=pgadmin

SECRET_KEY=secret_key
ALLOWED_HOSTS=*

```
### Run Backend
sudo apt install docker
sudo apt install docker-compose
cd app
sudo docker-compose up

### Remove Docker
sudo docker rm $(sudo docker ps -a) # Remove Containers
sudo docker rmi $(sudo docker image ls) # Remove Images
sudo docker volume $(sudo docker volume ls) # Remove Volumes
