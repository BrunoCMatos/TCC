from neo4j import GraphDatabase

# Database Credentials

uri = "bolt://localhost:7687"

# Connect to the neo4j database server

#Insert
variation_chrom_1 = "CALL apoc.load.json('annotations_chrom_1.json') YIELD value AS variation CREATE"\
        "(v:variation{id:variation.id,chrom:variation.chrom,variation_identification:variation.variation_identification,"\
        "pos:variation.pos,reference_allele:variation.reference_allele,alternative_allele:variation.alternative_allele,"\
        "annotations:variation.annotations,population_id:variation.population_id});"

variation_chrom_2 = "CALL apoc.load.json('annotations_chrom_2.json') YIELD value AS variation CREATE"\
        "(v:variation{id:variation.id,chrom:variation.chrom,variation_identification:variation.variation_identification,"\
        "pos:variation.pos,reference_allele:variation.reference_allele,alternative_allele:variation.alternative_allele,"\
        "annotations:variation.annotations,population_id:variation.population_id});"

variation_chrom_3 = "CALL apoc.load.json('annotations_chrom_3.json') YIELD value AS variation CREATE"\
        "(v:variation{id:variation.id,chrom:variation.chrom,variation_identification:variation.variation_identification,"\
        "pos:variation.pos,reference_allele:variation.reference_allele,alternative_allele:variation.alternative_allele,"\
        "annotations:variation.annotations,population_id:variation.population_id});"

variation_chrom_4 = "CALL apoc.load.json('annotations_chrom_4.json') YIELD value AS variation CREATE"\
        "(v:variation{id:variation.id,chrom:variation.chrom,variation_identification:variation.variation_identification,"\
        "pos:variation.pos,reference_allele:variation.reference_allele,alternative_allele:variation.alternative_allele,"\
        "annotations:variation.annotations,population_id:variation.population_id});"

variation_chrom_5 = "CALL apoc.load.json('annotations_chrom_5.json') YIELD value AS variation CREATE"\
        "(v:variation{id:variation.id,chrom:variation.chrom,variation_identification:variation.variation_identification,"\
        "pos:variation.pos,reference_allele:variation.reference_allele,alternative_allele:variation.alternative_allele,"\
        "annotations:variation.annotations,population_id:variation.population_id});"

variation_chrom_6 = "CALL apoc.load.json('annotations_chrom_6.json') YIELD value AS variation CREATE"\
        "(v:variation{id:variation.id,chrom:variation.chrom,variation_identification:variation.variation_identification,"\
        "pos:variation.pos,reference_allele:variation.reference_allele,alternative_allele:variation.alternative_allele,"\
        "annotations:variation.annotations,population_id:variation.population_id});"

variation_chrom_7 = "CALL apoc.load.json('annotations_chrom_7.json') YIELD value AS variation CREATE"\
        "(v:variation{id:variation.id,chrom:variation.chrom,variation_identification:variation.variation_identification,"\
        "pos:variation.pos,reference_allele:variation.reference_allele,alternative_allele:variation.alternative_allele,"\
        "annotations:variation.annotations,population_id:variation.population_id});"

variation_chrom_8 = "CALL apoc.load.json('annotations_chrom_8.json') YIELD value AS variation CREATE"\
        "(v:variation{id:variation.id,chrom:variation.chrom,variation_identification:variation.variation_identification,"\
        "pos:variation.pos,reference_allele:variation.reference_allele,alternative_allele:variation.alternative_allele,"\
        "annotations:variation.annotations,population_id:variation.population_id});"

variation_chrom_9 = "CALL apoc.load.json('annotations_chrom_9.json') YIELD value AS variation CREATE"\
        "(v:variation{id:variation.id,chrom:variation.chrom,variation_identification:variation.variation_identification,"\
        "pos:variation.pos,reference_allele:variation.reference_allele,alternative_allele:variation.alternative_allele,"\
        "annotations:variation.annotations,population_id:variation.population_id});"

variation_chrom_10 = "CALL apoc.load.json('annotations_chrom_10.json') YIELD value AS variation CREATE"\
        "(v:variation{id:variation.id,chrom:variation.chrom,variation_identification:variation.variation_identification,"\
        "pos:variation.pos,reference_allele:variation.reference_allele,alternative_allele:variation.alternative_allele,"\
        "annotations:variation.annotations,population_id:variation.population_id});"

variation_chrom_11 = "CALL apoc.load.json('annotations_chrom_11.json') YIELD value AS variation CREATE"\
        "(v:variation{id:variation.id,chrom:variation.chrom,variation_identification:variation.variation_identification,"\
        "pos:variation.pos,reference_allele:variation.reference_allele,alternative_allele:variation.alternative_allele,"\
        "annotations:variation.annotations,population_id:variation.population_id});"

variation_chrom_12 = "CALL apoc.load.json('annotations_chrom_12.json') YIELD value AS variation CREATE"\
        "(v:variation{id:variation.id,chrom:variation.chrom,variation_identification:variation.variation_identification,"\
        "pos:variation.pos,reference_allele:variation.reference_allele,alternative_allele:variation.alternative_allele,"\
        "annotations:variation.annotations,population_id:variation.population_id});"

chromosome = "CALL apoc.load.json('chromosome_table_input.json') YIELD value AS chromosome CREATE"\
        "(c:chromosome{id:chromosome.id,reference_id:chromosome.reference_id,chromosome_description:chromosome.chromosome_description});"

population = "CALL apoc.load.json('population_table_input.json') YIELD value AS population CREATE"\
        "(p:population{id:population.id,experiment:population.experiment});"

reference = "CALL apoc.load.json('reference_table_input.json') YIELD value AS reference CREATE"\
        "(r:reference{id:reference.id,reference_file_address:reference.reference_file_address,associated_paper_address:reference.associated_paper_address});"

individual = "CALL apoc.load.json('individual_table_input.json') YIELD value AS individual CREATE"\
        "(i:individual{id:individual.id,individual_identification:individual.individual_identification,description:individual.description,"\
        "phenotype:individual.phenotype, population_id:individual.population_id});"


#Relationships
chromosome_to_reference = "match (c:chromosome), (re:reference) where re.id = c.reference_id create (c) - [r:chromossome_to_reference]->(re) RETURN type(r);"

reference_to_chromosome = "match (c:chromosome), (re:reference) where re.id = c.reference_id create (re) - [r:reference_to_chromosome]->(c) RETURN type(r);"

variation_to_chromosome = "match (c:chromosome), (v:variation) where c.id = toInt(v.chrom) create (v) - [r:variation_to_chromosome]->(c) RETURN type(r);"

chromosome_to_variation = "match (c:chromosome), (v:variation) where c.id = toInt(v.chrom) create (c) - [r:chromosome_to_variation]->(v) RETURN type(r);"

variation_to_population = "match (p:population), (v:variation) where p.id = v.population_id create (v) - [r:variation_to_population]->(p) RETURN type(r);"

population_to_variation = "match (p:population), (v:variation) where p.id = v.population_id create (p) - [r:population_to_variation]->(v) RETURN type(r);"

population_to_individual = "match (p:population), (i:individual) where p.id = i.population_id create (p) - [r:population_to_individual]->(i) RETURN type(r);"

individual_to_population = "match (p:population), (i:individual) where p.id = i.population_id create (i) - [r:individual_to_population]->(p) RETURN type(r);"


#Indexes
index_reference_id = "CREATE INDEX ON :reference(id)"

index_chromosome_id = "CREATE INDEX ON :chromosome(id)"
index_chromosome_reference_id = "CREATE INDEX ON :chromosome(reference_id)"

index_individual_id = "CREATE INDEX ON :individual(id)"
index_individual_individual_identification = "CREATE INDEX ON :individual(individual_identification)"

index_population_id = "CREATE INDEX ON :population(id)"

index_variation_id = "CREATE INDEX ON :variation(id)"
index_variation_chrom = "CREATE INDEX ON :variation(chrom)"
index_variation_variation_identification = "CREATE INDEX ON :variation(variation_identification)"
index_variation_pos = "CREATE INDEX ON :variation(pos)"
index_variation_annotations = "CREATE INDEX ON :variation(annotations)"

def insert_node(node_query):
    graphDB_Driver = GraphDatabase.driver(uri)
    graphdb_session = graphDB_Driver.session()
    graphdb_session.run(node_query)
    print(graphdb_session.sync())
    graphDB_Driver.close()

def create_relationships(relationship_query):
    graphDB_Driver = GraphDatabase.driver(uri)
    graphdb_session = graphDB_Driver.session()
    graphdb_session.run(relationship_query)
    print(graphdb_session.sync())
    graphDB_Driver.close()

# Inserts
# insert_node(variation)
# insert_node(chromosome)
# insert_node(population)
# insert_node(reference)
# insert_node(individual)

# Relatioships
# create_relationships(chromosome_to_reference)
# create_relationships(variation_to_chromosome)
# create_relationships(variation_to_population)
# create_relationships(individual_to_population)
# create_relationships(chromosome_to_variation)
# create_relationships(reference_to_chromosome)
# create_relationships(population_to_variation)


