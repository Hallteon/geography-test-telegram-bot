import psycopg2
from data import config

connect = psycopg2.connect(config.DB_URI, sslmode="require")
cursor = connect.cursor()
