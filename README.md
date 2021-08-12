![Build](https://github.com/Computer-Progress/api/workflows/Build/badge.svg)
![Style](https://github.com/Computer-Progress/api/workflows/Style/badge.svg)
![Tests](https://github.com/Computer-Progress/api/workflows/Tests/badge.svg)

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

And if you need to install new dependencies you can run:

```bash 
  docker-compose run --rm backend poetry add [depency_name]
```
## Documentation

After the docker is runnig, you can acess the routes documentation accessing:

    http://localhost:8000/docs
