BEGIN TRANSACTION;
insert into order (side, user_id, security_id, price, quantity,) values ('sell', 3, 22, 2, 1000);
insert into order (side, user_id, security_id, price, quantity,) values ('sell', 2, 22, 5, 1000);
COMMIT;
