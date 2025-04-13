# Build step
FROM node:22-alpine AS builder
WORKDIR /app
COPY . .
RUN npm install && npm run build

# Serve with nginx
FROM nginx:stable-alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80