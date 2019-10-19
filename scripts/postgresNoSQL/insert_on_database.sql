copy reference FROM '/home/bruno/Documentos/unifesp/tcc/arquivos/postgresNoSQL/reference_table_input.csv' DELIMITER ',' CSV;

copy chromosome FROM '/home/bruno/Documentos/unifesp/tcc/arquivos/postgresNoSQL/chromosome_table_input.csv' DELIMITER ',' CSV;

copy population FROM '/home/bruno/Documentos/unifesp/tcc/arquivos/postgresNoSQL/population_table_input.csv' DELIMITER ',' CSV;

copy individual FROM '/home/bruno/Documentos/unifesp/tcc/arquivos/postgresNoSQL/individual_table_input.csv' DELIMITER ',' CSV;

copy variation FROM '/home/bruno/Documentos/unifesp/tcc/arquivos/postgresNoSQL/annotations_chrom_1.csv' DELIMITER ';' CSV QUOTE E'\'';
copy variation FROM '/home/bruno/Documentos/unifesp/tcc/arquivos/postgresNoSQL/annotations_chrom_2.csv' DELIMITER ';' CSV QUOTE E'\'';
copy variation FROM '/home/bruno/Documentos/unifesp/tcc/arquivos/postgresNoSQL/annotations_chrom_3.csv' DELIMITER ';' CSV QUOTE E'\'';
copy variation FROM '/home/bruno/Documentos/unifesp/tcc/arquivos/postgresNoSQL/annotations_chrom_4.csv' DELIMITER ';' CSV QUOTE E'\'';
copy variation FROM '/home/bruno/Documentos/unifesp/tcc/arquivos/postgresNoSQL/annotations_chrom_5.csv' DELIMITER ';' CSV QUOTE E'\'';
copy variation FROM '/home/bruno/Documentos/unifesp/tcc/arquivos/postgresNoSQL/annotations_chrom_6.csv' DELIMITER ';' CSV QUOTE E'\'';
copy variation FROM '/home/bruno/Documentos/unifesp/tcc/arquivos/postgresNoSQL/annotations_chrom_7.csv' DELIMITER ';' CSV QUOTE E'\'';
copy variation FROM '/home/bruno/Documentos/unifesp/tcc/arquivos/postgresNoSQL/annotations_chrom_8.csv' DELIMITER ';' CSV QUOTE E'\'';
copy variation FROM '/home/bruno/Documentos/unifesp/tcc/arquivos/postgresNoSQL/annotations_chrom_9.csv' DELIMITER ';' CSV QUOTE E'\'';
copy variation FROM '/home/bruno/Documentos/unifesp/tcc/arquivos/postgresNoSQL/annotations_chrom_10.csv' DELIMITER ';' CSV QUOTE E'\'';
copy variation FROM '/home/bruno/Documentos/unifesp/tcc/arquivos/postgresNoSQL/annotations_chrom_11.csv' DELIMITER ';' CSV QUOTE E'\'';
copy variation FROM '/home/bruno/Documentos/unifesp/tcc/arquivos/postgresNoSQL/annotations_chrom_12.csv' DELIMITER ';' CSV QUOTE E'\'';
