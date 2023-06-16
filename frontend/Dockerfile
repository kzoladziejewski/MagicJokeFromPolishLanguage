FROM node:alpine3.11

RUN mkdir -p /app
ADD . app/
WORKDIR app

RUN npm install
RUN npm run build

EXPOSE 3000
CMD [ "npm", "start" ]