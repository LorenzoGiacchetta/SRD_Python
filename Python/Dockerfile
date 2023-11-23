FROM python:3.10
WORKDIR /app
EXPOSE 5000
RUN apt update
RUN apt install -y libgl1-mesa-glx
RUN apt install -y python3-pil tesseract-ocr libtesseract-dev tesseract-ocr-eng tesseract-ocr-script-latn libleptonica-dev tesseract-ocr python3-pil tesseract-ocr-eng tesseract-ocr-script-latn libleptonica-dev liblept5
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
# run the command to start uWSGI
#CMD ["uwsgi", "app.ini"]
