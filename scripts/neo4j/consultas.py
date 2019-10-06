from neo4j import GraphDatabase

uri = "bolt://localhost:7687"

#1 refazer
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
#
# #6 remover
# def get_reference_of_individual(individual_identification):
#     print("Consulta 6")
#     individual_filter_query = {
#         "individual_identification" : individual_identification
#     }
#
#     individual_projection = {
#         "population_id" : 1
#     }
#
#     individual_results = db.individual.find(individual_filter_query, individual_projection)
#     sum = individual_results.explain()["executionStats"]["executionTimeMillis"]
#
#     variation_filter_query = {
#         "population_id" : individual_results[0]["population_id"]
#     }
#
#     variation_projection = {
#         "chrom" : 1
#     }
#
#     variation_results = db.variation.find_one(variation_filter_query, variation_projection)
#
#     chromosome_filter_query = {
#         "id" : int(variation_results["chrom"])
#     }
#
#     chromosome_projection = {
#         "reference_id" : 1
#     }
#
#     chromosome_results = db.chromosome.find(chromosome_filter_query, chromosome_projection)
#     sum += chromosome_results.explain()["executionStats"]["executionTimeMillis"]
#
#     print(chromosome_results[0]["reference_id"])
#     print(sum)
#
#
# #7
# def get_qtd_individuals_with_annotation(annotation):
#     print("Consulta 7")
#
#     variation_filter_query = {
#         "annotations" : {"$regex" : annotation}
#     }
#
#     variation_projection = {
#         "population_id" : 1
#     }
#
#     variation_results = db.variation.find(variation_filter_query, variation_projection)
#     sum = variation_results.explain()["executionStats"]["executionTimeMillis"]
#
#     population_ids = [variation_result["population_id"] for variation_result in variation_results]
#
#     individual_filter_query = {
#         "population_id": {"$in": population_ids}
#     }
#
#     individual_projection = {
#         "individual_identification": 1
#     }
#
#     individual_results = db.individual.find(individual_filter_query, individual_projection)
#     sum += individual_results.explain()["executionStats"]["executionTimeMillis"]
#     print(sum)
#
#     print(db.variation.count(variation_filter_query))
#
# #8
# def get_individuals_with_annotation(annotation):
#     print("Consulta 8")
#
#     variation_filter_query = {
#         "annotations": {"$regex": annotation}
#     }
#
#     variation_projection = {
#         "population_id": 1
#     }
#
#     variation_results = db.variation.find(variation_filter_query, variation_projection)
#     sum = variation_results.explain()["executionStats"]["executionTimeMillis"]
#
#     population_ids = [variation_result["population_id"] for variation_result in variation_results]
#
#     individual_filter_query = {
#         "population_id": {"$in": population_ids}
#     }
#
#     individual_projection = {
#         "individual_identification": 1
#     }
#
#     individual_results = db.individual.find(individual_filter_query, individual_projection)
#     sum += individual_results.explain()["executionStats"]["executionTimeMillis"]
#     print(sum)
#
#     print(db.variation.count(variation_filter_query))
#
# #9
# def snps_of_a_chromosome_in_a_population_at_each_reference(population_id):
#     print("Consulta 9")
#
#     reference_projection = {
#         "id" : 1
#     }
#
#     reference_results = db.reference.find({}, reference_projection)
#     sum = reference_results.explain()["executionStats"]["executionTimeMillis"]
#
#     results_chromosomes = {}
#     for reference_result in reference_results:
#         results_chromosomes[reference_result["id"]] = []
#         chromosome_filter_query = {
#             "reference_id" : str(reference_result["id"])
#         }
#         chromosome_projection = {
#             "id" : 1,
#             "chromosome_description" : 1
#         }
#
#         chromosome_results = db.chromosome.find(chromosome_filter_query, chromosome_projection)
#         sum += chromosome_results.explain()["executionStats"]["executionTimeMillis"]
#
#         results_chromosomes[reference_result["id"]].extend(chromosome_results)
#
#     quantidade_total = 0
#     for reference_id in results_chromosomes.keys():
#         print ("Reference: %s" % (reference_id))
#         for chromosome in results_chromosomes[reference_id]:
#             print ("\tChromosome: %s" % (chromosome["chromosome_description"]))
#
#             variation_filter_query = {
#                 "chrom": str(chromosome["id"]),
#                 "population_id" : population_id
#             }
#
#             variation_projection = {
#                 "id" : 1
#             }
#
#             qtd_variation = db.variation.count(variation_filter_query)
#             quantidade_total += qtd_variation
#             sum += db.variation.find(variation_filter_query, variation_projection).explain()["executionStats"]["executionTimeMillis"]
#             print(qtd_variation)
#     print("Total execution time: %.2f" % sum)
#     print(quantidade_total)
#
# #10
# def get_annotation_related_to_individual(individual_indentification):
#     print("Consulta 10")
#
#     individual_filter_query = {
#         "individual_identification" : individual_indentification
#     }
#
#     individual_projection = {
#         "population_id" : 1
#     }
#
#     individual_results = db.individual.find(individual_filter_query, individual_projection)
#     sum = individual_results.explain()["executionStats"]["executionTimeMillis"]
#
#     variation_filter_query = {
#         "annotations": {
#             "$exists": "true"
#         },
#         "population_id" : str(individual_results[0]["population_id"])
#     }
#
#     variation_projection = {
#         "annotations" : 1
#     }
#
#     variation_results = db.variation.find(variation_filter_query, variation_projection)
#     sum += variation_results.explain()["executionStats"]["executionTimeMillis"]
#
#     print("Total execution time: %.2f" % sum)
#     print(db.variation.count(variation_filter_query))
#
# #11
# def get_annotations_related_to_chromosome(chromosome_id):
#     print("Consulta 11")
#
#     variation_filter_query = {
#         "chrom" : str(chromosome_id),
#         "annotations": {
#             "$exists": "true"
#         }
#     }
#
#     variation_projection = {
#         "annotations" : 1
#     }
#
#     variation_results = db.variation.find(variation_filter_query, variation_projection)
#
#     sum = variation_results.explain()["executionStats"]["executionTimeMillis"]
#
#     print("Total execution time: %.2f" % sum)
#     print(db.variation.count(variation_filter_query))
#
# #12
# def get_annotations_related_to_position_and_populations_related_to_them(positions):
#     print("Consulta 12")
# # { "$in": chromosome_ids}
#
#     variation_filter_query = {
#         "pos" :  { "$in": positions},
#         "annotations": {
#             "$exists": "true"
#         }
#     }
#
#     variation_projection = {
#         "annotations" : 1,
#         "population_id" : 1
#     }
#
#     variation_results = db.variation.find(variation_filter_query, variation_projection)
#     sum = variation_results.explain()["executionStats"]["executionTimeMillis"]
#
#     print(sum)
#
#     for variation_result in variation_results:
#         print(variation_result["annotations"], variation_result["population_id"])
