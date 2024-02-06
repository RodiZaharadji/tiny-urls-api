
## Development setup
- Install required software
  - Docker ([MacOS](https://docs.docker.com/docker-for-mac/install/), [Linux](https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/))
  - Docker-compose ([MacOS](https://docs.docker.com/compose/install/), [Linux](https://docs.docker.com/compose/install/))

- Copy env template:
```bash
cp .env.template .env
```

- Init database
```bash
./manage migrate
```

- Run project
```bash
./manage main up
```

## Adding a new python dependency
To add a new package you need to update the requirements/base.in file with the pinned version (we always pin versions). Then run pip-compile

```bash
# production
./manage main run --rm api pip-compile --generate-hashes ./requirements/base.in

# development
./manage main run --rm api pip-compile --generate-hashes ./requirements/dev.in
```

Now you should have a changed requirements base.in and dev.txt - you should commit both to the git repo.


## Upgrading a python dependency

```bash
./manage main run --rm api pip-compile --upgrade-package [package-name]==[package-version] --generate-hashes
```


## Run python tests

```bash
./manage test run --rm test pytest -vv --asyncio-mode=auto
```


## Database migrations
In our case, database migration is implemented through the alembic package

To create a new migration run following command
```bash
./manage makemigrations -m "<your_message>"
```

To apply you migration locally run following command
```bash
./manage migrate
```
