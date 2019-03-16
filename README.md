Health
====

Provide the basic recording features for storage the health properties.

Docker
====

The application is developed by [Docker](https://www.docker.com/) technologies.
Execute the application simply by the following command:

   ```bash
   docker run --name health.kenson.idv.hk --rm -p 80:80 -p 443:443 [-e "ENV=value"] hubs.mansonsolutions.hk/kenson.health:latest
   ```

Supported Environment Variables
====

### Database related
- DBMS                  - The database backend. e.g.: "django.db.backends.sqlite3", "django.db.backends.postgresql";
- DBNAME                - The name of the database. If sqlite3, this should be the database file path (e.g. "./sqlite3.db");
- DBHOST                - The host-name of the database;
- DBPORT                - The port-num of the database;
- DBUSER                - The database login name;
- DBPASS                - The database login password;

### Django related
- SECRET_KEY            - The [secret key](https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-SECRET_KEY) in django;
- SECURE_SSL_REDIRECT   - The boolean value of [secure ssl redirect](https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-SECURE_SSL_REDIRECT) in django;
- ALLOWED_HOST          - The [host name](https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-ALLOWED_HOSTS);
- DEBUG                 - The indicator of [debug](https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-DEBUG) status;
