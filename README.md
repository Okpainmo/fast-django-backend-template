# fast-django-backend-template.

A modular, and highly flexible Python Django(with the Django Ninja framework) template, for easily bootstrapping Django projects, and building super-fast backends/servers. 

> Built with so much love ❤️ for myself, and engineering teams that I lead/work on.

The template is domain-driven-development(DDD)-inspired, and comes with 3 default/sample domains to demonstrate the beautiful modular standard it follows.

## About the Django Ninja Framework

Django Ninja is a fast, modern web framework built on top of Django and powered by Python type hints. It is designed to create high-performance APIs quickly and with minimal code. If you're familiar with Django and want to build APIs without the complexity of Django REST Framework, Django Ninja is a lightweight and expressive alternative.

### Why Choose Django Ninja?

- Built on Django – Fully compatible with Django’s ORM, views, models, authentication, and middleware.

- High Performance – As fast as FastAPI thanks to Starlette and Pydantic under the hood.

- Automatic Validation – Uses Pydantic for request and response data validation with full type hint support.

- Auto-generated API Docs – Comes with built-in OpenAPI and Swagger UI documentation.

- Simple & Intuitive – Less boilerplate, more productivity. Great for building clean and maintainable APIs.

> Django Ninja is heavily inspired by **FastAPI** and shares several core concepts, but it's built to work seamlessly within the Django ecosystem.

## Working Environment Support.

> As per working environments, the template supports 3 different environments(development/dev, staging, and production/prod) - with modularized settings for each. See `base > settings`. 
> 
> **This gives you the massive flexibility to test any of the working environments locally with so much ease.**
>
> Switching to a different environment is easy: **simply head to the `manage.py` file on the project's root, and un-comment the preferred environment setup. The default work environment is the "development" environment**.

E.g.

```bash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings.development')
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings.staging')
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings.production')
```

**Ensure to restart the server anytime you switch working environments!!!**

> The project has 2(two) environmental variable files(which are all intentionally un-ignored), to help you easily understand how the template's environmental variables setup works. **Endeavour to git-ignore them immediately you clone the project**.
>
> 1. `.env` - left empty - with only a comment
> 4. `.env.template` - this is simply a guide to help you set up the main `.env` that you should use. Feel free to delete it whenever you wish - which of course should be after setting up the main one.

**P.S: The template has a multi-database scope - hence has configurations for multiple databases(SQlite, and PostgreSQL for now). Kindly note that the template only utilizes PostgreSQL. The SQlite config is however left(commented) in place just in case you don't have a PostgreSQL setup, and prefer to use SQlite.**. 

## How To Use This Template.

1. Using this template is simple. The main criteria being that you know how to use Python, the Django Python Framework and the Django-Ninja framework. And also that you have Docker installed on your machine - the template is pre-configured to use local PostgreSQL databases running on Docker.

2. Create a virtual environment.

```shell
python -m venv env
```

3. Activate the virtual environment.

> windows:

```shell
source env/Scripts/activate
```

> linux/mac:

```shell
source venv/bin/activate
```

4. Check and ensure that the desired/created virtual environment is what you are currently logged on(especially in a case where the dependencies seem not to be getting installed, and/or if they seem not to be reflecting in the requirements file after installation - even after running `pip freeze > requirements.txt`).

```shell
which python
```

5. Proceed to install all project dependencies.

**with current project versions**:

```bash
pip install -r requirements.txt
```

**or, with new version installations(ensure to delete the `requirement.txt` file first)**:

```bash
pip install Django django-ninja python-dotenv psycopg2-binary gunicorn "uvicorn[standard]" # in progress
```

6. Update the current requirements.txt file - if/when necessary.

```shell
pip freeze > requirements.txt
```

7. Pull PostgreSQL image from Docker Hub.

```bash
docker pull postgres 
```

8. Setup and start the databases.

**Option 1: start them individually**.

```bash
# postgres(update the start command to suit your setup, and start databases for all the 3 environments using docker).

docker run -d --name container-name -p 543x:5432 -e POSTGRES_USER=your-user-name -e POSTGRES_PASSWORD=your-password -e POSTGRES_DB=database-name postgres

# E.g. 

# for dev:

docker run -d --name fdbt_pg__dev -p 5433:5432 -e POSTGRES_USER=your-user-name -e POSTGRES_PASSWORD=your-password -e POSTGRES_DB=fast_django_backend_template__db_dev postgres

# for staging:

docker run -d --name fdbt_pg__staging -p 5434:5432 -e POSTGRES_USER=your-user-name -e POSTGRES_PASSWORD=your-password -e POSTGRES_DB=fast_django_backend_template__db_staging postgres

# for prod:

docker run -d --name fdbt_pg__prod -p 5435:5432 -e POSTGRES_USER=your-user-name -e POSTGRES_PASSWORD=your-password -e POSTGRES_DB=fast_django_backend_template__db_prod postgres

# P.S: starting docker postgres instances for `staging` and `prod` may not be necessary since you would want to use real(remotely provisioned) databases for those.

# ===================================================================================================
# CONNECT YOUR DATABASES TO A POSTGRESQL GUI SOFTWARE/SERVICE - E.G PGADMIN, TO VIEW THEM.
# ===================================================================================================
```

**Option 2: update the added `docker-compose.yaml` file - using the added `docker-compose.template.yaml` file as a guide, and start all the databases at once**.

```bash
docker compose up -d
```

9. Start your python application/server.

```bash
python manage.py runserver
```

**Visit the server address: `http://127.0.0.1:8000/`. If everything is well set up, you should see a welcome screen like the one below**:

![Server home-screen screenshot](./public/server-homescreen.png)

The welcome screen is simply a Django template(template engine) build. TailwindCSS was used for styling.

10. Explore your project and test the following domain end-points.

```bash
.../api/v1/auth/
```

```bash
.../api/v1/user/
```

```bash
.../api/v1/admin/
```

11. Ride/speed on...

## Building Your Project With Docker.

The template comes with a pre-configured `Dockerfile`, and a `.dockerignore`. With these, building the template into a Docker image becomes as easy as running the command below.

> Remember to set to your preferred working environment - 'dev' I suppose.

```bash
docker build -t your-project-name .
```
E.g.

```bash
docker build -t fast-django-backend-template__docker .
```

With that, you can push the image to docker hub, and set-up a docker-compose configuration that pull the docker image, and starts up the database(s) - with one single command. This will provide much ease for team-mates(especially seniors and leads) who only wish to assess/test development progress - and not to contribute.

**sample Docker command to start a container that is running the image**.

```bash
docker run -d -p 8000:8000 --env-file .env --name fast-django-backend-template__docker fast-django-backend-template__docker
```

## Enforcing Coding(Contribution) Standards/Rules(Linting, Code Formatting, and more).

...in progress.

## Database Setup.

...in progress.

## Writing Tests.

...in progress.

## CI/CD Support With Jenkins.

...in progress.


