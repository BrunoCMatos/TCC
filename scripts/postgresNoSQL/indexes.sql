create index snp_annotation_index ON variation USING GIN((snp_annotation));
create index only_annotation_index ON variation USING GIN((snp_annotation->'annotations'));
create index only_variation_identification_index ON variation USING GIN((snp_annotation->'variation_identification'));
create index only_pos_index ON variation USING GIN((snp_annotation->'pos'));