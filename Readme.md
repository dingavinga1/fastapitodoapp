# Todo App
A simple todo application written in Python, following the principles of clean architecture.

## Running the application
- Navigate into the source folder:
  ```
  cd app
  ```

- Set the global environment:
  ```
  export CLEAN_ENV=<env name>
  ```

  For production environment, use `PROD`. Similarly, for development environment, use `DEV`. 
  
  > Choose the environment name while keeping in mind the name of your dotenv file. e.g. If `CLEAN_ENV=PROD`, environment variables will be retreived directly from the environment. For all other environments, you can add a suffix to the environment file. e.g. If `CLEAN_ENV=DEV`, the dotenv filename should be `.env.dev`.

- Install requirements:
  ```
  pip install -r requirements.txt
  ```

- Run [Database Migrations](#database-migrations)

- Finally, run the FastAPI application
  ```
  uvicorn entry:app
  uvicorn entry:app --reload
  uvicorn entry:app --reload --port 8090
  ```

### Containerized setup
For a containerized setup, you can utilize `docker compose`.

> Before running docker compose, make the you have a dotenv file at the `root` of this project. Check out [.env.test](.env.test) as an example but make sure to name the actual file `.env`. 

```
docker compose up
```

This will expose your FastAPI application on port 8090 of your `localhost`.

## Database Migrations
```
cd app
```

Creating a migration:
```
alembic revision --autogenerate -m "<Commit Message>"
```

Creating sql file for a migration:
```
alembic upgrade <migration identifier> --sql
alembic upgrade head --sql
```

Downgrading:
```
alembic downgrade -1
alembic downgrade <migration identifier>
```

Executing a migration:
```
alembic upgrade head
```