# tumatcher


# Requirements

- [ ] Add Order
- [ ] Delete Order
- [ ] List owned orders
- [ ] list match history

## List of tables

- Users: UUID, NAME
- Orders: UUID, USER, SIDE, SEQ, QTY
- Matches: UUID, SELL_ORDER_ID, BUY_ORDER_ID, SECURITY, QTY
- Sequrities UUID, NAME
- LOG: UUID, USER_ID, SIED, SEQ, QTY


## Add order

- Input data:
	- request (add)
	- quantity [INTEGER]
	- security name (e.g. IBM,JNPR, ...)
	- side ( BUY/SELL)
	- user name
- Response data
	- status (OK, REJECTED)
	- message (optional)

### Comments/Discussion
- If a user sends an update request, the entry with matching hash will be updated.
- All requests are logged into the order log table

## Delete order

- Input data:
	- request (del)
	- quantity [INTEGER]
	- security name (e.g. IBM,JNPR, ...)
	- side ( BUY/SELL)
	- user name
- Response data
	- status (OK, REJECTED)
	- message (optional)


## List owned orders

- Input data:
	- request (list_orders)
	- user name

- Response data:
	- List of owned orders


## List matched orders

- Input data:
	- request (list_matches)
	- user name

- Response data:
	- List of matched orders


# Commands for running

## set up env
```
python -m venv .
pip install -r requirements.txt
source bin/activate
```

## run flask app
```
flask --app flaskr --debug run
```

# populate db with securities
```
python3 symbols_parser.py
cd var/flaskr-instance
sqlite3 project.db
.read ../../securities.sql
```
