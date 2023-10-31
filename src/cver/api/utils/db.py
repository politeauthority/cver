"""Utils - DB
Database handler.

"""
import logging
import os

import pymysql.cursors
import mysql.connector
from mysql.connector import Error as MySqlError

from cver.api.utils import glow

DB_HOST = os.environ.get("CVER_DB_HOST")
DB_PORT = int(os.environ.get("CVER_DB_PORT"))
DB_NAME = os.environ.get("CVER_DB_NAME")
DB_USER = os.environ.get("CVER_DB_USER")
DB_PASS = os.environ.get("CVER_DB_PASS")


def connect():
    # Connect to the database
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME)
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


def connect_no_db(server: dict):
    """Connect to MySql server, without specifying a database, and get a cursor object."""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS)
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
    sql = """CREATE DATABASE IF NOT EXISTS %s; """ % DB_NAME
    cursor.execute(sql)
    logging.debug('Created database: %s' % DB_NAME)
    return True


def close() -> bool:
    """Close the MySQL connection."""
    if isinstance(glow.db["conn"], str):
        logging.error("Canot close database connection, it doesnt exist.")
        return False
    glow.db["conn"].close()
    return True

# End File: cver/src/api/utils/db.py
