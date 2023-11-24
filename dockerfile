FROM python:3.10.12

WORKDIR /usr/src/app

EXPOSE 5000

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["flask", "run", "--host=0.0.0.0", "--debug"]