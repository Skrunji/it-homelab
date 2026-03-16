import mysql.connector
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

connection = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

query = """
    SELECT COUNT(film_actor.actor_id) AS 'Movies per Actor',
           CONCAT(actor.first_name, ' ', actor.last_name) AS 'Name'
    FROM sakila.film_actor
    INNER JOIN sakila.actor ON actor.actor_id = film_actor.actor_id
    GROUP BY actor.actor_id, actor.first_name, actor.last_name
    ORDER BY COUNT(actor.actor_id) DESC
"""

df = pd.read_sql(query, connection)
print(df)

df.to_csv('movies_per_actor.csv', index=False)

connection.close()