FROM node:17-alpine

# Add bash
RUN apk update
RUN apk upgrade
RUN apk add bash

# Set work directory
WORKDIR /usr/src/app

# Update npm
RUN npm install --location=global npm

# Install Gulp
RUN npm install --location=global gulp-cli

# Add package.json
COPY ./package.json package.json

# Add dependencies gulp
RUN npm i
