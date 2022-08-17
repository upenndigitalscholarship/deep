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
**"theater_type":"None",
**"theater":"",
** "variant_description":"",
** "author_status":null,

Current data migration workflow:
**extract data from previous database**
- create db from sql file
- generate Django models (inspectdb > models.py)
- convert_db > deeps.jsonl
**extract data from previous website**
- backup_existing_site > crawls old site and saves HTML files in backup folder
- make_items_from_html > reads HTML files and creates item-level jsonl file (web_item_data.jsonl)
- convert_web_jsonl > reads both db data and web data, imports combined data into Django project

Current site generation workflow:
- search_index, reads current Django db, generates lunr index
- build, runs search_index and builds site data assets and local site directory
- deploy, runs all previous commands and deploys the site to Netlify



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


has variants: http://deep.sas.upenn.edu/viewrecord.php?deep_id=343
in_collection: http://deep.sas.upenn.edu/viewrecord.php?deep_id=5074.03
collection_contains: http://deep.sas.upenn.edu/viewrecord.php?deep_id=5181
independent_playbook: http://deep.sas.upenn.edu/viewrecord.php?deep_id=5147.01
also in collection: http://deep.sas.upenn.edu/viewrecord.php?deep_id=1002

+-------------------------------+
| Tables_in_deep                |
+-------------------------------+
| auspice                       |
| auspice_deep                  |
| auth_group                    |
| auth_group_permissions        |
| auth_permission               |
| auth_user                     |
| auth_user_groups              |
| auth_user_user_permissions    |
| author                        |
| author_attribution            |
| author_attribution_deep       |
| author_deep                   |
| bookseller                    |
| bookseller_deep               |
| company                       |
| company_deep                  |
| dc_pdc                        |
| deep                          |
| django_admin_log              |
| django_content_type           |
| django_migrations             |
| django_session                |
| export                        |
| genreharbage                  |
| genreharbage_deep             |
| genreplaybookattribution      |
| genreplaybookattribution_deep |
| imprintlocation               |
| imprintlocation_deep          |
| playtype                      |
| playtype_deep                 |
| printer                       |
| printer_deep                  |
| pt                            |
| publisher                     |
| publisher_deep                |
| record_type                   |
| srstationer                   |
| srstationer_deep              |
| status                        |
| status_deep                   |
| theater                       |
| theater_deep                  |
| theater_type                  |
| variant                       |
| variant_newish                |
+-------------------------------+
46 rows in set (0.00 sec)
