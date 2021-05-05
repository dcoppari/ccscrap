FROM python:3

ENV CROSSCHEXCLOUD_EMAIL=""
ENV CROSSCHEXCLOUD_PASSWORD=""
ENV CROSSCHEXCLOUD_COMPANY_ID=""

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./ccscrap.py" ]
