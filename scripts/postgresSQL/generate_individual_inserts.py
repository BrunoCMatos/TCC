import psycopg2

conn_string = "host='localhost' dbname='snps' user='postgres' password="
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()

query = "copy individual FROM '/home/brunocarmonia/Documents/Unifesp/ICBD/csv_files_postgresSQL/inserts_individual.csv' DELIMITER ',' CSV;"
cursor.execute(query)
conn.commit()
