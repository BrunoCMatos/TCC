import psycopg2

conn_string = "host='localhost' dbname='snps' user='postgres' password="
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()

query = "copy CHROMOSOME_VARIATION_ANNOTATION (chromosome_id, biologic_annotation_id, variation_id) FROM '/home/brunocarmonia/Documents/Unifesp/ICBD/csv_files_postgresSQL/chromosome_variation_annotation.csv' DELIMITER ',' CSV;"
cursor.execute(query)
conn.commit()
