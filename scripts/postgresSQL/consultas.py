import sys
import os
import psycopg2
import numpy

def time(text):
    splited_text = text.split(':')
    time = float(splited_text[1][1:-3]) #remove characters
    return time

def start_up():
    conn_string = "host='localhost' dbname='snps' user='postgres' password="
    conn = psycopg2.connect(conn_string)
    return conn.cursor()

#1
def snps_in_a_experiment(population_id, reference_id):
    cursor = start_up()

    print("Consulta 1")

    query_chromosome = "SELECT c.id, c.chromosome_description FROM chromosome c WHERE c.reference_id = '%s'" % reference_id
    cursor.execute(query_chromosome)
    chromosome_results = cursor.fetchall()
    cursor.execute(cursor.mogrify('explain analyze ' + query_chromosome))
    analyze_result = cursor.fetchall()
    sum = 0
    sum += time(analyze_result[-1][0])
    number_of_snps = 0
    for chromosome in chromosome_results:
        query_snps = "SELECT DISTINCT v.variation_identification FROM variation v, chromosome_variation_annotation cva WHERE v.id = cva.variation_id AND cva.chromosome_id = '%s' AND v.population_id = '%s'" % (chromosome[0], population_id)
        cursor.execute(cursor.mogrify('explain analyze ' + query_snps))
        analyze_result = cursor.fetchall()
        sum += time(analyze_result[-1][0])
        cursor.execute(query_snps)
        number_of_snps += len(cursor.fetchall())

    print("Total execution time: %.2f" % sum)
    print(number_of_snps)

#2
def get_all_snps_of_a_chromosome(chromosome_id):
    print("Consulta 2")

    cursor = start_up()
    query = " SELECT DISTINCT v.variation_identification FROM variation v, chromosome_variation_annotation cva, chromosome c WHERE (v.id = cva.variation_id AND cva.chromosome_id = c.id AND c.id = '%s')" % (chromosome_id)

    cursor.execute(cursor.mogrify('explain analyze ' + query))
    analyze_result = cursor.fetchall()

    print(analyze_result[-1][0])

    cursor.execute(query)
    print(len(cursor.fetchall()))


#3
def get_annotations_of_a_population(population_id):
    print("Consulta 3")
    query = "SELECT  (ba.annotation) FROM biologic_annotation ba, variation v, chromosome_variation_annotation cva WHERE ba.id = cva.biologic_annotation_id AND cva.variation_id = v.id AND v.population_id = '%s'" % population_id
    cursor = start_up()
    cursor.execute(cursor.mogrify('explain analyse ' + query))
    analyze_result = cursor.fetchall()
    sum = time(analyze_result[-1][0])

    print("Total execution time: %.2f" % sum)

    cursor.execute(query)
    print(len(cursor.fetchall()))


#4
def variation_related_to_biologic_annotation_and_individuals_related_to_them(biologic_annotation):
    print("Consulta 4")
    cursor = start_up()
    cursor2 = start_up()
    sum = 0
    query = "SELECT DISTINCT v.variation_identification, v.population_id FROM variation v, chromosome_variation_annotation cva, biologic_annotation ba WHERE ba.annotation = '" + biologic_annotation + "\n' AND v.id = cva.variation_id AND cva.biologic_annotation_id = ba.id"
    cursor.execute(cursor.mogrify('explain analyze ' + query))
    analyze_result = cursor.fetchall()
    sum += time(analyze_result[-1][0])

    print("Total execution time: %.2f" % sum)

    cursor.execute(query)
    results = cursor.fetchall()
    population_ids = set([result[1] for result in results])
    print(len(results))
    individual_query = "SELECT i.id, i.individual_identification FROM individual i, population p WHERE i.population_id = p.id AND p.id in %s" % (str(population_ids).replace('{', '(').replace('}', ')'))
    cursor2.execute(cursor.mogrify('explain analyze ' + individual_query))
    analyze_result = cursor2.fetchall()
    sum += time(analyze_result[-1][0])

    print("Total execution time: %.2f" % sum)

    cursor2.execute(query)
    print(len(cursor2.fetchall()))

#5
def get_annotations_related_to_variation(variation_identification):
    print("Consulta 5")
    cursor = start_up()
    query = "SELECT DISTINCT ba.annotation FROM biologic_annotation ba, chromosome_variation_annotation cva, variation v WHERE ba.id = cva.biologic_annotation_id AND cva.variation_id = v.id AND v.variation_identification = '%s'" % variation_identification
    cursor.execute(cursor.mogrify('explain analyse ' + query))
    analyze_result = cursor.fetchall()
    sum = time(analyze_result[-1][0])

    print("Total execution time: %.2f" % sum)

    cursor.execute(query)
    print(cursor.fetchall())

#6 remove
def get_reference_of_individual(individual_identification):
    print("Consulta 6")
    cursor = start_up()
    query = "SELECT DISTINCT r.reference_file_address FROM reference r, chromosome c, chromosome_variation_annotation cva, variation v, population p, individual i WHERE r.id = c.reference_id AND c.id = cva.chromosome_id AND cva.variation_id = v.id AND v.population_id = p.id AND p.id = i.population_id AND i.individual_identification = '%s'" % individual_identification
    cursor.execute(cursor.mogrify('explain analyse ' + query))
    analyze_result = cursor.fetchall()
    sum = time(analyze_result[-1][0])

    print("Total execution time: %.2f" % sum)
    print(analyze_result)

    cursor.execute(query)
    print(cursor.fetchall())

#7
def get_qtd_individuals_with_annotation(annotation):
    print("Consulta 7")
    cursor = start_up()
    query = "SELECT COUNT(DISTINCT(i.id)) FROM individual i, population p, variation v, chromosome_variation_annotation cva, biologic_annotation ba WHERE ba.annotation = '" + annotation + "\n' AND ba.id = cva.biologic_annotation_id AND cva.variation_id = v.id AND v.population_id = p.id AND i.population_id = p.id"
    cursor.execute(cursor.mogrify('explain analyse ' + query))
    analyze_result = cursor.fetchall()
    sum = time(analyze_result[-1][0])

    print("Total execution time: %.2f" % sum)

    cursor.execute(query)
    print(len(cursor.fetchall()))

#8
def get_individuals_with_annotation(annotation):
    print("Consulta 8")
    cursor = start_up()
    query = "SELECT DISTINCT(i.individual_identification) FROM individual i, population p, variation v, chromosome_variation_annotation cva, biologic_annotation ba WHERE ba.annotation = '" + annotation + "\n' AND ba.id = cva.biologic_annotation_id AND cva.variation_id = v.id AND v.population_id = p.id AND i.population_id = p.id"
    cursor.execute(cursor.mogrify('explain analyse ' + query))
    analyze_result = cursor.fetchall()
    sum = time(analyze_result[-1][0])

    print("Total execution time: %.2f" % sum)

    cursor.execute(query)
    print(len(cursor.fetchall()))
#9
def snps_of_a_chromosome_in_a_population_at_each_reference(population_id):
    print("Consulta 9")

    cursor = start_up()
    query_reference = "SELECT id FROM reference "
    cursor.execute(query_reference)
    reference_results = cursor.fetchall()
    cursor.execute(cursor.mogrify('explain analyze ' + query_reference))
    analyze_result = cursor.fetchall()
    sum = 0
    sum += time(analyze_result[-1][0])

    results_chromosomes = {}
    for reference_result in reference_results:
        results_chromosomes[reference_result[0]] = []
        cursor2 = start_up()
        query_chromosome = "SELECT c.id, c.chromosome_description FROM chromosome c WHERE c.reference_id = '%s'" % (reference_result[0])
        cursor2.execute(query_chromosome)
        results_chromosomes[reference_result[0]].extend(cursor2.fetchall())
        cursor.execute(cursor.mogrify('explain analyze ' + query_chromosome))
        analyze_result = cursor.fetchall()
        sum += time(analyze_result[-1][0])

    for reference_id in results_chromosomes.keys():
        print ("Reference: %s" % (reference_id))
        for chromosome in results_chromosomes[reference_id]:
            print ("\tChromosome: %s" % (chromosome[1]))
            query_snps = "SELECT COUNT(DISTINCT v.id) FROM variation v, chromosome_variation_annotation cva WHERE v.id = cva.variation_id AND v.population_id = '%s' AND cva.chromosome_id = %s" % (population_id, chromosome[0])
            #cursor.execute(query_snps)
            #result_snp = cursor.fetchone()
            #print("\t --Quantidade: %s \n\n" % (result_snp[0]))
            cursor.execute(cursor.mogrify('explain analyze ' + query_snps))
            analyze_result = cursor.fetchall()
            sum += time(analyze_result[-1][0])
    print("Total execution time: %.2f" % sum)

#10
def get_annotation_related_to_individual(individual_indentification):
    print("Consulta 10")
    cursor = start_up()
    query = "SELECT DISTINCT(ba.annotation) FROM biologic_annotation ba, chromosome_variation_annotation cva, variation v, population p, individual i WHERE i.individual_identification = '%s' AND i.population_id = p.id AND p.id = v.population_id AND cva.variation_id = v.id AND ba.id = cva.biologic_annotation_id" % individual_indentification
    cursor.execute(cursor.mogrify('explain analyse ' + query))
    analyze_result = cursor.fetchall()
    sum = time(analyze_result[-1][0])

    print("Total execution time: %.2f" % sum)

    cursor.execute(query)
    print(len(cursor.fetchall()))
#11
def get_annotations_related_to_chromosome(chromosome_id):
    print("Consulta 11")
    cursor = start_up()
    query = "SELECT DISTINCT(ba.annotation) FROM chromosome_variation_annotation cva, biologic_annotation ba WHERE cva.chromosome_id = %s AND cva.biologic_annotation_id = ba.id" % chromosome_id
    cursor.execute(cursor.mogrify('explain analyse ' + query))
    analyze_result = cursor.fetchall()
    sum = time(analyze_result[-1][0])

    print("Total execution time: %.2f" % sum)

    cursor.execute(query)
    print(len(cursor.fetchall()))

#12
def get_annotations_related_to_position_and_populations_related_to_them(positions):
    print("Consulta 12")
    cursor = start_up()

    query = "SELECT DISTINCT(ba.annotation, p.id) FROM biologic_annotation ba, chromosome_variation_annotation cva, variation v, population p WHERE v.pos in %s AND v.population_id = p.id AND cva.variation_id = v.id AND cva.biologic_annotation_id = ba.id" % (str(positions).replace('[', '(').replace(']', ')'))

    cursor.execute(cursor.mogrify('explain analyse ' + query))
    analyze_result = cursor.fetchall()
    sum = time(analyze_result[-1][0])

    print("Total execution time: %.2f" % sum)

    cursor.execute(query)
    print(cursor.fetchall())
