use mysql
create user 'onsoim'@'localhost' identified by 'onsoim';
grant all privileges on *.* to 'onsoim'@'localhost';
create database accounts;
