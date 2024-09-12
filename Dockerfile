FROM alpine
EXPOSE 8000

RUN apk update && apk add nano python3 tzdata iputils bash p7zip
RUN mkdir HolidayPlanner

ENV PYTHONIOENCODING=UTF-8
RUN echo "export PS1='\u@\h:\w\\$ '" >> ~/.bashrc

COPY HolidayPlanner /HolidayPlanner/
COPY db.sqlite3 /HolidayPlanner
COPY manage.py /HolidayPlanner
COPY requirements.txt /HolidayPlanner
WORKDIR /HolidayPlanner
RUN python3 -m venv /HolidayPlanner/venv
RUN . /HolidayPlanner/venv/bin/activate && python3 -m ensurepip && pip3 install --upgrade pip setuptools && pip3 install -r requirements.txt
    #&& python3 manage.py migrate

#ENTRYPOINT [".", "/app/venv/bin/activate", "&&", "python3 manage.py runserver"]
ENTRYPOINT ["tail", "-f", "/dev/null"]