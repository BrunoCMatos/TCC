from neo4j import GraphDatabase

uri = "bolt://localhost:7687"

#1
def snps_in_a_experiment(tx, population_id, reference_id):
    print("Consulta 1")

    query = "MATCH (chromosome {reference_id: '" + reference_id + "'}) --> (variation {population_id: '" + population_id + "'}) RETURN variation.variation_identification"
    results = tx.run(query)
    print(query)
    cont = 0
    for result in results:
        cont += 1

    print(cont)

#2
def get_all_snps_of_a_chromosome(tx, chromosome_id):
    print("Consulta 2")

    query = "MATCH (chromosome{id: " + chromosome_id + "}) --> (variation) RETURN variation.variation_identification"
    results = tx.run(query)
    print(query)
    cont = 0
    for result in results:
        # print(result['variation.variation_identification'])
        cont += 1

    print(cont)


#3
def get_annotations_of_a_population(tx, population_id):
    print("Consulta 3")

    query = "MATCH (population{id: '" + population_id + "'}) --> (v:variation) WHERE EXISTS (v.annotations) RETURN v.variation_identification"
    results = tx.run(query)
    print(query)
    cont = 0
    for result in results:
        # print(result['v.variation_identification'])
        cont += 1

    print(cont)


# 4
def variation_related_to_biologic_annotation_and_individuals_related_to_them(tx, biologic_annotation):
    print("Consulta 4")

    query = "MATCH (v:variation) where v.annotations CONTAINS '" + biologic_annotation + "' RETURN  v.variation_identification, v.population_id"
    results = tx.run(query)
    print(query)
    cont = 0
    population_ids = set()
    for result in results:
        # print(result['v.variation_identification'])
        cont += 1
        population_ids.add(result['v.population_id'])

    population_ids = list(population_ids)
    print(cont)
    print(population_ids)

    query = "MATCH (i:individual) WHERE i.population_id IN " + str(population_ids) + " RETURN i.individual_identification"

    print(query)
    results = tx.run(query)
    cont = 0
    for result in results:
        # print(result['v.variation_identification'])
        cont += 1

    print(cont)

# 5
def get_annotations_related_to_variation(tx, variation_identification):
    print("Consulta 5")

    query = "MATCH (variation{variation_identification: '" + variation_identification + "'}) RETURN variation.annotations"
    print(query)
    results = tx.run(query)
    annotations = ""
    for result in results:
        # print(result['v.variation_identification'])
        annotations = result['variation.annotations']

    print(annotations)

# 6
def get_qtd_individuals_with_annotation(tx, biologic_annotation):
    print("Consulta 6")

    query = "MATCH (v:variation) where v.annotations CONTAINS '" + biologic_annotation + "' RETURN  v.variation_identification, v.population_id"
    results = tx.run(query)
    print(query)
    cont = 0
    population_ids = set()
    for result in results:
        # print(result['v.variation_identification'])
        cont += 1
        population_ids.add(result['v.population_id'])

    population_ids = list(population_ids)
    print(cont)
    print(population_ids)

    query = "MATCH (i:individual) WHERE i.population_id IN " + str(
        population_ids) + " RETURN i.individual_identification"

    print(query)
    results = tx.run(query)
    cont = 0
    for result in results:
        # print(result['v.variation_identification'])
        cont += 1

    print(cont)

# 7
def get_individuals_with_annotation(tx, biologic_annotation):
    print("Consulta 7")

    query = "MATCH (v:variation) where v.annotations CONTAINS '" + biologic_annotation + "' RETURN  v.variation_identification, v.population_id"
    results = tx.run(query)
    print(query)
    cont = 0
    population_ids = set()
    for result in results:
        # print(result['v.variation_identification'])
        cont += 1
        population_ids.add(result['v.population_id'])

    population_ids = list(population_ids)
    print(cont)
    print(population_ids)

    query = "MATCH (i:individual) WHERE i.population_id IN " + str(
        population_ids) + " RETURN i.individual_identification"

    print(query)
    results = tx.run(query)
    cont = 0
    for result in results:
        # print(result['v.variation_identification'])
        cont += 1

    print(cont)

# 8
def snps_of_each_chromosome_in_a_population(tx, population_id):
    print("Consulta 8")

    query = "MATCH (c:chromosome) --> (v:variation{population_id: '" + population_id + "'}) RETURN c.id, v.variation_identification ORDER BY c.id"
    results = tx.run(query)
    print(query)
    cont = 0
    snps_per_chromsome = [0 for i in range(12)]
    for result in results:
        # print(result['v.variation_identification'])
        cont += 1
        snps_per_chromsome[result['c.id'] - 1] += 1

    print(cont)
    print(snps_per_chromsome)


# 9
def get_annotation_related_to_individual(tx, individual_indentification):
    print("Consulta 9")

    query = "MATCH (i:individual{individual_identification: '" + individual_indentification + "'}) --> (p:population) --> (v:variation) WHERE EXISTS (v.annotations) RETURN v.variation_identification, v.annotations"

    results = tx.run(query)
    print(query)
    cont = 0
    for result in results:
        # print(result['v.variation_identification'])
        cont += 1

    print(cont)

# 10
def get_annotations_related_to_chromosome(tx, chromosome_id):
    print("Consulta 10")

    query = "MATCH (c:chromosome{id: " + str(chromosome_id) + "}) --> (v:variation) WHERE EXISTS (v.annotations) RETURN v.variation_identification, v.annotations"

    results = tx.run(query)
    print(query)
    cont = 0
    for result in results:
        # print(result['v.variation_identification'])
        cont += 1

    print(cont)

# 11
def get_annotations_related_to_position_and_populations_related_to_them(tx, positions):
    print("Consulta 11")

    query = "MATCH (v:variation) WHERE v.pos IN " + str(positions) + " AND EXISTS (v.annotations) RETURN v.variation_identification, v.annotations, v.population_id"

    results = tx.run(query)
    print(query)
    cont = 0
    for result in results:
        # print(result['v.variation_identification'])
        print(result['v.annotations'], result['v.population_id'])