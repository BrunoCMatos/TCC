\copy variation FROM '/home/brunocarmonia/Documents/Unifesp/ICBD/csv_files_postgresNoSQL/annotations_chrom_1.csv' DELIMITER ';' CSV QUOTE E'\'';
\copy variation FROM '/home/brunocarmonia/Documents/Unifesp/ICBD/csv_files_postgresNoSQL/annotations_chrom_2.csv' DELIMITER ';' CSV QUOTE E'\'';
\copy variation FROM '/home/brunocarmonia/Documents/Unifesp/ICBD/csv_files_postgresNoSQL/annotations_chrom_3.csv' DELIMITER ';' CSV QUOTE E'\'';
\copy variation FROM '/home/brunocarmonia/Documents/Unifesp/ICBD/csv_files_postgresNoSQL/annotations_chrom_4.csv' DELIMITER ';' CSV QUOTE E'\'';
\copy variation FROM '/home/brunocarmonia/Documents/Unifesp/ICBD/csv_files_postgresNoSQL/annotations_chrom_5.csv' DELIMITER ';' CSV QUOTE E'\'';
\copy variation FROM '/home/brunocarmonia/Documents/Unifesp/ICBD/csv_files_postgresNoSQL/annotations_chrom_6.csv' DELIMITER ';' CSV QUOTE E'\'';
\copy variation FROM '/home/brunocarmonia/Documents/Unifesp/ICBD/csv_files_postgresNoSQL/annotations_chrom_7.csv' DELIMITER ';' CSV QUOTE E'\'';
\copy variation FROM '/home/brunocarmonia/Documents/Unifesp/ICBD/csv_files_postgresNoSQL/annotations_chrom_8.csv' DELIMITER ';' CSV QUOTE E'\'';
\copy variation FROM '/home/brunocarmonia/Documents/Unifesp/ICBD/csv_files_postgresNoSQL/annotations_chrom_9.csv' DELIMITER ';' CSV QUOTE E'\'';
\copy variation FROM '/home/brunocarmonia/Documents/Unifesp/ICBD/csv_files_postgresNoSQL/annotations_chrom_10.csv' DELIMITER ';' CSV QUOTE E'\'';
\copy variation FROM '/home/brunocarmonia/Documents/Unifesp/ICBD/csv_files_postgresNoSQL/annotations_chrom_11.csv' DELIMITER ';' CSV QUOTE E'\'';
\copy variation FROM '/home/brunocarmonia/Documents/Unifesp/ICBD/csv_files_postgresNoSQL/annotations_chrom_12.csv' DELIMITER ';' CSV QUOTE E'\'';

\copy population FROM '/home/brunocarmonia/Documents/Unifesp/ICBD/csv_files_postgresNoSQL/inserts_population.csv' DELIMITER ',' CSV;

\copy individual FROM '/home/brunocarmonia/Documents/Unifesp/ICBD/csv_files_postgresNoSQL/inserts_individual.csv' DELIMITER ',' CSV;


/*
  insert into variation values(1,1,'{"variation_identification":"SNP-1.578.","pos":1579,"reference_allele":"G","alternative_allele":"A","depth":".","annotations":[],"genotype":["0/0","0/0"]}', 'rice1');

*/
