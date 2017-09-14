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
