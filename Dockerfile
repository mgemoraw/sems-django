FROM python:3.12
ENV SEMSVERSION 1

# set working directory to app
WORKDIR /app

# copy and intall dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# copy project files
COPY . /app

# Expose port (optional but recommended)
EXPOSE 8000

# Run django server
CMD python manage.py runserver 0.0.0.0:8000