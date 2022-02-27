FROM node:alpine3.11

RUN mkdir -p /app
WORKDIR /app

COPY ../../../frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm install
RUN npm run build

EXPOSE 3000
CMD [ "npm", "start" ]