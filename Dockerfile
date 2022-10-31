FROM node:18
WORKDIR /app
COPY package*.json /app/
COPY src/index.js /app
CMD node index.js
