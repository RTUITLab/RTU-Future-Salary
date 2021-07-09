# SALARY-PROJECT
💸 Salary is a web service that allows you to calculate guaranteed payments to faculty members at RTU MIREA

## Launching project in production mode
#### Git, Docker and Docker Compose must be installed

1. Clone project with submodules

```
git clone https://github.com/RTUITLab/RTU-Future-Salary salary
cd salary
git submodule init
git submodule update
```

2. Generate new DJANGO_SECRET_KEY and paste it to salary_backend service as SECRET_KEY environment variable in docker-compose.yml

> To generate new DJANGO_SECRET_KEY use this instruction: https://stackoverflow.com/a/57678930/14355198

```
services:
  salary_backend:
    environment:
      - SECRET_KEY=NEW_DJANGO_SECRET_KEY
```

3. Put your PRODUCTION_URL to salary_frontend service as YOUR_PRODUCTION_URL environment variable in docker-compose.yml
```
services:
  salary_frontend:
    environment:
      - REACT_APP_PRODUCTION_URL=http://YOUR_PRODUCTION_URL:8000/
```

4. Launch project

```
docker-compose up --build
```

> Done! Project launched on 8000 port!

<!---

-->
Demonstration: https://youtu.be/CYeBP6JI1FY

![Main page](https://github.com/AlexGeniusMan/SALARY-PROJECT/blob/master/readme-images/main.png?raw=true)

This project was made by RealityGang - team of RTUITLab.
