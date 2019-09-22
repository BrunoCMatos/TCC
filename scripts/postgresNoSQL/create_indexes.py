import psycopg2

conn_string = "host='localhost' dbname='snps_nosql' user='postgres' password="
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()

query = "create index snp_annotation_index ON variation USING GIN((snp_annotation));"
cursor.execute(query)
conn.commit()
query = "create index only_annotation_index ON variation USING GIN((snp_annotation->'annotations'));"
cursor.execute(query)
conn.commit()
query = "create index only_variation_identification_index ON variation USING GIN((snp_annotation->'variation_identification'));"
cursor.execute(query)
conn.commit()
query = "create index only_pos_index ON variation USING GIN((snp_annotation->'pos'));"
cursor.execute(query)
conn.commit()

