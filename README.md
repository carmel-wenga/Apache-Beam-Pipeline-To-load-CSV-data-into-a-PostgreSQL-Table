## What is this sample beam pipeline about ?
This sample project aims at loading data from a csv file into a PostgreSQL 
database.

The project structure is the following
```
├── database
│   ├── Dockerfile
│   └── init.sql
├── pipeline.py
├── README.md
├── requirements.txt
└── source
    └── salaries_data.csv
```

The data that will be loaded into the postgres database are in the 
```source/salaries_data.csv``` file. I downloaded the salary data from
[kaggle](https://www.kaggle.com/datasets/mohithsairamreddy/salary-data).
This dataset contains salary data based on experience, age, gender, function and
level of education. You can also use other data in csv format.

The ***apache beam*** pipeline itself is defined by the ```pipeline.py``` file, 
which reads the csv file and loads its contents into a postgres table.

Finally, the postgres database is defined with a Dockerfile 
(```database/Dockerfile```). The ``init.sql`` file creates the ``salaries`` 
table in the database at startup.


## Create Virtual Environment
```commandline
python3.10 -m venv .env
```

## Install Requirements

The main requirements are the following:
* ```apache-beam==2.52.0```
* ```beam-postgres-connector==0.1.3```
* ```psycopg2-binary==2.9.9```

The ```requirements.txt``` file contain the complete list of requirements
for this sample project.

```commandline
source .env/bin/activate && pip install -r requirements.txt
```

## Build and Run the database container

```commandline
cd database && docker build -t pipelinedb .
```
Run the ```pipelinedb``` container with the command below
```commandline
docker run -it -p 5432:5432 --name pipelinedb --env-file .env pipelinedb
```
The ```.env``` file contain environment variables (DB, USER, PASSWORD) useful for 
the postgres container. Note that the ```.env``` is not versioned in the repository.
Go to the database folder and run the following command to create the .env file

```commandline
cat <<EOF >> brightup.sh
POSTGRES_DB=beamdb
POSTGRES_USER=beamdb
POSTGRES_PASSWORD=ra5hoxetRami5
EOF
```

The postgres database will be accessible from localhost with the following uri
```postgres://localhost:5432/beamdb```

## Run the pipeline

Go back in the project's root directory and run the beam pipeline with the 
following command

```commandline
python pipeline.py --input source/salaries_data.csv --dbhost localhost --dbport 5432
```

## Output

After running the pipeline, salary data must be loaded into the ``salaries`` 
table in the postgres database.

To inspect your database, run the commands below

1. Connect to the container
```commandline
docker exec -it pipelinedb bash
```
2. Connect to the database
```commandline
psql -U beamdb -d beamdb
```
3. Run the query below to check that the data has been loaded into the 
```salaries``` table
```sql
select * from salaries;
```
The result of the above query should look something like the following
```
 age | gender | education_level |               job_title               | year_of_experience | salary 
-----+--------+-----------------+---------------------------------------+--------------------+--------
  32 | Male   | Bachelor        | Software Engineer                     |                  5 |  90000
  28 | Female | Master          | Data Analyst                          |                  3 |  65000
  45 | Male   | PhD             | Senior Manager                        |                 15 | 150000
  36 | Female | Bachelor        | Sales Associate                       |                  7 |  60000
  52 | Male   | Master          | Director                              |                 20 | 200000
  29 | Male   | Bachelor        | Marketing Analyst                     |                  2 |  55000
  42 | Female | Master          | Product Manager                       |                 12 | 120000
  31 | Male   | Bachelor        | Sales Manager                         |                  4 |  80000
  26 | Female | Bachelor        | Marketing Coordinator                 |                  1 |  45000
  38 | Male   | PhD             | Senior Scientist                      |                 10 | 110000
  29 | Male   | Master          | Software Developer                    |                  3 |  75000
```






