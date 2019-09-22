CREATE INDEX variation_identification_index ON variation (variation_identification);
CREATE INDEX pos_index ON variation (pos);

CREATE INDEX chromosome_variation_annotation_index ON chromosome_variation_annotation (chromosome_id, biologic_annotation_id, variation_id);

CREATE INDEX biologic_annotation_index ON biologic_annotation (annotation);