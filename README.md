# sac_elections

App to facilitate SAC elections. Ensures databse integrity through hashing.

## Intstallation

### End Usage:
  **Use branch 'master'**
  1. Copy docker-compose.yml file
  ```
  cp docker-compose.yml.example docker-compose.yml
  ```
  2. Change the docker-compose.yml file and change credentials
  3. Copy settings.py file
  ```
  cp sac_elections/sac_elections/settings.py.example sac_elections/sac_elections/settings.py
  ```
  4. Change the credentials (such as app_secret) in the file
  5. Copy nginx config file
  ```
  cp production/nginx/sac_elections.conf.example production/nginx/sac_elections.conf
  ```
  6. Run command
  ```
  docker-compose build
  ```
  7. Run command
  ```
  docker-compose up
  ```
### Development:

**Use branch 'staging2'**
  1. Copy docker-compose.yml file
  ```
  cp docker-compose.yml.example docker-compose.yml
  ```
  2. Change the docker-compose.yml file and change credentials
  3. Copy settings.py file
  ```
  cp sac_elections/sac_elections/settings.py.example sac_elections/sac_elections/settings.py
  ```
  4. Change the credentials (such as app_secret) in the file
  5. Run command
  ```
  docker-compose build
  ```
  6. Run command
  ```
  docker-compose up
  ```
  
#### 

**Note:** Any credentials found in the commit history have been destroyed ;)
