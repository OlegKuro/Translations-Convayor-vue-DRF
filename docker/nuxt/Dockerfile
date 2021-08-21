FROM node:15.9

ENV APP_ROOT /app
WORKDIR ${APP_ROOT}
COPY ./frontend/package*.json ./
RUN npm install
COPY ./frontend .
RUN npm run build
EXPOSE 3000