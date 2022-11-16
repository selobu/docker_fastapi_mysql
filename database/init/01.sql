CREATE DATABASE IF NOT EXISTS ventas2022
        CHARACTER SET = 'utf8'
        COLLATE = 'utf8_general_ci'
        COMMENT = 'Administrar las ventas';
        
DROP USER IF EXISTS 'adminuser'@'backend';

CREATE USER IF NOT EXISTS 'adminuser'@'backend' IDENTIFIED BY 'adminuser123';

GRANT USAGE ON ventas2022.* TO 'adminuser'@'backend';
-- GRANT ALL PRIVILEGES ON ventas2022.* TO 'adminuser'@'backend';

FLUSH PRIVILEGES;
-- GRANT USAGE ON *.* TO tom@'%';
