import consultas
from neo4j import GraphDatabase

uri = "bolt://localhost:7687"

# for i in range(10):
#     print("Execução: " + str(i + 1))
#     #1 --
# graphDB_Driver = GraphDatabase.driver(uri)
# graphdb_session = graphDB_Driver.session()
# graphdb_session.read_transaction(consultas.snps_in_a_experiment, "rice1", "Oryza_sativa.IRGSP-1.0.dna_rm.all_chromosomes")
# graphDB_Driver.close()


# for i in range(10):
#     print("Execução: " + str(i + 1))
#     #2 --
# graphDB_Driver = GraphDatabase.driver(uri)
# graphdb_session = graphDB_Driver.session()
# chromosome_id = 3
# graphdb_session.read_transaction(consultas.get_all_snps_of_a_chromosome, str(chromosome_id))
# graphDB_Driver.close()

# for i in range(10):
#     print("Execução: " + str(i + 1))
#     #3 --
# graphDB_Driver = GraphDatabase.driver(uri)
# graphdb_session = graphDB_Driver.session()
# graphdb_session.read_transaction(consultas.get_annotations_of_a_population, 'rice1')
# graphDB_Driver.close()
#
# for i in range(10):
#     print("Execução: " + str(i + 1))
#     #4 -- estranho
# biologic_annotation = "expressed protein"
# graphDB_Driver = GraphDatabase.driver(uri)
# graphdb_session = graphDB_Driver.session()
# graphdb_session.read_transaction(consultas.variation_related_to_biologic_annotation_and_individuals_related_to_them, biologic_annotation)
# graphDB_Driver.close()
#
# for i in range(10):
#     print("Execução: " + str(i + 1))
#     #5 --
# biologic_annotation = "expressed protein"
# graphDB_Driver = GraphDatabase.driver(uri)
# graphdb_session = graphDB_Driver.session()
# graphdb_session.read_transaction(consultas.get_annotations_related_to_variation, "SNP-1.10006211.")
# graphDB_Driver.close()
#
# for i in range(10):
#     print("Execução: " + str(i + 1))
#     #7 --
# graphDB_Driver = GraphDatabase.driver(uri)
# graphdb_session = graphDB_Driver.session()
# graphdb_session.read_transaction(consultas.get_qtd_individuals_with_annotation, "expressed protein")
# graphDB_Driver.close()
#
# for i in range(10):
#     print("Execução: " + str(i + 1))
#     #8 --
# graphDB_Driver = GraphDatabase.driver(uri)
# graphdb_session = graphDB_Driver.session()
# graphdb_session.read_transaction(consultas.get_individuals_with_annotation, "expressed protein")
# graphDB_Driver.close()
#
# for i in range(10):
#     print("Execução: " + str(i + 1))
#     #9 --
# graphDB_Driver = GraphDatabase.driver(uri)
# graphdb_session = graphDB_Driver.session()
# graphdb_session.read_transaction(consultas.snps_of_each_chromosome_in_a_population, "rice1")
# graphDB_Driver.close()
#
# for i in range(10):
#     print("Execução: " + str(i + 1))
#     #10 --
# graphDB_Driver = GraphDatabase.driver(uri)
# graphdb_session = graphDB_Driver.session()
# graphdb_session.read_transaction(consultas.get_annotation_related_to_individual, 'IRGC121864@0a12f8f9.0')
# graphDB_Driver.close()
#
# for i in range(10):
#     print("Execução: " + str(i + 1))
#     #11 --
# graphDB_Driver = GraphDatabase.driver(uri)
# graphdb_session = graphDB_Driver.session()
# graphdb_session.read_transaction(consultas.get_annotations_related_to_chromosome, 3)
# graphDB_Driver.close()
#
# for i in range(10):
#     print("Execução: " + str(i + 1))
#     #12 --
positions = ["958179", "10006042", "10007236"]
graphDB_Driver = GraphDatabase.driver(uri)
graphdb_session = graphDB_Driver.session()
graphdb_session.read_transaction(consultas.get_annotations_related_to_position_and_populations_related_to_them, positions)
graphDB_Driver.close()