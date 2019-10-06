from pymongo import MongoClient

try:
    conn = MongoClient()
    print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")

db = conn.snps

#1
def snps_in_a_experiment(population_id, reference_id):
    print("Consulta 1")
    chromosome_filter_query = {
        "reference_id" : reference_id
    }
    chromosome_projection = {
        "id" : 1,
    }
    chromosome_results = db.chromosome.find(chromosome_filter_query, chromosome_projection)
    analyze_result = chromosome_results.explain()
    number_of_snps = 0
    sum = analyze_result["executionStats"]["executionTimeMillis"]
    for chromosome in chromosome_results:
        print(chromosome["id"])
        variation_query_filter = {
            "chrom" : str(chromosome["id"]),
            "population_id" : population_id
        }
        variation_projection = {
             "variation_identification" : 1
        }
        analyze_result = db.variation.find(variation_query_filter, variation_projection).explain()
        number_of_snps += db.variation.count(variation_query_filter)
        sum += analyze_result["executionStats"]["executionTimeMillis"]
    print("Total execution time: %.2f" % sum)
    print(number_of_snps)

#2
def get_all_snps_of_a_chromosome(chromosome_id):
    print("Consulta 2")

    variation_projection = {
        "variation_identification": 1
    }

    variation_results = db.variation.find({"chrom" : str(chromosome_id)}, variation_projection).explain()["executionStats"]["executionTimeMillis"]

    print(variation_results)
    print(db.variation.count({"chrom" : str(chromosome_id)}))
#3
def get_annotations_of_a_population(population_id):
    print("Consulta 3")

    variation_query_filter = {
        "population_id": population_id,
        "annotations" : {
            "$exists" : "true"
        }
    }
    variation_projection = {
        "annotations" : 1
    }

    variation_results = db.variation.find(variation_query_filter, variation_projection).explain()["executionStats"]["executionTimeMillis"]

    print(variation_results)

    print(db.variation.count(variation_query_filter))


#4
def variation_related_to_biologic_annotation_and_individuals_related_to_them(biologic_annotation):
    print("Consulta 4")

    variation_filter_query = {
        "annotations": {"$regex" :  biologic_annotation}
    }
    variation_projection = {
        "variation_identification": 1,
        "population_id": 1
    }
    variation_results = db.variation.find(variation_filter_query, variation_projection)
    sum = variation_results.explain()["executionStats"]["executionTimeMillis"]

    population_ids = list(set([result["population_id"] for result in variation_results]))

    individual_filter_query = {
        "population_id" : {"$in" : population_ids}
    }

    individual_projection = {
        "id" : 1,
        "individual_identification" : 1
    }

    individual_results = db.individual.find(individual_filter_query, individual_projection).explain()["executionStats"]["executionTimeMillis"]
    sum += individual_results
    print(sum)

    print(db.variation.count(variation_filter_query))

#5
def get_annotations_related_to_variation(variation_identification):
    print("Consulta 5")

    variation_filter_query = {
        "variation_identification":  variation_identification
    }
    variation_projection = {
        "annotations": 1
    }
    variation_results = db.variation.find(variation_filter_query, variation_projection)
    sum = variation_results.explain()["executionStats"]["executionTimeMillis"]

    print(sum)
    print(variation_results[0]["annotations"])

#6 remover
def get_reference_of_individual(individual_identification):
    print("Consulta 6")
    individual_filter_query = {
        "individual_identification" : individual_identification
    }

    individual_projection = {
        "population_id" : 1
    }

    individual_results = db.individual.find(individual_filter_query, individual_projection)
    sum = individual_results.explain()["executionStats"]["executionTimeMillis"]

    variation_filter_query = {
        "population_id" : individual_results[0]["population_id"]
    }

    variation_projection = {
        "chrom" : 1
    }

    variation_results = db.variation.find_one(variation_filter_query, variation_projection)

    chromosome_filter_query = {
        "id" : int(variation_results["chrom"])
    }

    chromosome_projection = {
        "reference_id" : 1
    }

    chromosome_results = db.chromosome.find(chromosome_filter_query, chromosome_projection)
    sum += chromosome_results.explain()["executionStats"]["executionTimeMillis"]

    print(chromosome_results[0]["reference_id"])
    print(sum)


#7
def get_qtd_individuals_with_annotation(annotation):
    print("Consulta 7")

    variation_filter_query = {
        "annotations" : {"$regex" : annotation}
    }

    variation_projection = {
        "population_id" : 1
    }

    variation_results = db.variation.find(variation_filter_query, variation_projection)
    sum = variation_results.explain()["executionStats"]["executionTimeMillis"]

    population_ids = [variation_result["population_id"] for variation_result in variation_results]

    individual_filter_query = {
        "population_id": {"$in": population_ids}
    }

    individual_projection = {
        "individual_identification": 1
    }

    individual_results = db.individual.find(individual_filter_query, individual_projection)
    sum += individual_results.explain()["executionStats"]["executionTimeMillis"]
    print(sum)

    print(db.variation.count(variation_filter_query))

#8
def get_individuals_with_annotation(annotation):
    print("Consulta 8")

    variation_filter_query = {
        "annotations": {"$regex": annotation}
    }

    variation_projection = {
        "population_id": 1
    }

    variation_results = db.variation.find(variation_filter_query, variation_projection)
    sum = variation_results.explain()["executionStats"]["executionTimeMillis"]

    population_ids = [variation_result["population_id"] for variation_result in variation_results]

    individual_filter_query = {
        "population_id": {"$in": population_ids}
    }

    individual_projection = {
        "individual_identification": 1
    }

    individual_results = db.individual.find(individual_filter_query, individual_projection)
    sum += individual_results.explain()["executionStats"]["executionTimeMillis"]
    print(sum)

    print(db.variation.count(variation_filter_query))

#9
def snps_of_each_chromosome_in_a_population(population_id):
    print("Consulta 9")

    reference_projection = {
        "id" : 1
    }

    reference_results = db.reference.find({}, reference_projection)
    sum = reference_results.explain()["executionStats"]["executionTimeMillis"]

    results_chromosomes = {}
    for reference_result in reference_results:
        results_chromosomes[reference_result["id"]] = []
        chromosome_filter_query = {
            "reference_id" : str(reference_result["id"])
        }
        chromosome_projection = {
            "id" : 1,
            "chromosome_description" : 1
        }

        chromosome_results = db.chromosome.find(chromosome_filter_query, chromosome_projection)
        sum += chromosome_results.explain()["executionStats"]["executionTimeMillis"]

        results_chromosomes[reference_result["id"]].extend(chromosome_results)

    quantidade_total = 0
    for reference_id in results_chromosomes.keys():
        print ("Reference: %s" % (reference_id))
        for chromosome in results_chromosomes[reference_id]:
            print ("\tChromosome: %s" % (chromosome["chromosome_description"]))

            variation_filter_query = {
                "chrom": str(chromosome["id"]),
                "population_id" : population_id
            }

            variation_projection = {
                "id" : 1
            }

            qtd_variation = db.variation.count(variation_filter_query)
            quantidade_total += qtd_variation
            sum += db.variation.find(variation_filter_query, variation_projection).explain()["executionStats"]["executionTimeMillis"]
            print(qtd_variation)
    print("Total execution time: %.2f" % sum)
    print(quantidade_total)

#10
def get_annotation_related_to_individual(individual_indentification):
    print("Consulta 10")

    individual_filter_query = {
        "individual_identification" : individual_indentification
    }

    individual_projection = {
        "population_id" : 1
    }

    individual_results = db.individual.find(individual_filter_query, individual_projection)
    sum = individual_results.explain()["executionStats"]["executionTimeMillis"]

    variation_filter_query = {
        "annotations": {
            "$exists": "true"
        },
        "population_id" : str(individual_results[0]["population_id"])
    }

    variation_projection = {
        "annotations" : 1
    }

    variation_results = db.variation.find(variation_filter_query, variation_projection)
    sum += variation_results.explain()["executionStats"]["executionTimeMillis"]

    print("Total execution time: %.2f" % sum)
    print(db.variation.count(variation_filter_query))

#11
def get_annotations_related_to_chromosome(chromosome_id):
    print("Consulta 11")

    variation_filter_query = {
        "chrom" : str(chromosome_id),
        "annotations": {
            "$exists": "true"
        }
    }

    variation_projection = {
        "annotations" : 1
    }

    variation_results = db.variation.find(variation_filter_query, variation_projection)

    sum = variation_results.explain()["executionStats"]["executionTimeMillis"]

    print("Total execution time: %.2f" % sum)
    print(db.variation.count(variation_filter_query))

#12
def get_annotations_related_to_position_and_populations_related_to_them(positions):
    print("Consulta 12")
# { "$in": chromosome_ids}

    variation_filter_query = {
        "pos" :  { "$in": positions},
        "annotations": {
            "$exists": "true"
        }
    }

    variation_projection = {
        "annotations" : 1,
        "population_id" : 1
    }

    variation_results = db.variation.find(variation_filter_query, variation_projection)
    sum = variation_results.explain()["executionStats"]["executionTimeMillis"]

    print(sum)

    for variation_result in variation_results:
        print(variation_result["annotations"], variation_result["population_id"])
