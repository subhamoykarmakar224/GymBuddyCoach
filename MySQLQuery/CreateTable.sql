use gymms;

create table Students(
SID varchar(100) primary key,
allotedtime varchar(200),
membershipvalidity varchar(200),
phone varchar(100),
studentage varchar(10),
studentname varchar(100),
regstatus varchar(100),
dueamount varchar(100) default "0"
);

create table Notification(
notifId varchar(100) primary key,
studentId varchar(100), 
dateTime varchar(100),
level varchar(10),
msg text
);

create table GymAdmin(
gymId varchar(100) primary key,
gymName varchar(100),
adminName varchar(100),
phone varchar(100),
validity varchar(100),
username varchar(100),
passwd text,
loginstatus int 
);
