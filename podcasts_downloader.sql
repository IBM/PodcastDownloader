DROP DATABASE  if exists podcast_downloader;
CREATE DATABASE podcast_downloader;

USE podcast_downloader;

drop table if exists customers;

create table customer
(
customerid INT(10) not null AUTO_INCRAMENT,
name varchar(30) not null,
PRIMARY KEY(custpodomerid)
) ENGINE=InnoDB;

drop table if exists podcast;

create table podcast
(
podid INT(10) not null AUTO_INCRAMENT
podname varchar(50) not null,
url varchar(200) not null,
PRIMARY KEY (podid)
) ENGINE=InnoDB;

drop table if exists subs;

create table subs
(
subid INT(10) not null AUTO_INCREMENT,
customerid INT not null,
podid INT not null,
PRIMARY KEY (subid)
FOREIGN KEY (customerid) REFERENCES customer(customerid) ON UPDATE CACADE ON DELETE CASCADE,
FOREIGN KEY (podid) REFERENCES podcast(podid) ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB;