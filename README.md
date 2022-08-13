# DEEP  

DEEP: Database of Early English Playbooks allows scholars and students to investigate the publishing, printing, and marketing of English Renaissance drama in ways not possible using any other print or electronic resource. An easy-to-use and highly customizable search engine of every playbook produced in England, Scotland, and Ireland from the beginning of printing through 1660, DEEP provides a wealth of information about the original playbooks, their title-pages, paratextual matter, advertising features, bibliographic details, and theatrical backgrounds.


# Migration Process

## Context 
The original PHP application was scheduled for retirement by SAS computing. 
The previous Digital Humanities Specialist began work on the migration process
and gathered initial requirements from the stakeholders. This work was in progress when he passed away. 

When the new digital scholarship programmer was hired, he began work on the project in April 2022. 

The original MySQL database was dumped to a sql file by SAS computing.
That file `20220411_deep_dump.sql`, can be found in the backup directory.  That directory 
also contains html files scraped from the old site for each of the 1911 DEEP records. 

Initally, it was assumed that the database would be the best source of data for the new site.
An admin command `main/management/commands/convert_db.py` was created to export the individual deep 
records as dictionaries in a jsonl file. This script provided an opportunity to become familiar with 
the site data and the previous data model.  

However, it appears that the previous application significantly alters the data. For example, each record
has a DEEP id (int) and DEEP id display (str). The display value is altered by the application so that '10.000' becomes '10'.  Furthermore, it uses the Variant table to "pool" variants of a text and then displays the record with the lowest DEEP id. Without access to the application's code, it became very difficult to 
write tests to establish that the new site's data is identical to the existing project. This is especially true for the variant and collection data.  Rather that build from the database, it became necessary to work from the backup html files. 

However, some data that is present in the db, is used by the application, but is not displayed to the user.  These fields are included, so that the end result provides and accurate image of all the data in the previous dataset. 

HTML > Django > item_data.json > site




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
