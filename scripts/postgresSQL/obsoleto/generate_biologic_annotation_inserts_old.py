import sys
import os
import psycopg2

conn_string = "host='localhost' dbname='snps' user='postgres' password="
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()

for i in range(1, 2):

    inserts = {}

    file_name = "/home/bruno/Documents/Unifesp/ICBD/IniciacaoCientifica/references/Oryza_sativa.IRGSP-1.0.40.chromosome." + str(i) + ".gff3"

    with open(file_name, 'r') as reference_file:
        gff3_file_lines = reference_file.readlines()


        for line in gff3_file_lines:

            if line[0] == '#': continue

            line_fields = line.split('\t')

            inserts[file_name] = []
            inserts[file_name].append(int(line_fields[3]))
            inserts[file_name].append(int(line_fields[4]))
            inserts[file_name].append(line_fields[2])

            for insert in inserts.keys():
                query = "INSERT INTO BIOLOGIC_ANNOTATION (chrom, starting_position, ending_position, annotation) VALUES ('%d','%d','%d', '%s') \n" % (i, inserts[insert][0], inserts[insert][1], inserts[insert][2])
                cursor.execute(query)
                conn.commit()
