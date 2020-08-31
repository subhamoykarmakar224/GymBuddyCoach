describe students;


describe notification;

describe gymadmin;
select * from gymadmin;
-- insert into gymadmin values("BodyShapers-9876", "Body Shapers Gymnasium", "Kanchan Basu", "9432743720", "31-12-2020", "kbasu", SHA1("1234"), "0");
-- delete from gymadmin where loginstatus="0";

delete from gymadmin;

SET SQL_SAFE_UPDATES = 0;
select gymId, gymName, adminName, username from GymAdmin where phone='+919876543210';

select * from gymadmin;
select * from localaction;
select * from notification order by datestamp, timestmp desc;
select * from softwareflags;
select * from students;
select * from msgnotif;
select * from CustomMessage;

insert into CustomMessage values("msg1", "This is a test message for msg1");
insert into CustomMessage values("msg2", "This is a test message for msg2");
insert into CustomMessage values("msg3", "This is a test message for msg3");

select * from CustomMessage;
select * from msgnotif order by msgcounter desc limit 1;
delete from msgnotif where msgcounter=39;

-- notifId varchar(100) primary key,
-- studentId varchar(100), 
-- stamp varchar(100),
-- datestamp date,
-- timeStmp time,
-- level varchar(10),
-- msg text

insert into notification values(
"N003", 
"ID-2932-2", 
"Tue Aug 25 08:16:38 GMT+05:30 2020", 
STR_TO_DATE("25-08-2020", '%d-%m-%Y'), 
"08:16:38", 
"RED", 
"Student tried to access when not alloted."
);

select studentname from Students where SID="ID-2932-1";
select *from students;

select count(*) from notification;
select *from notification where datestamp = curdate() and timeStmp <= TIME('17:00:00') and level=upper('red');
select *from notification where datestamp < now() - interval 20 DAY;

select *from Attendence;
select *from Attendence where datestamp='2020-08-22';
update Attendence set uploadstatus="0" where uploadstatus="1";
select distinct SID from Attendence where uploadstatus="0";

select * from Attendence 
where SID="ID-2932-7e24dabd" 
and datestamp >= STR_TO_DATE("2020-08-01", "%d-%m-%Y") 
and datestamp <= STR_TO_DATE("2020-08-31", "%d-%m-%Y");

select * from Attendence 
where SID="ID-2932-7e24dabd" 
and datestamp like "2020-08-%" order by datestamp asc;


delete from attendence where datestamp="2020-08-27";

delete from Attendence;
delete from notification;
delete from students;
delete from msgnotif;

update softwareflags set status=0 where flagname="firstinstallstudent";