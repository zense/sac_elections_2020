# IMP: Make sure the container starts up on 172.17.0.3
# IMP: Change pass on production

GRANT ALL PRIVILEGES ON *.* TO 'root'@'172.17.0.3' IDENTIFIED BY 'devPass123' WITH GRANT OPTION;
SET PASSWORD FOR root@'172.17.0.3' = PASSWORD('root');
FLUSH PRIVILEGES;