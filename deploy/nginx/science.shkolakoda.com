# Nginx configuration for WebGarden Happy Science.
#
# Install only after the local service responds on 127.0.0.1:8005:
#   sudo cp deploy/nginx/science.shkolakoda.com /etc/nginx/sites-available/science.shkolakoda.com
#   sudo ln -s /etc/nginx/sites-available/science.shkolakoda.com /etc/nginx/sites-enabled/science.shkolakoda.com
#   sudo nginx -t
#   sudo systemctl reload nginx
#
# The existing shkolakoda.com certificate already covers science.shkolakoda.com.
# IPv6 listen lines are required to avoid SNI/default-certificate mismatches.

server {
    listen 80;
    listen [::]:80;
    server_name science.shkolakoda.com;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl;
    listen [::]:443 ssl;
    server_name science.shkolakoda.com;

    ssl_certificate /etc/letsencrypt/live/shkolakoda.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/shkolakoda.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    access_log /var/log/nginx/science-shkolakoda-access.log;
    error_log /var/log/nginx/science-shkolakoda-error.log;

    client_max_body_size 5M;
    root /var/www/webgarden/sites/science;

    location /static {
        alias /var/www/webgarden/sites/science/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    location = /favicon.ico {
        alias /var/www/webgarden/sites/science/static/favicon.ico;
        log_not_found off;
        access_log off;
    }

    location = /robots.txt {
        alias /var/www/webgarden/sites/science/static/robots.txt;
        log_not_found off;
        access_log off;
    }

    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }

    location / {
        proxy_pass http://127.0.0.1:8005;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;

        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;

        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 8 4k;
    }
}
