FROM python:3.10
WORKDIR /app
RUN apt update
RUN apt install -y libgl1-mesa-glx
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
# run the command to start uWSGI
#CMD ["uwsgi", "app.ini"]
