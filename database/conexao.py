
import mysql.connector

from database.config import DB_CONFIG


def conectar():
    return mysql.connector.connect(**DB_CONFIG)