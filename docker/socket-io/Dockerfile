FROM node:15.9

ENV APP_ROOT /app
WORKDIR ${APP_ROOT}
COPY ./websockets/package*.json ./
RUN npm install
COPY ./websockets .
EXPOSE 4000
CMD ["npm", "run", "start"]