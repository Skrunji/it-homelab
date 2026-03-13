# Day-02

I started off by trying to install MySQL with winget. MySQL.MySQL didn't work so I used winget search MySQL which returned lots of related results. I went with the Oracle.MySQL package.

It didn't install properly so I downloaded the installer directly from the Oracle website and installed MySQLWorkbench as well. I downloaded sakila DB to work as well. Once I got those all installed I started exploring the DB and writing some basic queries to see what was in the tables. The sakila DB contains data for a blockbuster era movie rental store. Then I posed a challenge to myself, which actor appeared in the most films?

I struggled with writing the correct query. it took many attempts but I eventually got it. 

```sql
USE sakila;

SELECT COUNT(film_actor.actor_id) AS 'Movies per Actor', CONCAT (actor.first_name, ' ', actor.last_name) AS 'Name'
FROM sakila.film_actor
INNER JOIN sakila.actor ON actor.actor_id = film_actor.actor_id
GROUP BY actor.actor_id, actor.first_name, actor.last_name
ORDER BY COUNT(actor.actor_id) DESC;
```
I then exported it to a CSV. That's all for today! I feel pretty good about today.