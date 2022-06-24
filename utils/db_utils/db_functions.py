import psycopg2
from .connect_db import connect, cursor
from ..misc.continents_data import data_continents

continent_names = list(data_continents.keys())

continents_convert = {
    continent_names[0]: "europe",
    continent_names[1]: "asia",
    continent_names[2]: "africa",
    continent_names[3]: "america",
    continent_names[4]: "australia"
}


async def create_table():
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL NOT NULL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    europe SMALLINT NOT NULL,
    asia SMALLINT NOT NULL,
    america SMALLINT NOT NULL,
    africa SMALLINT NOT NULL,
    australia SMALLINT NOT NULL)""")

    connect.commit()


async def create_user_record(user_id, user_name):
    cursor.execute(f"""INSERT INTO users VALUES ({user_id}, '{user_name}', {0}, {0}, {0}, {0}, {0}) ON CONFLICT DO NOTHING""")
    connect.commit()


async def set_max_continent_points(user_id, continent, points):
    cursor.execute(f"""SELECT {continents_convert[continent]} FROM users WHERE id = {user_id};""")

    if points > cursor.fetchone()[0]:
        cursor.execute(f"""UPDATE users SET {continents_convert[continent]} = {points} WHERE id = {user_id};""")
        connect.commit()


async def disconnect_db():
    connect.close()