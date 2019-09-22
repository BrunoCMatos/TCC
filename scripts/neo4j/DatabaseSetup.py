from neo4j import GraphDatabase

# Database Credentials

uri = "bolt://localhost:7687"

# Connect to the neo4j database server

graphDB_Driver = GraphDatabase.driver(uri)

#Insert
variation = "CALL apoc.load.json('dump_mongo_variation') YIELD value AS variation CREATE"\
        "(v:variation{id:variation.id,chrom:variation.chrom,variation_identification:variation.variation_identification,"\
        "pos:variation.pos,reference_allele:variation.reference_allele,alternative_allele:variation.alternative_allele,"\
        "annotations:variation.annotations,population_id:variation.population_id});"

chromosome = "CALL apoc.load.json('dump_mongo_chromosome') YIELD value AS chromosome CREATE"\
        "(c:chromosome{id:chromosome.id,reference_id:chromosome.reference_id,chromosome_description:chromosome.chromosome_description});"

population = "CALL apoc.load.json('dump_mongo_population') YIELD value AS population CREATE"\
        "(p:population{id:population.id,experiment:population.experiment});"

reference = "CALL apoc.load.json('dump_mongo_reference') YIELD value AS reference CREATE"\
        "(r:reference{id:reference.id,reference_file_address:reference.reference_file_address,associated_paper_address:reference.associated_paper_address});"

individual = "CALL apoc.load.json('dump_mongo_individual') YIELD value AS individual CREATE"\
        "(i:individual{id:individual.id,individual_identification:individual.individual_identification,description:individual.description,"\
        "phenotype:individual.phenotype, population_id:individual.population_id});"


#Relationships
chromosome_of_reference = "match (c:chromosome), (re:reference) where re.id = c.reference_id create (c) - [r:chromossome_of_reference]->(re) RETURN type(r);"

variation_of_chromosome = "match (c:chromosome), (v:variation) where c.id = toInt(v.chrom) create (v) - [r:variation_of_chromosome]->(c) RETURN type(r);"

variation_of_population = "match (p:population), (v:variation) where p.id = v.population_id create (v) - [r:variation_of_population]->(p) RETURN type(r);"

individual_of_population = "match (p:population), (i:individual) where p.id = i.population_id create (i) - [r:individual_of_population]->(p) RETURN type(r);"

def insert_node(node_query):
    graphdb_session = graphDB_Driver.session()
    graphdb_session.run(node_query)
    print(graphdb_session.sync())
    graphDB_Driver.close()

def create_relationships(relationship_query):
    graphdb_session = graphDB_Driver.session()
    graphdb_session.run(relationship_query)
    print(graphdb_session.sync())
    graphDB_Driver.close()

#Inserts
insert_node(variation)
insert_node(chromosome)
insert_node(population)
insert_node(reference)
insert_node(individual)

#Relatioships
create_relationships(chromosome_of_reference)
create_relationships(variation_of_chromosome)
create_relationships(variation_of_population)
create_relationships(individual_of_population)


