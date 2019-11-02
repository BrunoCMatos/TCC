-- 1 - snps_in_a_experiment
SELECT DISTINCT v.variation_identification
FROM variation v, chromosome_variation_annotation cva
WHERE v.id = cva.variation_id  AND v.population_id = 'rice1'
AND  cva.chromosome_id IN (
select c.id FROM chromosome c WHERE c.reference_id = 'Oryza_sativa.IRGSP-1.0.dna_rm.all_chromosomes');

-- 2 - get_all_snps_of_a_chromosome
SELECT DISTINCT v.variation_identification
FROM variation v, chromosome_variation_annotation cva, chromosome c
WHERE (v.id = cva.variation_id AND cva.chromosome_id = c.id AND c.id = 3)

-- 3 - get_annotations_of_a_population
SELECT  DISTINCT(ba.annotation)
FROM biologic_annotation ba, variation v, chromosome_variation_annotation cva
WHERE ba.id = cva.biologic_annotation_id AND cva.variation_id = v.id AND v.population_id = 'rice1'

-- 4 - variation_related_to_biologic_annotation
SELECT DISTINCT v.variation_identification
FROM variation v, chromosome_variation_annotation cva, biologic_annotation ba
WHERE ba.annotation LIKE '%expressed protein%' AND v.id = cva.variation_id AND cva.biologic_annotation_id = ba.id

-- 5 - get_annotations_related_to_variation
SELECT DISTINCT ba.annotation
FROM biologic_annotation ba, chromosome_variation_annotation cva, variation v
WHERE ba.id = cva.biologic_annotation_id AND cva.variation_id = v.id AND v.variation_identification = 'SNP-1.10006211.'

-- 6 - get_qtd_individuals_with_annotation
SELECT COUNT(DISTINCT(i.id)) FROM individual i, population p, variation v, chromosome_variation_annotation cva, biologic_annotation ba
WHERE ba.annotation LIKE '%expressed protein%'
AND ba.id = cva.biologic_annotation_id AND cva.variation_id = v.id AND v.population_id = p.id AND i.population_id = p.id

-- 7 - get_qtd_individuals_with_annotation
SELECT DISTINCT(i.individual_identification) FROM individual i, population p, variation v, chromosome_variation_annotation cva, biologic_annotation ba
WHERE ba.annotation LIKE '%expressed protein%'
AND ba.id = cva.biologic_annotation_id AND cva.variation_id = v.id AND v.population_id = p.id AND i.population_id = p.id

-- 8 - snps_of_a_chromosome_in_a_population_at_each_reference
SELECT r.id as reference, c.id as chromosome, COUNT(DISTINCT v.id) as quantidade
FROM variation v, chromosome_variation_annotation cva, chromosome c, reference r
WHERE v.population_id = 'rice1' AND v.id = cva.variation_id AND cva.chromosome_id = c.id
AND c.reference_id = r.id GROUP BY r.id, c.id

-- 9 - get_annotations_related_to_individual
SELECT DISTINCT(ba.annotation)
FROM biologic_annotation ba, chromosome_variation_annotation cva, variation v, population p, individual i
WHERE i.individual_identification = 'IRGC121864@0a12f8f9.0' AND i.population_id = p.id
AND p.id = v.population_id AND cva.variation_id = v.id AND ba.id = cva.biologic_annotation_id

-- 10 - get_annotations_related_to_chromosome
SELECT DISTINCT(ba.annotation)
FROM chromosome_variation_annotation cva, biologic_annotation ba
WHERE cva.chromosome_id = 3 AND cva.biologic_annotation_id = ba.id

--11 - get_annotations_related_to_position_and_populations_related_to_them
SELECT v.pos as position, ba.annotation as annotation, p.id as population
FROM biologic_annotation ba, chromosome_variation_annotation cva, variation v, population p
WHERE v.pos in ('958179', '10006042', '10007236') AND v.population_id = p.id
AND cva.variation_id = v.id AND cva.biologic_annotation_id = ba.id
GROUP BY v.pos, ba.annotation, p.id