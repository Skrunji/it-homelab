import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine

load_dotenv()


def get_connection():
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    database = os.getenv("DB_NAME")
    return create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")
st.title("Sakila Video Rental Dashboard")

st.header("Most Popular Genres")

if st.button("Run Report"):
    conn = get_connection()
    
    query = """
        SELECT c.name AS Genre, COUNT(r.rental_id) AS Total_Rentals
        FROM rental r
        JOIN inventory i ON r.inventory_id = i.inventory_id
        JOIN film f ON i.film_id = f.film_id
        JOIN film_category fc ON f.film_id = fc.film_id
        JOIN category c ON fc.category_id = c.category_id
        GROUP BY c.name
        ORDER BY Total_Rentals DESC
    """
    
    df = pd.read_sql(query, conn)
    st.dataframe(df)

st.header("Overdue Rentals")

if st.button("Show Overdue Rentals"):
    conn = get_connection()
    
    query = """
        SELECT r.rental_id, c.first_name, c.last_name, f.title, DATE_ADD(r.rental_date, INTERVAL f.rental_duration DAY) AS Due_Date
        FROM rental r
        JOIN customer c ON r.customer_id = c.customer_id
        JOIN inventory i ON r.inventory_id = i.inventory_id
        JOIN film f ON i.film_id = f.film_id
        WHERE DATE_ADD(r.rental_date, INTERVAL f.rental_duration DAY) < '2005-09-01' AND r.return_date IS NULL
    """
    
    df_overdue = pd.read_sql(query, conn)
    st.dataframe(df_overdue)

st.header("Top Customers by Rental Count")

if st.button("Show Top Customers"):
    conn = get_connection()
        
    query = """
         SELECT c.first_name, c.last_name, COUNT(r.rental_id) AS Total_Rentals
        FROM rental r
        JOIN customer c ON r.customer_id = c.customer_id
        GROUP BY c.customer_id
        ORDER BY Total_Rentals DESC
        LIMIT 10
        """
        
    df_top_customers = pd.read_sql(query, conn)
    st.dataframe(df_top_customers)