# fast-django-backend-template.

A modular, and highly flexible Python Django(with the Django Ninja framework) template, for easily bootstrapping Django projects, and building super-fast backends/servers. 

> Built with so much love(❤️) for myself, and engineering teams that I lead/work on.
>
> The template is domain-driven-development(DDD)-inspired, and comes with 3 default/sample domains to demonstrate the beautiful modular standard it follows.

## About the Django Ninja Framework

Django Ninja is a fast, modern web framework built on top of Django and powered by Python type hints. It is designed to create high-performance APIs quickly and with minimal code. If you're familiar with Django and want to build APIs without the complexity of Django REST Framework, Django Ninja is a lightweight and expressive alternative.

### Why Choose Django Ninja?

- Built on Django – Fully compatible with Django’s ORM, views, models, authentication, and middleware.

- High Performance – As fast as FastAPI thanks to Starlette and Pydantic under the hood.

- Automatic Validation – Uses Pydantic for request and response data validation with full type hint support.

- Auto-generated API Docs – Comes with built-in OpenAPI and Swagger UI documentation.

- Simple & Intuitive – Less boilerplate, more productivity. Great for building clean and maintainable APIs.

> Django Ninja is heavily inspired by **FastAPI** and shares several core concepts, but it's built to work seamlessly within the Django ecosystem. I consider it to be like having the best of both worlds - Enjoying the robustness of Django(especially the speed that it's pre-configured setups provides), while still making the best of the simplicity and control that FastAPI affords.

## Working Environment Support.

> As per working environments, the template supports 3 different environments(development/dev, staging, and production/prod) - with modularized settings for each. See `base > settings`. 
> 
> **This gives you the massive flexibility of being able to test any of the working environments locally with so much ease.**
>
> Switching to a different environment is easy: **simply head to the `manage.py` file on the project's root, and un-comment the preferred environment setup. The default work environment is the "development" environment**.

I.e.

```python
# ...code before

# ==================================================================================================================
# selecting the preferred/current working environment.
# ==================================================================================================================

# default - no longer needed
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')

# Split set-up due to the project's decentralized configuration. For production deployment, environment selection must be
# handled here(`manage.py`), inside `base -> settings -> wsgi.py` and inside `base -> settings -> asgi.py`. But
# For development(when in a local environment), selection will work even when done in only this file(`manage.py`).
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings.development')
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings.staging')
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings.production')

# =================================================================================================================
# selecting the preferred/current working environment.
# =================================================================================================================


# ...code after
```

**Ensure to restart the server anytime you switch working environments!!!**

### Environment Variables

> The project has a template environmental variable files - to help you easily understand how the project's environmental variables setup works. 
>
> `.env.template` - is simply a guide to help you set up the main `.env` that you should use. Feel free to delete it whenever you wish - which of course should be after setting up the main one. Simply create the `.env`, then copy the content of `.env.template` into it and make necessary updates.

**P.S: The template has a multi-database scope - hence it has configurations for multiple databases(SQlite, and PostgreSQL for now). Kindly note that the template only utilizes PostgreSQL. However, the SQlite config is left(commented) in place just in case you don't have a PostgreSQL setup, and prefer to use SQlite.**. 

## How To Use This Template.

1a. Using this template is simple. The main criteria being that you know how to use Python, the Django framework and the Django-Ninja framework. One other important requirement, is that you should have Docker installed on your machine - the template is pre-configured to use local PostgreSQL databases running on Docker.

1b. Create a project repository(using this as a template), and settle in to start working.

```bash
git clone your-new-project-repo-url

cd your-project-name
```

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
source env/bin/activate
```

4. Check and ensure that the desired/created virtual environment is what you are currently logged on(especially in a case where the dependencies seem not to be getting installed, and/or if they seem not to be reflecting in the requirements file after installation - even after running `pip freeze > requirements.txt`).

```shell
which python
```

5a. Proceed to install all project dependencies.

**with current project versions**:

```bash
pip install -r requirements.txt
```

**or, with new version installations(ensure to delete the `requirement.txt` file first)**:

```bash
pip install Django django-ninja python-dotenv psycopg2 psycopg2-binary gunicorn "uvicorn[standard]" black pylint pylint-django pre-commit PyJWT structlog[json] boto3
# in progress
```

5b. Install hook for `pre-commit`

```bash
pre-commit install
```

6. Update the current requirements.txt file - if/when necessary.

```shell
pip freeze > requirements.txt
```

7. Pull PostgreSQL database image from Docker Hub.

```bash
docker pull postgres 
```

8. Setup and start the databases.

**Option 1: start them individually**.

```bash
# update the start command to suit your setup, and start databases for all the 3 environments using docker.

docker run -d --name container-name -p 543x:5432 -e POSTGRES_USER=your-user-name -e POSTGRES_PASSWORD=your-password -e POSTGRES_DB=database-name postgres
```
E.g. 

```bash
# for dev:

docker run -d --name fdbt_pg__dev -p 5433:5432 -e POSTGRES_USER=your-user-name -e POSTGRES_PASSWORD=your-password -e POSTGRES_DB=fast_django_backend_template__db_dev postgres
```

```bash
# for staging:

docker run -d --name fdbt_pg__staging -p 5434:5432 -e POSTGRES_USER=your-user-name -e POSTGRES_PASSWORD=your-password -e POSTGRES_DB=fast_django_backend_template__db_staging postgres
```

```bash
# for prod:

docker run -d --name fdbt_pg__prod -p 5435:5432 -e POSTGRES_USER=your-user-name -e POSTGRES_PASSWORD=your-password -e POSTGRES_DB=fast_django_backend_template__db_prod postgres
```

> P.S: starting docker postgres instances for `staging` and `prod` may not be necessary since you would want to use real(remotely provisioned) databases for those.

CONNECT YOUR DATABASES TO A POSTGRESQL GUI SOFTWARE/SERVICE - E.G PGADMIN, TO VIEW THEM.

**Option 2: create a `docker-compose.yaml` file on the project's root - and update it with the content of `docker-compose.template.yaml`, then proceed to start all the databases at once with command below**.

```bash
docker compose up -d
```

9. Start your python application/server.

```bash
python manage.py runserver
```

9b. Visit the server address: `http://127.0.0.1:8000/`. If everything is well set up, you should see a welcome screen like the one below:

![Server home-screen screenshot](./public/server-homescreen.png)

The welcome screen is simply a Django template(template engine) build. TailwindCSS was used for styling.

10. Take a deep breath, reward yourself with a coffee break, and return to hack on.

## Building The Template With Docker.

The template comes with a pre-configured `Dockerfile`, and a `.dockerignore`. With the Dockerfile in place, building the template into a Docker image becomes as easy as running the command below.

> Remember to set to your preferred working environment - 'dev' I suppose.

```bash
docker build -t your-project-name .
```
E.g.

```bash
docker build -t fast-django-backend-template__docker .
```

**sample Docker command to start a container that is running the image**.

```bash
docker run -d -p 8001:8000 --env-file .env --name fast-django-backend-template__docker fast-django-backend-template__docker
```

> Instead of building the app/server directly with Docker, while still separately setting up the databases with docker-compose, you can set-up the docker-compose configuration to handle everything(build the app/server, and start up the database(s)) - all with one single command. This will provide much ease for team-mates(especially seniors and leads) who only wish to assess/test the development progress - and not to contribute. Ensure to use separate ports for the app/server running on docker, and the one running locally on your machine, so as to avoid conflicts. See `docker-compose.template.yaml` for help.

## Enforcing Coding Contribution(Collaboration) Standards(Linting, Code Formatting, and more).

This template is built to support the best industry standards available. Hence enforcing code quality
was a core focus.

1. For linting, [**Pylint**](https://pypi.org/project/pylint/) was used. See the `.pylintrc` file on the project root, for **Pylint** configurations.

To format your code manually, Simply run the code below on the project's root directory.

```bash
pylint .
```

> P.S: Looking into the `.pylintrc` file, you will find some **disabled** Pylint rules. It is very important, that you access, and set up all of them in a way that suits your preferences/standards - especially the rules with an "# approve" comment/flag at their ends. I highly recommend that you look out for those, un-disable them(turn them back on), and verify that you're okay with them being disabled.

2. For code-formatting [**Black**](https://github.com/psf/black) was used. Check out the `pyproject.toml` file on the project's root for Black configurations.

Run the command below on the project's root directory, to enforce code formatting with Black.

```bash
black .
```

3. As can be seen so far(if left that way), linting and code-formatting would be manual, hence collaborating developers can easily forget to run the necessary checks before pushing their contributions to Github.

To solve that issue, [**pre-commit**](https://pre-commit.com) was used to enforce automated linting and code-formatting on all **staged** files to be committed - before a commit is allowed.

To run the pre-commit hook manually(on all related files in this case - not just for staged ones), use the command below:

```bash
pre-commit run --all-files
```

The above command, will run both **Black** and **Pylint** - ensuring both linting and code-formatting checks.

> P.S: You do not need to run the manual command for `pre-commit`. If you follow all instructions, and set up the template correctly, a pre-commit task would be automatically triggered whenever you try to make any code commit to Github, thereby - linting and formatting your code automatically.
>
> The pre-commit configuration file, is the `pre-commit-config.yaml` file which can be found on the project's root.

## Sample End-points.

As earlier stated, the project comes with 3 different domains(the auth domain, the user domain, and the admin domain) that help to demonstrate how to keep things modular, domain-driven, neat, and professional.

Below are the 3 default domains and their sample end-point, which you can build on top of - if you wish.

### Default Domains And Their End-points.

1. Admin:

- Endpoints:

    - De-activate user - /api/v1/admin/deactivate-user/:userId

2. Auth:

- Endpoints:

    - Log-in - /api/v1/auth/log-in
    - Register - /api/v1/auth/register

3. User:

- Endpoints:

    - Get user profile - /api/v1/user/:userId

## Want To Contribute?

This project will be a progressive one. I and any other contributor(s), will continue to add relevant updates. This makes it very important that you always share details about any contribution you wish to make - before-hand, and avoid the needless stress of proceeding to work a contribution for a topic that is already in-progress.

To contribute successfully, simply create a Github issues that mentions me, and I'll be right with you to discuss your proposed/intended contribution.

Feel free to drop a star, fork/use, and share every contributions you possibly can.

## Wrapping up.

> Just in case this repository ever gets to save your butt at work or while learning to build production-grade Node/Express with Typescript APIs, and you wish to send an appreciation, [feel free to buy me a 'coffee'](https://paystack.com/pay/cagnddqmr2).

Cheers!!!