## Database Migrations
Creating a migration:
```
alembic revision --autogenerate -m "<Commit Message>"
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