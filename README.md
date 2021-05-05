
# CrossChex Cloud Scrap

CrossChex is personnel identity verification, access control and time attendance management system.
The cloud version let you manage remote attendance systems all in one place.

## Instalation

You can build and run the image using docker

```
docker build -t ccscrap .
```

Runing the image

```
docker run -ti --rm \
-e "CROSSCHEXCLOUD_EMAIL=myportal@email.com" \
-e "CROSSCHEXCLOUD_PASSWORD=h4ckmyp4ss" \
-e "CROSSCHEXCLOUD_COMPANY_ID=1234" \
ccscrap
```

The process will login and dump the information of current day only.
