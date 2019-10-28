-- 1 - snps_in_a_experiment
SELECT DISTINCT v.snp_annotation->>'variation_identification'
FROM variation v
WHERE v.population_id = 'rice1'
AND v.chrom IN (SELECT c.id FROM chromosome c WHERE c.reference_id = 'Oryza_sativa.IRGSP-1.0.dna_rm.all_chromosomes')

-- 2 - get_all_snps_of_a_chromosome
SELECT v.snp_annotation->>'variation_identification'
FROM variation v
WHERE v.chrom = 3

-- 3 - get_annotations_of_a_population
SELECT v.snp_annotation->>'annotations'
FROM variation v
WHERE v.snp_annotation ? 'annotations' AND v.population_id = 'rice1'

-- 4 - variation_related_to_biologic_annotation
SELECT DISTINCT v.snp_annotation->>'variation_identification', v.population_id
FROM variation v
WHERE v.snp_annotation ->>'annotations' LIKE '%expressed protein%'

-- 5 - get_annotations_related_to_variation
SELECT DISTINCT v.snp_annotation->>'annotations'
FROM variation v
WHERE v.snp_annotation ->'variation_identification' ? 'SNP-1.10006211.'

-- 6 - get_qtd_individuals_with_annotation
SELECT COUNT(DISTINCT(i.id))
FROM individual i, population p, variation v
WHERE v.snp_annotation ->>'annotations' LIKE '%expressed protein%' AND v.population_id = p.id AND i.population_id = p.id

-- 7 - get_qtd_individuals_with_annotation
SELECT DISTINCT(i.individual_identification)
FROM individual i, population p, variation v
WHERE v.snp_annotation ->>'annotations' LIKE '%expressed protein%' AND v.population_id = p.id AND i.population_id = p.id

-- 8 - snps_of_a_chromosome_in_a_population
SELECT r.id as reference, c.id as chromosome, COUNT(DISTINCT v.id) as quantidade
FROM variation v, chromosome c, reference r
WHERE v.population_id = 'rice1' AND v.chrom = c.id AND c.reference_id = r.id GROUP BY r.id, c.id

-- 9 - get_annotations_related_to_individual
SELECT v.snp_annotation->>'annotations'
FROM variation v, population p, individual i
WHERE v.snp_annotation ? 'annotations' AND i.individual_identification = 'IRGC121864@0a12f8f9.0'
AND i.population_id = p.id AND p.id = v.population_id

-- 10 - get_annotations_related_to_chromosome
SELECT v.snp_annotation->>'annotations'
FROM variation v
WHERE v.chrom = 3 AND v.snp_annotation ? 'annotations'

--11 - get_annotations_related_to_position_and_populations_related_to_them
SELECT v.snp_annotation->>'pos' as position, v.snp_annotation->>'annotations' as annotation, p.id as population
FROM variation v, population p
WHERE v.snp_annotation @>'{"pos" : 958179}'
OR v.snp_annotation @>'{"pos" : 10006042}'
OR v.snp_annotation @>'{"pos" : 10007236}' AND v.population_id = p.id
GROUP BY v.snp_annotation->>'pos', v.snp_annotation->>'annotations', p.id