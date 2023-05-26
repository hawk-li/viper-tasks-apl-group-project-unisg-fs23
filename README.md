# Viper Tasks (Group Project)

## Demo

The application is deployed at [vipertasks.hawk.li](https://vipertasks.hawk.li)

For a demo account, use the following credentials (no password required):

```
Username: demo
EMail: demo@demo.com
```

Instructions for running the application locally can be found in the deployment section below.

## Introduction

For our group project, we decided to try a python framework, that could manage a webapplication including persisting data but was still easy to use. We decided to try out [Django](https://www.djangoproject.com/), which is a python framework for web applications. Django is a Model-View-Controller (MVC) framework, which means that the application is split into three parts: The model, which is responsible for the data, the view, which is responsible for the user interface and the controller, which is responsible for the logic. Django also includes a built-in Object-Relational-Mapper (ORM), which means that the application does not have to interact with the database directly, but can use python objects instead. Django also includes a built-in webserver, which makes it easy to test the application locally.

## Features

For the use-case we decided to choose a relatively simple one, to be able to experiment with the features django offered and see how they work. We decided to create a simple task management application, where users can create tasks and specify a due date until which they have to be completed.

The tasks are then displayed in a list, where the user can see the task and has the option to complete (or delete) the task. The user can also create new tasks, which are then added to the list. Editing is currently not supported, but could be added in the future.

In addition, we created a little dashboard, where we visualize various statistics, such as
- Number of open/completed tasks
- Number of completed tasks per day
- Completion rate
- Overdue rate
- Average completion time
- Number of tasks created per day

This is achieved by using the [Chart.js](https://www.chartjs.org/) library, which is a javascript library for creating charts. The data is retrieved from the backend using AJAX requests.

## Learnings

During the development of the application, we learned a lot about the django framework and how it works. We also learned how to use the built-in ORM to interact with the database. Overall we were very satisfied with the framework, as it was easy to use and we were able to create a working application in a relatively short amount of time. While we intentionally tried to keep things simple (e.g. no authentication), we were still able to create a working application with a nice user interface. Additionally, we realized how much work can go into a "simple" application if it has to cover all possible use-cases.

Additionally, we also gained more experience in how such an application can be deployed on a webserver. We decided to use docker-compose in combination with nginx as a proxy server for the django application. This allowed us to easily deploy the application on a webserver and also made it easy to add additional services (e.g. a dedicated database) if needed (currently django automatically creates a sqlite database, which is not very scalable).

## Code

The code for the application can be found in the `vipertasks/tasks` directory. The `static` directory contains the static files (e.g. css, javascript, images) and the `templates` directory contains the html templates. The `views.py` file contains the logic for the application, while the `models.py` file contains the models for the application. The `urls.py` file contains the url mappings for the application.

## Deployment

To deploy the application locally, python 3.9 or higher is required. The application was developed using python 3.9.1, but should also work with newer versions. To install the required dependencies, run the following command in the root directory of the project:

```
pip install -r requirements.txt
```

To start the application, run the following commands:

```
cd vipertasks
python manage.py runserver
```

After running the application for the first time, django automatically creates the database. This means that the application has to be quit once and migrations have to be applied using the command:

```
python manage.py migrate
```

After that, the application can be started again using the command:

```
python manage.py runserver
```

The application is now available at [localhost:8000](http://localhost:8000).

## Server setup

To deploy the application on a webserver, we decided to use docker-compose in combination with nginx as proxy server for the django application. The docker-compose file can be found in the root directory of the project. To deploy the application, the following steps have to be performed:

1. Clone the repository on the server
2. Install docker and docker-compose
3. Modify the files in the `/nginx-conf` directory to match the domain name of the server (init-letsencrypt.sh and nginx.conf)
4. Run the file `/nginx-conf/init-letsencrypt.sh` with elevated permissions to create the required certificates
5. Run `docker-compose up -d` in the root directory of the project to start the application. This will download the required images and build the application.
