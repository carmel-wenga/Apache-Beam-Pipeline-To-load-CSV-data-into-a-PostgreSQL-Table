# base image
FROM postgres:13-alpine

# run init.sql on init to create the salaries table into the database
COPY init.sql /docker-entrypoint-initdb.d
