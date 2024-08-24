# WhatsApp Bot Project


## Prerequisites

- Python 3.11+
- PostgreSQL database
- ngrok (for local use only)
- Install requirements

```bash
pip install -r requirements.txt
```

## Running the project in dev mode

To start the project, leave running both commands
Ngrok is used to expose the local server to the internet, so that Facebook can reach it.

```bash
uvicorn main:app --reload
ngrok http 8000
```

You can claim a fixed url or static domain on ngrok with a free account:

1. Log in to your ngrok account.
2. Navigate to Cloud Edge > Domains.‍
3. Follow the prompts to claim your unique, static domain.

After that, you can start de ngrok service with that static domain:

```bash
ngrok http --domain=[static-domain] 8000
```

## Setting up with Facebook

To set up the bot with Facebook, you need to create a Facebook App 
at developers.facebook.com. When asked for app type, select 'business'
In the app dashboard, add Whatsapp as a product.

From the API Setup page, you can get your Phone Number ID, that goes into the url ```(FACEBOOK_WHATSAPP_API_URL)```; and a temporary access token for the env variable ```(FACEBOOK_WHATSAPP_TOKEN)```.

Then, you need to create a Webhook. First, set a token in the env variable ```(FACEBOOK_VERIFY_TOKEN)```. This is like a password, so it can be whatever you want. 

Then in the Facebook page, set the webhook url to the ngrok url, with the path ```/whatsapp-webhook```. You have to verify the url with the python server running for it to work

Also, you need to configure the webhook fields to be ```messages```.

### Generating a permanent access token

You need to set up a system user as the admin of your app. You can then generate never expiring access tokens for this system user.

Add a system user to your facebook app if it doesn't exist yet. Make sure it has the admin role.

On the same page, in the "Assigned Assets" section, check whether your app is listed here. If not, add your app via the "Add asset" button, granting "Full control" over your app.

Add the system user to your Whatsapp account in the "People" section, granting "Full control" over your Whatsapp account

Now click the "Generate new token" button for above system user which reveals a "Generate token" popup. Select the 2 permissions whatsapp_business_management and whatsapp_business_messaging and confirm

A new access token is presented to you as a link. Click it and then store the generated token safely as it will not be stored for you by facebook. This token will not expire.

## Running Lunary

Lunary is a webapp to track LLM usage and expenses.
It consists of a frontend and a backend. The frontend is a NextJS app, and the backend is a Express API built with Koa.

### Lunary database requirement and migrations

Lunary needs to connect to a PostgreSQL database to save and persist the managed data. It can use the same server that the chatbot uses, but with a different database. For this project, the environment variable DATABASE_URL has been changed to LUNARY_DATABASE_URL.

Lunary, being a Node.js application, handles database migration with the command:

```shell
npm run migrate:db
```

This command needs to be executed in the Lunary directory.

Lunary doesn't have any commands to revert migrations. The "versions" of the database are `.sql` files in the `db` folder that are executed sequentially. If any change to the database needs to be added, will be adding a new file or script in this folder following the numbers in the file name.

## Database Migrations for Chatbot with Alembic

Alembic is a database migration tool written by the author of SQLAlchemy. It offers several functionalities: it can emit ALTER statements to a database, provides a system for constructing "migration scripts," and allows these scripts to execute sequentially.

To learn more about Alembic and how it works, you can visit the [Alembic webpage](https://alembic.sqlalchemy.org/en/latest/).

The Alembic folder is located under the `migrations` folder, which has the following modifications:

* The `env.py` file has been modified to fetch environment variables and set the `sqlalchemy.url` correctly.
* In the `env.py` file, the `target_metadata` has been changed to point to the project's models.
* The line setting the `sqlalchemy.url` variable in the `alembic.ini` file has been commented out.

Each migration file is located in the `versions` sub-directory. The first migration file represents the initial project setup and contains the first tables.

Alembic provides the `alembic` command to control the database state. Here are the main commands:

* `alembic revision --autogenerate -m "name of the migration"`: Checks the models and compares them with the existing tables in the database. Any differences are used to create a new migration. If there are no differences, the developer can add their custom script.
* `alembic upgrade head`: Migrates or upgrades the database to the latest version.
* `alembic downgrade -1`: Downgrades the database by one version.
* `alembic downgrade base`: Downgrades all the versions.
* `alembic current`: Prints the hash string of the current database version or migration.
* `alembic history`: Prints all the versions applied to the database.
