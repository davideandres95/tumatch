BEGIN TRANSACTION;
insert into user (name, password) values ('Cristian', 'sha256$ecd71870d1963316a97e3ac3408c9835ad8cf0f3c1bc703527c30265534f75ae');
insert into user (name, password) values ('Omar', 'sha256$ecd71870d1963316a97e3ac3408c9835ad8cf0f3c1bc703527c30265534f75ae');
COMMIT;
