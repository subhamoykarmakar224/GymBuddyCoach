describe students;
select * from students;

describe notification;

describe gymadmin;
select * from gymadmin;
-- insert into gymadmin values("BodyShapers-9876", "Body Shapers Gymnasium", "Kanchan Basu", "9432743720", "31-12-2020", "kbasu", SHA1("1234"), "0");
-- delete from gymadmin where loginstatus="0";

delete from gymadmin;

SET SQL_SAFE_UPDATES = 0;
select gymId, gymName, adminName, username from GymAdmin where phone='+919876543210';

select * from softwareflags;

delete from softwareflags;