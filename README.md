# Inspiration of TUMatcher

TUMatcher is a stock trading platform with some cool features built within 1 day
Here you will find more information about the platform, how to use, and what features you can expect to find.


## System Development (How we built it)

### 1. System Setup
We use the following:
1. Flask as the backend server
2. Material UI JS as frontend server
	- Non-blocking single and multi orders dispatch system
3. Python as the main language fullstack and JS for the frontend
4. MYSQL for database management fully integrated with backend and frontend via serialization pipelines
	- We used the hashtables to identify unique orders via manual seeds parsed from the requests payloads.
5. The initial backend prototype of the system is done entirely containerneized inside `main.py`. This file loads data from ``data/clients_requests.json`. It assumes batch processing by default.

### 2. Functional System Validation
- Requirements were given to us as SWE2 elements which from we derived SWE3. Those requirements were mentioned above in the features section.
- Based on SWE2 & SWE3 we developed our unit and integration test cases
- Covered boundry cases to increase robustness of the system
- We followed the smallest section of the V-Model to model our system for the given data, particularaly, the lower section:
![image-1.png](./resources/image-1.png)

You can find all the tests that we implemented and passed in:
`tumatcher/tests/tests.csv`

### 3. Installation and Running Instructions

#### 1. Clone our github repo
```bash
git clone https://github.com/davideandres95/tumatch.git
```

#### 2. Set up project environment via `venv`
```bash
python -m venv .
pip install -r requirements.txt
source bin/activate
```

#### 3. Start the main backend server and 
Please make sure you have `Flask` installed on your system that is 2.x.x. To install it.
Run the flask server:
```bash
python3 -m flask --app flaskr --debug run
```

#### 4. Populate the database with securities
Insert in the database
```
python3 symbols_parser.py
sqlite3 var/flaskr-instance/project.db < ./db_initialization/securities.sql
sqlite3 var/flaskr-instance/project.db < ./db_initialization/users.sql
sqlite3 var/flaskr-instance/project.db < ./db_initialization/orders.sql
```

#### 5. Start the back end and frontend servers
```bash
cd ./front/
npm install
npm start
```


#### 8. Test our Backend also with POSTMAN!
**load our config file into POSTMAN and thest the use cases**
```
./tumatch.postman_collection.json

```
There are initial use cases for creating orders, as well as checking for matches and verifying the functional requirements

#### 7. Visit the webapp
```
http://localhost:3000
```
Register with your name and password. ENJOY!

## Features (What it does)

We added the features based on the main requirements handed to us before dev, those were to provide mainly:
1. Add orders(handling duplicated orders and track history)
2. Delete(also handling duplications and invalid deletions of non-existent orders)
3. List orders(owned by used)
4. Matching History(All orders matched)

We treated those as SWE2 components, from which we derived SWE3(system detailed design), where we decided what will be our backend and what will be our frontend. And with more in depth design details that were discusesed amongst the team before the coding phase.

In parallel, we covered SWE5(Software Integration Test Specifications) which would help us cover the essential aspects of the system, more mentioned inthe system validation section.

### Accomplishments that we're proud of

In addition to the above features, we extended TUMatcher to have some extra feats:
1. History of executed commands on the system(records)
2. Batched Orders Processing in the database
3. Security tokens & web sockets to estables quick personal user profiles to cluster the orders by input
4. Mult-Client system as our backend accepts multiple requests simultaneously via authenticated web sockets
5. Non-blocking frontend order requests dispatch for single and batched orders
6. List logged date and time of the received orders and recorded as meta information for the user for entered orders
5. Market Stock Valuation via Moving Averages calculations(EMA, SMA)

### 1. Add Order to sell or buy a stock with choosen price
There is multiple options for the user to enter an order to TUMatcher:
1. via GUI:
	- You can input the orders via the webapp delivered as frontend of TUMatcher

### 2. Delete a sell or buy order of a stock
1. via GUI:
	- You can input the orders via the webapp delivered as frontend of TUMatcher


### 3. List orders you own on the platform

1. via GUI:
	- You can input the orders via the webapp delivered as frontend of TUMatcher


### 4. List the matching history of all completed orderes
1. via GUI:
	- You can input the orders via the webapp delivered as frontend of TUMatcher
	- For batch processing

### 5. Choosing Market Value of a Stock
We analyed state-of-the-art Stock Evalution tools in realtime markets. From which we found two essential indicators that can help identifying the market value of the stock:
1. Simple Moving Average(SMA) is used by professional platforms to evaluate the stock based on the fixed-time intervals e.g. daily averages between Open-High-Low-Close bounds that is collected over fixed time duration configured by the user(e.g. last 10 days, 20 days, etc).
	- **Pros**:
		- More stable than more sensitive trend indicators that give more weight to recent time price changes.
		- This could be more beneficial for well known stocks like `AAPL` or `NVDA` which are know to generally perform well on the long run.
		- Simpler to implement, even weight to all time steps
	- **Cons**:
		- Slower than other moving averages to indicate an early trend which can be missed early entrance
2. Exponential Moving Average(EMA) is similar to SMA with the main diff being adding more weight to the recent price changes of the stock rather than treating the whole price history of the stock as evenly contributing factors. EMA is giving more weight on the recent period to have a faster trend-convergence.
	- **Pros**:
		- Can be used to detect an early trend
	- **Cons**:
		- The indicating trend can be false trend. In this case, slower convergence to the trend like in SMA will give a better indication of how originally is the stock behaving.
		- More complicated than SMA

Our analysis and the boilerplate for our equations with some data tests are provided in the source file `resources/EMA - Analysis.csv`
> Implementation status: TBD
## Challenges we ran into
Coding an stock trading and exchange platform in almost 1 day is challenging.
Doing that in hackaTUM to to match the high expectations is even more challenging !! :)

We ran into many logistics challenges of the team. We had unstable internet connections on some floors, we didn't know most of the backend the first days where we had to bootstrap ourselves and get hooked with the simplest framework that is written in a language the team is comfortable with i.e. FLASK.

We came from different departments, different knowledge levels, and backgrounds. Integrating all of those with high intenstiy is no easy challenge.

## What we learned
- How to work as a team. Since every one worked on something and we had to to sync every 3 hours max due to the limited dev window.
- Learned different technologies that others in the team know i.e. Knowledge Sharing sessions took place to boostrap the rest of the team in intersting topic.
- Time management in short dev time.
- Applying some learned software decomposition techniques and development models like the V-Model on a lower scale gave us a better understanding of how to incorporate that in the future. 

## What's next for TUMatch
- We feel that our app still needs somework on different market indicators rendering to help the user learning more about the available stocks for trading.
- Extend the current functionality to include graphical plotting of the orders history
