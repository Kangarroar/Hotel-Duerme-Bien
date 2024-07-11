# utils/database.py
import mysql.connector
from utils.terminal import *
conexion = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="hotel"
)

cursor = conexion.cursor()

