copy reference FROM '/home/bruno/Documentos/unifesp/tcc/arquivos/postgreSQL/reference_table_input.csv' DELIMITER ',' CSV;

copy chromosome FROM '/home/bruno/Documentos/unifesp/tcc/arquivos/postgreSQL/chromosome_table_input.csv' DELIMITER ',' CSV;

copy population FROM '/home/bruno/Documentos/unifesp/tcc/arquivos/postgreSQL/population_table_input.csv' DELIMITER ',' CSV;

copy individual FROM '/home/bruno/Documentos/unifesp/tcc/arquivos/postgreSQL/individual_table_input.csv' DELIMITER ',' CSV;

copy variation FROM '/home/bruno/Documentos/unifesp/tcc/arquivos/postgreSQL/variation_table_input.csv' DELIMITER ',' CSV;

copy biologic_annotation FROM '/home/bruno/Documentos/unifesp/tcc/arquivos/postgreSQL/biologic_annotation_table_input.csv' DELIMITER '&' CSV;

copy CHROMOSOME_VARIATION_ANNOTATION (chromosome_id, biologic_annotation_id, variation_id) FROM '/home/bruno/Documentos/unifesp/tcc/arquivos/postgreSQL/chromosome_variation_annotation_table_input.csv' DELIMITER ',' CSV;

