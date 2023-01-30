
## 0 - Requirements
1. Python 3.10.6
2. NodeJS 18.X
3. npm 8.19.3
4. Yarn

### 0.1 - Install NodeJS and Yarn
Here a list of commands to install the correct version of NodeJS if you are using linux or similar systems. If not, please check the offical Node [website](https://nodejs.org/en/)
```
sudo curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
sudo npm install -g yarn
```
If you encounter some problems, check [HERE](https://github.com/nodesource/distributions/issues/1157) 

## 1 - Setup
This webapp use sqlite3 so you don't need any other DB connection. All the commands listed use as root path, the root of the project.

### 1.1 - Python dependecies
Make you you are running the correct python version as per app's requirements (you can check it by running `python --version`) and install python dependecies by running `pip install -r ./requirements.txt`.

### 1.2 - JS dependecies
Install all the javascript dependencies by running the command `yarn` in the `./frontend` folder.

### 1.3 - ENV file
Create a `.env` file by creating it or copying it from the `.env.example` and fill the `SECRET_KEY` and `DEBUG` configs.

## 2 - Database
If the app does not provide a `./db.sqlite3` file, you need to run this commands

### 2.1 - Migration
Run `python ./manage.py makemigrations` to make sure no migrations were left uncommited, then run `python ./manage.py migrate`. This will create the database's file along with all the tables

### 2.2 - Create superuser (optional)
Run the command `python manage.py createsuperuser` and type your email and password

## 3 - Run the app
To run the app make sure that the following commands are running simultaneously. By default, the API server will be hosted on port 8000 and the Frontend server on the port 3000.

### 3.1 - API/Backend
Run the command `python manage.py runserver`. You can also specify the port simply by typing it after the command `python manage.py runserver 8100` (default is 8000). If you change port make sure to edit the frontend config file. More on that in the point below

### 3.2 - Frontend
Run the command `cd ./frotend && yarn dev` to start the app in DEV mdoe. If you want to build the app for deployment you can either chose to run `yarn build && yarn start` (Server Deployment) or  `yarn generate` (Static Deployment (Pre-rendered)). Follow the [Official Documentation](https://nuxtjs.org/docs/get-started/commands/) for further details. If you changed the port for the backend, please edit the `./frontend/nuxt.config.js` at the following part:
```
  axios: {
    baseURL: 'http://127.0.0.1:[NewPort]/api/v1',
  },
```

### 3.2.1 - Troubleshooting
If you encounter some problem when running the `yarn ...` commands you need to check the file `./frontend/package.json` in the `script` section:
1. If you are using linux or similar systems make sure to have `export  NODE_OPTIONS=--openssl-legacy-provider && [...]` before all the commands
2. If you are using windows `set NODE_OPTIONS=--openssl-legacy-provider && [...]`

## 4 - Browse the app
You can navigate the app at the frontend url (by default is http://localhost:3000/). 

If you need to access the admin panel, you can go to http://localhost:8000/admin/ (or change the porti if you edited it).