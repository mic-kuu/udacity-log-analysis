# Project3: mic-kuu's log analysis
This project is a result of Udcaity's Fullstack Developer Nanodegree assginment. It's a simple python script that gathers data from a server database and presents the output in the command line.

## Overview
The script is written in python 3. It uses psycopg2 library to connect to a website's database and answers 3 diagnostic questions about the website:
1. What are the most popular three articles of all time? 
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

For simplicty the script uses views that need to be defined on the database. The views are described in the views section.

Below you can find result of running the script on the project's database: 
```
 --------------------------------------------------------------------------------
|  1: The most popular three articles of all time
 --------------------------------------------------------------------------------

 [ 1 ]  "Candidate is jerk, alleges rival"              338647 views
 [ 2 ]  "Bears love berries, alleges bear"              253801 views
 [ 3 ]  "Bad things gone, say good people"              170098 views

 --------------------------------------------------------------------------------
|  2: The most popular article authors of all time
 --------------------------------------------------------------------------------

 [ 1 ]  "Ursula La Multa"                               507594 views
 [ 2 ]  "Rudolf von Treppenwitz"                        423457 views
 [ 3 ]  "Anonymous Contributor"                         170098 views
 [ 4 ]  "Markoff Chaney"                                84557 views

 --------------------------------------------------------------------------------
|  3: Days on which more than 1% of requests lead to errors
 --------------------------------------------------------------------------------

 [ 1 ]  2016-07-17                                      2.26%
```

## How to use
First you need to add 3 views running commands described in the views section. For simplicty, I've prepared the `views.sql` that will add all 3 of my views to your db. To do that execute them like that:
```bash
psql -d news -f views.sql
```
After that you simply need to make the `db_stats.py` executable by:
```bash
chmod +x db_stats.py
```
and then execute it like:
```bash
./db_stats.py
```
Alternatively just run it using python3 interpreter explicitly:
```bash
python3 db_stats.py
```

## Views
Simply copy and execute those sql views into your database. After all 3 of them are added the log script will execute correctly. Alternatively use the `views.sql` according to the instructions in the 'how to use' section.
### top_articles
```sql
create view top_articles as
select  articles.title,
        top_endpoints.views_sum
from articles
inner join
(
  select distinct path,
  count(path) as views_sum
  from log
  group by path
  order by views_sum desc
) top_endpoints
  on top_endpoints.path like concat('%', articles.slug)
limit 3;
```
### top_authors
```sql
create view top_authors as
select  authors.name,
        sum(articles_views.views_sum) as views_total
from authors
inner join
(
  select  articles.author as author_id,
          top_endpoints.views_sum
  from articles
  inner join
  (
    select distinct path,
                    count(path) as views_sum
    from log
    group by path
    order by views_sum desc
  ) top_endpoints
    on top_endpoints.path like concat('%', articles.slug)
) articles_views
  on articles_views.author_id = authors.id
group by authors.name
order by views_total
desc;
```
### request_stats
```sql
create view request_stats as
select  day,
        (error_sum::decimal / request_sum::decimal) as failure_ratio
from 
(
  select  time::date as day,
          count(*) as request_sum,
          sum (case when status != '200 OK' then 1 else 0 end) as error_sum
  from log
  group by day
) daily_stats
where (error_sum::decimal / request_sum::decimal) > 0.01;
```
## Contributions
Special thanks to:
* [psycopg](http://initd.org/psycopg/)


## License
![Creative Commons License](https://i.creativecommons.org/l/by/4.0/88x31.png) 
This work is licensed under a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/)
