FROM mcr.microsoft.com/playwright:v1.26.0-focal

# FROM jupyter/pyspark-notebook:python-3.9

WORKDIR /usr/src/app

COPY requirements.txt ./

# RUN playwright install 
# RUN playwright install-deps
RUN apt update -y
RUN apt-get install python3.9 -y
RUN apt-get install python3-pip -y
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install
RUN playwright install-deps

COPY . .

CMD [ "python3", "./books_in_print_list_4.py" ]