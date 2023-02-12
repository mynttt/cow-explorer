FROM python:3.7
RUN pip install Flask Flask-Cors gunicorn
COPY api/ /app
WORKDIR /app
ENV PORT 8080
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 api:app
