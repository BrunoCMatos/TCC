
#10
def get_annotation_related_to_individual(individual_indentification):
    print("Consulta 10")
    cursor = start_up()
    query = "SELECT v.snp_annotation->>'annotations' FROM variation v, population p, individual i WHERE v.snp_annotation ? 'annotations' AND i.individual_identification = '%s' AND i.population_id = p.id AND p.id = v.population_id" % individual_indentification
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
    query = "SELECT v.snp_annotation->>'annotations' FROM variation v WHERE v.chrom = %s AND v.snp_annotation ? 'annotations'" % chromosome_id
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

    pos_statement = "("
    for position in positions[:-1]:
        pos_statement += "v.snp_annotation @>'{\"pos\" : %s}' OR " % position
    pos_statement += "v.snp_annotation @>'{\"pos\" : %s}')" % positions[-1]
    query = "SELECT v.snp_annotation->>'annotations', p.id FROM variation v, population p WHERE %s AND v.population_id = p.id" % pos_statement
    print(query)
    cursor.execute(cursor.mogrify('explain analyse ' + query))
    analyze_result = cursor.fetchall()
    sum = time(analyze_result[-1][0])

    print("Total execution time: %.2f" % sum)

    cursor.execute(query)
    print(cursor.fetchall())
