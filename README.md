[![Build](https://github.com/Computer-Progress/api/workflows/Build/badge.svg)](https://github.com/Computer-Progress/api/actions/workflows/build.yml)
[![Style](https://github.com/Computer-Progress/api/workflows/Style/badge.svg)](https://github.com/Computer-Progress/api/actions/workflows/style.yml)
[![Tests](https://github.com/Computer-Progress/api/workflows/Tests/badge.svg)](https://github.com/Computer-Progress/api/actions/workflows/test.yml)

# API Computer Progress

## Commands 

To execute the project just run this:

```bash 
  docker-compose up
```
    
To generate alembic new migrations files:

```bash 
  docker-compose run --rm backend alembic revision --autogenerate
```

To run the migrations:

```bash 
  docker-compose run --rm backend alembic upgrade head
```

To execute the tests:

```
  sudo docker-compose build --build-arg INSTALL_DEV=true && \
  sudo docker-compose run --rm backend pytest
```

To run code style verification:

```
  sudo docker-compose build --build-arg INSTALL_DEV=true && \
  sudo docker-compose run --rm backend flake8
```

And if you need to install new dependencies you can run:

```bash 
  docker-compose run --rm backend poetry add [depency_name]
```
## Documentation

After the docker is runnig, you can acess the routes documentation accessing:

    http://localhost:8000/docs
