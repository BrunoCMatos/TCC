import psycopg2

conn_string = "host='localhost' dbname='snps_nosql' user='postgres' password="
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()

query = "copy individual FROM '/home/brunocarmonia/Documents/Unifesp/ICBD/csv_files_postgresNoSQL/inserts_individual.csv' DELIMITER ',' CSV;"
cursor.execute(query)
conn.commit()
