# SALARY-PROJECT
💸 Core backend service for open-source "Salary" project for RTUITLab

## Launching project in production mode
#### Git, Docker and Docker Compose must be installed

1. Clone project with submodules

```
git clone https://github.com/AlexGeniusMan/SALARY-PROJECT salary
cd salary
git submodule init
git submodule update
```

2. Generate new DJANGO_SECRET_KEY and paste it to salary_backend service as SECRET_KEY environment variable

> To generate new DJANGO_SECRET_KEY use this instruction: https://stackoverflow.com/a/57678930/14355198

```
services:
  salary_backend:
    environment:
      - SECRET_KEY=NEW_DJANGO_SECRET_KEY
```

3. Launch project

```
docker-compose up
```

> Done! Project launched on 8000 port!

## Launching project in developing mode

> Coming soon
<!---
#### Git, Docker and Docker Compose must be installed

4. Create `.env` file in the directory named `backend` and add your new django secret key to it

```
SECRET_KEY=r#l+(jiyg2m7d!f8(-zo2o2rsckwdaq4jm=_fg3$ghir5fxf6e
```

5. Create `.env` file in the directory named `frontend` and add your production URL to it

```
REACT_APP_PRODUCTION_URL = "http://<your_production_url>:8000/"
```

Note: if you want to launch project locally, set REACT_APP_PRODUCTION_URL = "http://127.0.0.1:8000/"

6. Start the project from "salary" directory

`docker-compose up --build`

> Done! Project launched on 8000 port!

![Main page](https://github.com/AlexGeniusMan/SALARY-PROJECT/blob/master/readme-images/main.png?raw=true)
-->
This project was made by RealityGang.
