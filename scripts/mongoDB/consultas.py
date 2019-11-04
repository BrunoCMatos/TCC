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
    sum = analyze_result["executionStats"]["executionTimeMillis"]
    chromosome_ids = [str(chromosome["id"]) for chromosome in chromosome_results]
    variation_query_filter = {
        "chrom" : {"$in": chromosome_ids},
        "population_id" : population_id
    }

    variation_projection = {
        "variation_identification": 1
    }

    results = db.variation.find(variation_query_filter, variation_projection)
    sum += results.explain()["executionStats"]["executionTimeMillis"]
    print("Total execution time: %.2f" % sum)
    print(results.count())

#2
def get_all_snps_of_a_chromosome(chromosome_id):
    print("Consulta 2")

    variation_projection = {
        "variation_identification": 1
    }

    variation_results = db.variation.find({"chrom" : str(chromosome_id)}, variation_projection)

    print(variation_results.explain()["executionStats"]["executionTimeMillis"])

    print(variation_results.count())
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
        "annotations": 1
    }

    variation_results = db.variation.find(variation_query_filter, variation_projection)
    print(variation_results.explain()["executionStats"]["executionTimeMillis"])
    print(len(variation_results.distinct("annotations")))

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

#6
def get_qtd_individuals_with_annotation(annotation):
    print("Consulta 6")

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
        "individual_identification" : 1
    }

    individual_results = db.individual.find(individual_filter_query, individual_projection)
    sum += individual_results.explain()["executionStats"]["executionTimeMillis"]
    print(sum)

    print(individual_results.count())

#7
def get_individuals_with_annotation(annotation):
    print("Consulta 7")

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

    print(individual_results.count())

#8
def snps_of_each_chromosome_in_a_population(population_id):
    print("Consulta 8")

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

            variation_results = db.variation.find(variation_filter_query, variation_projection)
            qtd_variation = variation_results.count()
            quantidade_total += qtd_variation
            sum += variation_results.explain()["executionStats"]["executionTimeMillis"]
            print(qtd_variation)
    print("Total execution time: %.2f" % sum)
    print(quantidade_total)

#9
def get_annotation_related_to_individual(individual_indentification):
    print("Consulta 9")

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
    print(len(variation_results.distinct("annotations")))

#10
def get_annotations_related_to_chromosome(chromosome_id):
    print("Consulta 10")

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

    print(variation_results.explain()["executionStats"]["executionTimeMillis"])
    print(len(variation_results.distinct("annotations")))

#11
def get_annotations_related_to_position_and_populations_related_to_them(positions):
    print("Consulta 11")
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
