FROM python:3.7-slim-stretch
WORKDIR /flask-server
ADD ./requirements.txt ./
RUN pip install -r requirements.txt
COPY . .

# EXPOSE 5000

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000", "--debugger", "--reload"]