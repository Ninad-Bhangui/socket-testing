FROM node:12-alpine
WORKDIR /node-server
COPY package.json yarn.lock ./
RUN yarn install
COPY . .

CMD ["node", "index.js"]
