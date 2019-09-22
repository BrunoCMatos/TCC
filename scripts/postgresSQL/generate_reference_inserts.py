import sys
import os
import psycopg2

conn_string = "host='localhost' dbname='snps' user='postgres' password="
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()

for i in range(1):

    inserts = {}
    dir_path = "/home/bruno/Documents/Unifesp/ICBD/IniciacaoCientifica/references/"
    file_name = "Oryza_sativa.IRGSP-1.0.dna_rm.all_chromosomes" # deixar genérico
    reference_id = file_name
    associated_paper = "none"
    query = """INSERT INTO REFERENCE VALUES (%s,%s,%s);"""
    cursor.execute(query, (file_name, dir_path, associated_paper,))
    conn.commit()
