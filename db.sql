/*╥ипехуж╬*/
drop table if exists fetion_log;
create table fetion_log(
	id int(11) not null primary key auto_increment,
	user varchar(64),
	msg varchar(256),
	ip varchar(16),
	status varchar(28),
	stime timestamp not null default '0000-00-00 00:00:00'
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

drop table if exists filter_ip;
create table filter_ip(
	id int(11) not null primary key auto_increment,
	ip varchar(16),
	stime timestamp not null default '0000-00-00 00:00:00'
)ENGINE=InnoDB DEFAULT CHARSET=utf8;