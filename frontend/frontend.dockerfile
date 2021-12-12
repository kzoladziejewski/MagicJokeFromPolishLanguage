FROM node:alpine3.11
RUN mkdir -p /app
WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

EXPOSE 3000
ENV NUXT_HOST=0.0.0.0
ENV NUXT_PORT=3000
ENV PROXY_API="http://localhost"

CMD [ "npm", "start" ]