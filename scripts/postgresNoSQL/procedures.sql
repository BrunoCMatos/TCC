CREATE OR REPLACE FUNCTION function_to_search_3(TEXT, TEXT) RETURNS INDIVIDUAL[]
/*$1 - variation_identification; $2 - position*/
LANGUAGE plpgsql
AS $$
DECLARE
var_genotypes jsonb;
var_individual_ids INTEGER[] DEFAULT ARRAY[] :: INTEGER[];
var_alternative_allele CHAR;
var_genotype TEXT;
var_indivual_id INTEGER := 1;
var_current_index INTEGER := 0;
var_population_id TEXT;
var_individual INDIVIDUAL;
var_individuals INDIVIDUAL[] DEFAULT ARRAY[] :: INDIVIDUAL[];
BEGIN
  SELECT snp_annotation->'genotype', population_id INTO var_genotypes, var_population_id FROM variation v WHERE v.snp_annotation->>'variation_identification' = $1 AND v.snp_annotation->>'pos' = $2;
  FOR var_genotype IN SELECT * FROM jsonb_array_elements_text(var_genotypes)
  LOOP
     IF substring(var_genotype from 1 for 1) != substring(var_genotype from 3 for 1) THEN
      var_individual_ids[var_current_index] := var_indivual_id;
      var_current_index := var_current_index + 1;
     END IF;
     var_indivual_id := var_indivual_id + 1;
  END LOOP;
  var_indivual_id := 0;
  var_current_index := 0;
  FOREACH var_indivual_id IN ARRAY var_individual_ids
  LOOP
    SELECT i.* INTO var_individual FROM individual i WHERE i.population_id = var_population_id AND i.id = var_indivual_id;
    var_individuals[var_current_index] := var_individual;
    var_current_index := var_current_index + 1;
  END LOOP;
  RETURN var_individuals;
END
$$;

CREATE OR REPLACE FUNCTION function_to_search_6(INTEGER, TEXT) RETURNS BOOLEAN
/*$1 - chromosome_id; $2 - population_id*/
LANGUAGE plpgsql
AS $$
DECLARE
var_genotype TEXT;
var_individual_id INTEGER := 1;
var_individual TEXT;
var_variations VARIATION;
var_group_0_0 INTEGER [] DEFAULT ARRAY[] :: INTEGER[];
var_group_0_1 INTEGER [] DEFAULT ARRAY[] :: INTEGER[];
var_group_1_0 INTEGER [] DEFAULT ARRAY[] :: INTEGER[];
var_group_1_1 INTEGER [] DEFAULT ARRAY[] :: INTEGER[];
BEGIN
  /*SELECT v.chrom, v.variation_identification, v.pos, v.reference_allele, v.alternative_allele, v.depth, v.population_id, v.genotypes INTO var_chrom, var_variation_identification, var_pos, var_reference_allele, var_alternative_allele, var_depth, var_population_id, var_genotype FROM variation v, chromosome_variation_annotation cva, chromosome c WHERE c.id = $1 AND v.id = cva.variation_id AND c.id = cva.chromosome_id AND v.population_id = '$2'
*/
  FOR var_variations IN SELECT DISTINCT v.* FROM variation v, chromosome c WHERE c.id = $1 AND c.id = v.chrom AND v.population_id = $2
  LOOP
    var_group_0_0 := ARRAY[] :: INTEGER[];
    var_group_0_1 := ARRAY[] :: INTEGER[];
    var_group_1_0 := ARRAY[] :: INTEGER[];
    var_group_1_1 := ARRAY[] :: INTEGER[];
    /*raise notice 'Variation: %', var_variations.id;*/
    var_individual_id := 1;
    FOR var_genotype IN SELECT * FROM jsonb_array_elements_text(var_variations.snp_annotation->'genotype')
    LOOP
       IF substring(var_genotype from 1 for 3) = '0/0' THEN
        var_group_0_0 := array_append(var_group_0_0, var_individual_id);
       ELSIF substring(var_genotype from 1 for 3) = '0/1' THEN
        var_group_0_1 := array_append(var_group_0_1, var_individual_id);
       ELSIF substring(var_genotype from 1 for 3) = '1/0' THEN
        var_group_1_0 := array_append(var_group_1_0, var_individual_id);
       ELSIF substring(var_genotype from 1 for 3) = '1/1' THEN
        var_group_1_1 := array_append(var_group_1_1, var_individual_id);
       END IF;
       var_individual_id := var_individual_id + 1;
    END LOOP;

    /*raise notice '0/0: %', array_length(var_group_0_0, 1);
    raise notice '0/1: %', array_length(var_group_0_1, 1);
    raise notice '1/0: %', array_length(var_group_1_0, 1);
    raise notice '1/1: %', array_length(var_group_1_1, 1);*/

    FOR var_individual_id IN SELECT DISTINCT * FROM UNNEST(var_group_0_0)
    LOOP
      SELECT (i.individual_identification, i.phenotype, i.description) INTO var_individual FROM individual i WHERE i.id = var_individual_id;
      /*raise notice '0/0: %', var_individual;*/
    END LOOP;

    FOR var_individual_id IN SELECT DISTINCT * FROM UNNEST(var_group_0_1)
    LOOP
      SELECT (i.individual_identification, i.phenotype, i.description) INTO var_individual FROM individual i WHERE i.id = var_individual_id;
      /*raise notice '0/1: %', var_individual;*/
    END LOOP;

    FOR var_individual_id IN SELECT DISTINCT * FROM UNNEST(var_group_1_0)
    LOOP
      SELECT (i.individual_identification, i.phenotype, i.description) INTO var_individual FROM individual i WHERE i.id = var_individual_id;
      /*raise notice '1/0: %', var_individual;*/
    END LOOP;

    FOR var_individual_id IN SELECT DISTINCT * FROM UNNEST(var_group_1_1)
    LOOP
      SELECT (i.individual_identification, i.phenotype, i.description) INTO var_individual FROM individual i WHERE i.id = var_individual_id;
      /*raise notice '1/1: %', var_individual;*/
    END LOOP;
  END LOOP;
  RETURN TRUE;
END
$$;

CREATE OR REPLACE FUNCTION function_to_search_5(TEXT, TEXT) RETURNS BOOLEAN
/*$1 - population_id*, *$2 - annotation */
LANGUAGE plpgsql
AS $$
DECLARE
var_genotype TEXT;
var_quantidade_0_0 INTEGER := 0;
var_quantidade_0_1 INTEGER := 0;
var_quantidade_1_0 INTEGER := 0;
var_quantidade_1_1 INTEGER := 0;
var_individual TEXT;
var_variation VARIATION;
BEGIN
   FOR var_variation IN SELECT v.* FROM variation v WHERE v.population_id = $1 AND v.snp_annotation->>'annotations' LIKE '%' || $2 || '%'
    LOOP
      /*raise notice 'Variation: %', var_variation.id;*/
      FOR var_genotype IN SELECT * FROM jsonb_array_elements_text(var_variation.snp_annotation->'genotype')
      LOOP
        IF substring(var_genotype from 1 for 3) = '0/0' THEN
         var_quantidade_0_0 := var_quantidade_0_0 + 1;
        ELSIF substring(var_genotype from 1 for 3) = '0/1' THEN
         var_quantidade_0_1 := var_quantidade_0_1 + 1;
        ELSIF substring(var_genotype from 1 for 3) = '1/0' THEN
         var_quantidade_1_0 := var_quantidade_1_0 + 1;
        ELSIF substring(var_genotype from 1 for 3) = '1/1' THEN
         var_quantidade_1_1 := var_quantidade_1_1 + 1;
        END IF;
      END LOOP;
      /*raise notice '0/0: %', (var_quantidade_0_0);
      raise notice '0/1: %', (var_quantidade_0_1);
      raise notice '1/0: %', (var_quantidade_1_0);
      raise notice '1/1: %', (var_quantidade_1_1);*/
      var_quantidade_0_0 = 0;
      var_quantidade_0_1 = 0;
      var_quantidade_1_0 = 0;
      var_quantidade_1_1 = 0;
    END LOOP;
  RETURN TRUE;
END
$$;

CREATE OR REPLACE FUNCTION function_to_search_7(TEXT, TEXT) RETURNS INDIVIDUAL []
/*$1 - population_id*, *$2 - annotation */
LANGUAGE plpgsql
AS $$
DECLARE
var_genotype TEXT;
var_individual_id INTEGER := 1;
var_individual INDIVIDUAL;
var_variation VARIATION;
var_heterozygous INTEGER [] DEFAULT ARRAY[] :: INTEGER[];
var_individuals INDIVIDUAL [] DEFAULT ARRAY[] :: INDIVIDUAL[];
var_variation_individuals TEXT [] DEFAULT ARRAY[] :: TEXT[];
BEGIN
  FOR var_variation IN SELECT v.* FROM variation v WHERE v.population_id = $1 AND v.snp_annotation->>'annotations' LIKE '%' || $2 || '%'
  LOOP
    var_individual_id := 1;
    FOR var_genotype IN SELECT * FROM jsonb_array_elements_text(var_variation.snp_annotation->'genotype')
    LOOP
       IF substring(var_genotype from 1 for 3) = '0/1' OR substring(var_genotype from 1 for 3) = '1/0' THEN
         var_heterozygous := array_append(var_heterozygous, var_individual_id);
       END IF;
       var_individual_id := var_individual_id + 1;
    END LOOP;
  END LOOP;
  FOR var_individual_id IN SELECT DISTINCT * FROM UNNEST(var_heterozygous)
  LOOP
    SELECT i.* INTO var_individual FROM individual i WHERE i.id = var_individual_id;
    var_individuals := array_append(var_individuals, var_individual);
  END LOOP;
  RETURN var_individuals;
END
$$;
/*Corrigir posição*/
CREATE OR REPLACE FUNCTION function_to_search_10(TEXT, INT) RETURNS TEXT[]
/*$1 - position*, *$2 - chromosome_id */
LANGUAGE plpgsql
AS $$
DECLARE
var_variation VARIATION;
var_population POPULATION;
var_annotation_population_array TEXT[] DEFAULT ARRAY[] :: TEXT[];
BEGIN
  FOR var_variation IN SELECT v.* FROM variation v WHERE v.snp_annotation->>'pos' = $1 AND v.chrom = $2
  LOOP
    var_annotation_population_array = array_append(var_annotation_population_array, CAST (var_variation.snp_annotation->>'annotations' AS TEXT));
    FOR var_population IN SELECT DISTINCT p.* FROM population p WHERE var_variation.population_id = p.id
    LOOP
      var_annotation_population_array = array_append(var_annotation_population_array, CAST (var_population.id AS TEXT));
    END LOOP;
  END LOOP;
  RETURN var_annotation_population_array;
END
$$;
