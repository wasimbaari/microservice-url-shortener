FROM nginx:alpine
RUN apk upgrade --no-cache

# Copy frontend files
COPY frontend/ /usr/share/nginx/html/

# Copy nginx config
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

