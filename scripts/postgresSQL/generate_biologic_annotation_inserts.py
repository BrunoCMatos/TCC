import sys
import os
import psycopg2

conn_string = "host='localhost' dbname='snps' user='postgres' password="
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()

file_name = "/home/brunocarmonia/Documents/Unifesp/ICBD/IniciacaoCientifica/references/all.locus_brief_info.7.0"

with open(file_name, 'r') as file:
    annotation_info = file.readlines()[1:]
    query = "INSERT INTO BIOLOGIC_ANNOTATION (chrom, starting_position, ending_position, annotation) VALUES ('%d','%d','%d', '%s') \n" % (
    0, 0, 0, 'intron')
    cursor.execute(query)
    for line in annotation_info:
        line_fields = line.split('\t')
        chrom = line_fields[0].split('r')[1]
        if chrom.isdigit():
            chrom = int(line_fields[0].split('r')[1])
        else:
            break
#        print(chrom)
        start_position = int(line_fields[3])
        end_position = int(line_fields[4])
        annotation = line_fields[9]
        if (len(annotation.split("'")) > 0) :
            annotation_aux = annotation.split("'")
            annotation = ""
            for x in annotation_aux:
                annotation += x
            query = "INSERT INTO BIOLOGIC_ANNOTATION (chrom, starting_position, ending_position, annotation) VALUES ('%d','%d','%d', '%s') \n" % (chrom, start_position, end_position, annotation)
            cursor.execute(query)
    conn.commit()
