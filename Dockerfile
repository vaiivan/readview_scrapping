FROM python:3.9

# FROM jupyter/pyspark-notebook:python-3.9

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install 
RUN playwright install-deps

COPY . .

CMD [ "python", "./books_in_print_list_5.py" ]