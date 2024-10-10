FROM node:16-alpine AS build

LABEL authors="shaygoldstein"

WORKDIR /app

COPY package*.json ./

RUN npm install

RUN npx update-browserslist-db@latest

COPY . .

FROM node:16-alpine AS production

WORKDIR /app

COPY --from=build /app/node_modules ./node_modules

COPY --from=build /app .

EXPOSE 3000

ENTRYPOINT ["npm"]

CMD ["start"]