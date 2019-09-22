import sys
import os
import psycopg2

conn_string = "host='localhost' dbname='snps_nosql' user='postgres' password="
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()
for i in range(12):
    file_name = "/home/brunocarmonia/Documents/Unifesp/ICBD/IniciacaoCientifica/references/Oryza_sativa.IRGSP-1.0.dna_rm.chromosome." + str(i + 1) + ".fa"
    reference_id = "Oryza_sativa.IRGSP-1.0.dna_rm.all_chromosomes"
    with open(file_name, 'r') as reference_file:
        reference_file_lines = reference_file.readlines()
        for line in reference_file_lines:
            if line[0] == '>':
                #print(line)
                chromosome_description = line[1:]
                query = "INSERT INTO CHROMOSOME (id, reference_id, chromosome_description) VALUES ('%s','%s','%s') \n" % (str(i + 1), reference_id, chromosome_description)
                cursor.execute(query)
        conn.commit()
