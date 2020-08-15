use gymms;

create table Students(
SID varchar(100) primary key,
allotedtime varchar(200),
membershipvalidity varchar(200),
phone varchar(100),
studentage varchar(100),
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
memberrole varchar(100),
gymName varchar(100),
adminName varchar(100),
phone varchar(100),
validity varchar(100),
username varchar(100),
passwd text,
loginstatus int
);

create table localaction(
actiontime datetime,
module varchar(100),
action varchar(100),
status int
);

create table softwareflags(
flagname varchar(100),
status int
);

create table msgnotif(
msgcounter int primary key,
SID varchar(100),
message text,
foreign key (SID) references Students(SID)
);

drop table if exists GymAdmin;
drop table if exists Students;
drop table if exists Notification;
drop table if exists localaction;
drop table if exists msgnotif;




