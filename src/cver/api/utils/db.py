"""Utils - DB
Database handler.

"""
import logging

import pymysql.cursors
import mysql.connector
from mysql.connector import Error as MySqlError

from cver.api.utils import glow


def connect():
    # Connect to the database
    try:
        connection = pymysql.connect(
            host=glow.db["HOST"],
            port=glow.db["PORT"],
            user=glow.db["USER"],
            password=glow.db["PASS"],
            database=glow.db["NAME"])
    except pymysql.err.OperationalError as e:
        message = "An error occurred while connecting to the MySQL server: %s" % e
        logging.critical(message)
        raise RuntimeError

    logging.info("Generating database connection")
    glow.db["conn"] = connection
    glow.db["cursor"] = connection.cursor()
    return {
        "conn": connection,
        "cursor": connection.cursor()
    }


def connect_no_db():
    """Connect to MySql server, without specifying a database, and get a cursor object."""
    try:
        connection = mysql.connector.connect(
            host=glow.db["HOST"],
            user=glow.db["USER"],
            port=glow.db["PORT"],
            password=glow.db["PASS"])
        if connection.is_connected():
            connection.get_server_info()
            cursor = connection.cursor()
            cursor.execute("select database();")
            cursor.fetchone()
        return (connection, cursor)
    except MySqlError as e:
        print("Error while connecting to MySQL: %s" % e)
        exit(1)


def create_mysql_database(conn, cursor):
    """Create the MySQL database."""
    sql = """CREATE DATABASE IF NOT EXISTS %s; """ % glow.db["NAME"]
    cursor.execute(sql)
    logging.debug('Created database: %s' % glow.db["NAME"])
    return True


def close() -> bool:
    """Close the MySQL connection."""
    if isinstance(glow.db["conn"], str):
        logging.error("Canot close database connection, it doesnt exist.")
        return False
    glow.db["conn"].close()
    return True

# End File: cver/src/api/utils/db.py
