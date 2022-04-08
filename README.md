# Blue Onion Labs Take Home Test Completed

This is the solution to the [Blue Onion Labs Take Home Test](https://github.com/BlueOnionLabs/api-spacex-backend). It has been solved in the easiest and faster way I could think and not necessarily as it would be done for production environment applications. At least, I think this is the spirit of the exercise after reading sentences such as the ones I quote below:

> Don't hesitate to use any tools/tricks you know to load data quickly and easily!

And

> No need to derive any fancy match for distances (...)

```
Some practices like avoing hardcoding credentials, modularity, or adding unit tests
are ignored to keep it simple and easier to read.
```

# The Problem:

We want to achieve a few goals:
  - To import the SpaceX Satellite data _as a time series_ into a database
  - To be able to query the data to determine the last known latitude/longitude of the satellite for a given time

# The Task (Part 1):

Stand up your favorite kind of database (and ideally it would be in a form that would be runnable by us, via something like docker-compose).

## Solution:

I have completed the task using Postgres, to run it you can use `docker-compose` (as requested)

```
docker-compose up -d
```

# The Task (Part 2):

Write a script (in whatever language that you prefer, though Ruby, Python, or Javascript would be ideal for us) to import the relevant fields in starlink_historical_data.json as a time series. The relevant fields are:

    - spaceTrack.creation_date (represents the time that the lat/lon records were recorded)
    - longitude
    - latitude
    - id (this is the starlink satellite id)

Again, the goal is that we want to be able to query the database for the last known position for a given starlink satellite.

Don't hesitate to use any tools/tricks you know to load data quickly and easily!

## Solution:

This is the process I followed to complete this task:

1. I created a small script called `json2csv.py` which selects the important fields and creates a CSV file.
2. Then, using [this tool](https://www.convertcsv.com/csv-to-sql.htm) I converted the CSV file into SQL and took only the `INSERT`s (since the tool generates the SQL for MySQL and the `CREATE TABLE` is formatted differently in Postgres) and saved them in a `data/init.sql` file.
3. Afterward, I manually wrote the commands to create the table and the indexes.
4. Finally, I configured the `docker-compose.yml` file to automatically import the `init.sql` file.

**Note:** It would also have been possible to import the CSV file in a Python script using the method indicated on [this web page](https://www.geeksforgeeks.org/python-import-csv-into-postgresql/), but I preferred to do it this way because it is a simple method and does not require an additional execution of the script each time the container is started nor the creation of a volume to persist the data.

# The Task (Part 3):

Write a query to fetch the last known position of a satellite (by id), given a time T. Include this query in your README or somewhere in the project submission.

## Solution:

```sql
SELECT longitude, latitude
FROM starlink_historical_data
WHERE id='60106f20e900d60006e32cc4'
ORDER BY creation_date
DESC LIMIT 1;
```

Replace `60106f20e900d60006e32cc4` for the ID of the desired satellite.

# Bonus Task (Part 4):

Write some logic (via a combination of query + application logic, most likely) to fetch from the database the _closest_ satellite at a given time T, and a given a position on a globe as a (latitude, longitude) coordinate.

No need to derive any fancy match for distances for a point on the globe to a position above the earth. You can just use the Haversine formula. Example libraries to help here:

For Python: https://github.com/mapado/haversine

For Ruby: https://github.com/kristianmandrup/haversine

## Solution:

Completed! To test the app: 

1. Create a virtual environment.
2. Active the virtual environment.
3. Install the dependencies.
4. Run the database container.
5. Run the program `bonus.py` and follow the instructions: 

```
python -m venv venv
source venv/bin/activate # for linux
pip install -r requirements.txt
docker-compose up -d
python bonus.py
# follow the instructions
```

Note: If something is not working, check the OS and Python version. I'd expect it to work on Windows, Linux and Mac with any Python version `>=3.6`, but it has been tested only on `Ubuntu 20.04` with `Python 3.10`, so prefer this OS and version combo if possible.
