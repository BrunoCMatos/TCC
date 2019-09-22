import psycopg2

conn_string = "host='localhost' dbname='snps' user='postgres' password="
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()

query = "CREATE INDEX variation_identification_index ON variation (variation_identification);"
cursor.execute(query)
conn.commit()
query = "CREATE INDEX pos_index ON variation (pos);"
cursor.execute(query)
conn.commit()
query = "CREATE INDEX chromosome_variation_annotation_index ON chromosome_variation_annotation (chromosome_id, biologic_annotation_id, variation_id);"
cursor.execute(query)
conn.commit()
query = "CREATE INDEX biologic_annotation_index ON biologic_annotation (annotation);"
cursor.execute(query)
conn.commit()

