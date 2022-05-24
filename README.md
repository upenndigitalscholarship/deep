# DEEP  

DEEP: Database of Early English Playbooks allows scholars and students to investigate the publishing, printing, and marketing of English Renaissance drama in ways not possible using any other print or electronic resource. An easy-to-use and highly customizable search engine of every playbook produced in England, Scotland, and Ireland from the beginning of printing through 1660, DEEP provides a wealth of information about the original playbooks, their title-pages, paratextual matter, advertising features, bibliographic details, and theatrical backgrounds.

On the Digital Ocean server, this app has the following configuration.  

**/etc/systemd/system/deep.service **
```
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=www-data
WorkingDirectory=/srv/deep
ExecStart=/srv/deep/venv/bin/gunicorn deep.wsgi --workers 4 --bind unix:/srv/deep/deep.sock --access-logfile /srv/deep/access.log --error-logfile /srv/deep/error.log

[Install]
WantedBy=multi-user.target
```

**/etc/nginx/sites-available/deep**

```
server {
    server_name deep.pennds.org;
    listen 80;

    location /assets {
        alias /var/www/assets;
    }

    location /admin {
        include proxy_params;
        proxy_pass http://unix:/srv/deep/deep.sock;

    }

    location / {
        root /srv/deep/site;
        index index.html;
    }


}
```
