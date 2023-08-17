FROM python:3.11.3
# m=create home directory, s= define shell type
RUN useradd -ms /bin/bash tamar-admin
COPY ./requirements.txt .
RUN pip install -r /requirements.txt
USER tamar-admin 
# make a new dir and enter
WORKDIR /home/tamar-admin/app
#copy the source code + depedencies 
COPY . . 
# -w = worker number
CMD ["gunicorn","-w", "3" ,"--bind", "0.0.0.0:5000", "app:app"]

