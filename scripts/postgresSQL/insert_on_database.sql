\copy population FROM '/home/brunocarmonia/Documents/Unifesp/ICBD/csv_files_postgresSQL/inserts_population.csv' DELIMITER ',' CSV;

\copy individual FROM '/home/brunocarmonia/Documents/Unifesp/ICBD/csv_files_postgresSQL/inserts_individual.csv' DELIMITER ',' CSV;

\copy variation FROM '/home/brunocarmonia/Documents/Unifesp/ICBD/csv_files_postgresSQL/variation.csv' DELIMITER ',' CSV;

\copy CHROMOSOME_VARIATION_ANNOTATION (chromosome_id, biologic_annotation_id, variation_id) FROM '/home/brunocarmonia/Documents/Unifesp/ICBD/csv_files_postgresSQL/chromosome_variation_annotation.csv' DELIMITER ',' CSV;
