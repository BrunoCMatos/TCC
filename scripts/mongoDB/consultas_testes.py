import consultas
'''
db.variation.getPlanCache().clear()
db.genotype.getPlanCache().clear()
db.chromosome.getPlanCache().clear()
db.individual.getPlanCache().clear()
'''
for i in range(10):
    print("Execução: " + str(i + 1))
    #1 --
    consultas.snps_in_a_experiment("rice1", "Oryza_sativa.IRGSP-1.0.dna_rm.all_chromosomes")

for i in range(10):
    print("Execução: " + str(i + 1))
    #2 --
    chromosome_id = 3
    consultas.get_all_snps_of_a_chromosome(chromosome_id)

for i in range(10):
    print("Execução: " + str(i + 1))
    #3 --
    consultas.get_annotations_of_a_population('rice1')

for i in range(10):
    print("Execução: " + str(i + 1))
    #4 -- estranho
    biologic_annotation = " expressed protein"
    consultas.variation_related_to_biologic_annotation_and_individuals_related_to_them(biologic_annotation)

for i in range(10):
    print("Execução: " + str(i + 1))
    #5 --
    consultas.get_annotations_related_to_variation("SNP-1.10006211.")

for i in range(10):
    print("Execução: " + str(i + 1))
    #6 --
    consultas.get_qtd_individuals_with_annotation("expressed protein")

for i in range(10):
    print("Execução: " + str(i + 1))
    #7 --
    consultas.get_individuals_with_annotation(" expressed protein")

for i in range(10):
    print("Execução: " + str(i + 1))
    #8 --
    consultas.snps_of_each_chromosome_in_a_population("rice1")

for i in range(10):
    print("Execução: " + str(i + 1))
    #9 --
    consultas.get_annotation_related_to_individual('IRGC121864@0a12f8f9.0')

for i in range(10):
    print("Execução: " + str(i + 1))
    #10 --
    consultas.get_annotations_related_to_chromosome(3)

for i in range(10):
    print("Execução: " + str(i + 1))
    #11 --
    positions = ["958179", "10006042", "10007236"]
    consultas.get_annotations_related_to_position_and_populations_related_to_them(positions)
