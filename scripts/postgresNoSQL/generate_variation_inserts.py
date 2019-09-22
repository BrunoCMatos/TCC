import psycopg2

conn_string = "host='localhost' dbname='snps_nosql' user='postgres' password="
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()

query = "copy variation FROM '/home/brunocarmonia/Documents/Unifesp/ICBD/csv_files_postgresNoSQL/annotations_chrom_1.csv' DELIMITER ';' CSV QUOTE E'\\'';"
cursor.execute(query)
conn.commit()

query = "copy variation FROM '/home/brunocarmonia/Documents/Unifesp/ICBD/csv_files_postgresNoSQL/annotations_chrom_2.csv' DELIMITER ';' CSV QUOTE E'\\'';"
cursor.execute(query)
conn.commit()

query = "copy variation FROM '/home/brunocarmonia/Documents/Unifesp/ICBD/csv_files_postgresNoSQL/annotations_chrom_3.csv' DELIMITER ';' CSV QUOTE E'\\'';"
cursor.execute(query)
conn.commit()

query = "copy variation FROM '/home/brunocarmonia/Documents/Unifesp/ICBD/csv_files_postgresNoSQL/annotations_chrom_4.csv' DELIMITER ';' CSV QUOTE E'\\'';"
cursor.execute(query)
conn.commit()

query = "copy variation FROM '/home/brunocarmonia/Documents/Unifesp/ICBD/csv_files_postgresNoSQL/annotations_chrom_5.csv' DELIMITER ';' CSV QUOTE E'\\'';"
cursor.execute(query)
conn.commit()

query = "copy variation FROM '/home/brunocarmonia/Documents/Unifesp/ICBD/csv_files_postgresNoSQL/annotations_chrom_6.csv' DELIMITER ';' CSV QUOTE E'\\'';"
cursor.execute(query)
conn.commit()

query = "copy variation FROM '/home/brunocarmonia/Documents/Unifesp/ICBD/csv_files_postgresNoSQL/annotations_chrom_7.csv' DELIMITER ';' CSV QUOTE E'\\'';"
cursor.execute(query)
conn.commit()

query = "copy variation FROM '/home/brunocarmonia/Documents/Unifesp/ICBD/csv_files_postgresNoSQL/annotations_chrom_8.csv' DELIMITER ';' CSV QUOTE E'\\'';"
cursor.execute(query)
conn.commit()

query = "copy variation FROM '/home/brunocarmonia/Documents/Unifesp/ICBD/csv_files_postgresNoSQL/annotations_chrom_9.csv' DELIMITER ';' CSV QUOTE E'\\'';"
cursor.execute(query)
conn.commit()

query = "copy variation FROM '/home/brunocarmonia/Documents/Unifesp/ICBD/csv_files_postgresNoSQL/annotations_chrom_10.csv' DELIMITER ';' CSV QUOTE E'\\'';"
cursor.execute(query)
conn.commit()

query = "copy variation FROM '/home/brunocarmonia/Documents/Unifesp/ICBD/csv_files_postgresNoSQL/annotations_chrom_11.csv' DELIMITER ';' CSV QUOTE E'\\'';"
cursor.execute(query)
conn.commit()


query = "copy variation FROM '/home/brunocarmonia/Documents/Unifesp/ICBD/csv_files_postgresNoSQL/annotations_chrom_12.csv' DELIMITER ';' CSV QUOTE E'\\'';"
cursor.execute(query)
conn.commit()
