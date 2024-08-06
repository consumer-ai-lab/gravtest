FROM node:alpine

WORKDIR /usr/nodeapp

COPY ./package.json ./

EXPOSE 5000

RUN npm install

COPY ./ ./

CMD [ "npm", "start" ]
