# SALARY-PROJECT
Core backend service for open-source "Salary" project for RTUITLab


## Launching project
#### Git, Docker and Docker Compose must be installed
1. Create new directory and open it

`mkdir salary`

`cd salary`

2. Clone backend

`git clone https://github.com/AlexGeniusMan/SALARY-PROJECT .`

3. Clone frontend

`git clone https://github.com/Zayac11/Salary frontend`


4. Create `.env` file in the directory named `backend` and add your new django secret key to it

```
SECRET_KEY=r#l+(jiyg2m7d!f8(-zo2o2rsckwdaq4jm=_fg3$ghir5fxf6e
```

5. Create `.env` file in the directory named `frontend` and add your production URL to it

```
REACT_APP_BASE_URL = "http://127.0.0.1:8000/"
REACT_APP_PRODUCTION_URL = "<your_production_url>"
```

6. Start the project

`docker-compose up --build`

> Done! Project launched!

This project was made by Dev.gang.
