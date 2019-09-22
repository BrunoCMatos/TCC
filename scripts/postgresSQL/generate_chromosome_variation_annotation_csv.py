import sys
import os
import psycopg2

inserts = {}

conn_string = "host='localhost' dbname='snps' user='postgres' password="
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()
cursor2 = conn.cursor()

csv_file = open("/home/brunocarmonia/Documents/Unifesp/ICBD/csv_files_postgresSQL/chromosome_variation_annotation.csv", "w")
query = "select id, chrom, pos from variation ORDER BY chrom"
cursor2.execute(query)
variations = cursor2.fetchmany(70000)
while (len(variations) > 0):
    print(len(variations))
    for variation in variations:
        query = "select * from BIOLOGIC_ANNOTATION WHERE starting_position <= '%s' AND ending_position >= '%s' AND chrom = '%s'" % (variation[2], variation[2], variation[1])
        cursor.execute(query)
        biologic_annotations = cursor.fetchmany(10000)
        has_annotation = False
        while (len(biologic_annotations) > 0):
            has_annotation = True
            for biologic_annotation in biologic_annotations:
                line = str(variation[1]) + "," + str(biologic_annotation[0]) + "," + str(variation[0]) + "\n"
                csv_file.write(line)
            biologic_annotations = cursor.fetchmany(10000)
        if not has_annotation:
            #relate to annotation saved as intron
            line = str(variation[1]) + "," + "1" + "," + str(variation[0]) + "\n"
            csv_file.write(line)
    variations = cursor2.fetchmany(70000)
