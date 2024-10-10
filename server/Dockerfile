FROM node:16-alpine AS build

LABEL authors="shaygoldstein"

WORKDIR /server

COPY package*.json ./

RUN npm install

COPY . .

FROM node:16-alpine AS production

WORKDIR /server

COPY --from=build /server/node_modules ./node_modules

COPY --from=build /server .

EXPOSE 5050

ENTRYPOINT ["npm"]

CMD ["run", "dev"]