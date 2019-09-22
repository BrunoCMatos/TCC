
CREATE TABLE REFERENCE(
	id varchar, -- name of the reference file
	reference_file_address varchar not null,
	associated_paper_address varchar
);

CREATE TABLE CHROMOSOME(
	id int,
	reference_id varchar,
	chromosome_description varchar not null
);

CREATE TABLE BIOLOGIC_ANNOTATION (
	id serial,
	chrom int,
	starting_position int not null,
	ending_position int not null,
	annotation varchar not null
);

CREATE TABLE POPULATION (
	id varchar,
	experiment varchar not null
);

CREATE TABLE VARIATION (
	id int,
	chrom int not null,
	variation_identification varchar unique,
	pos int not null,
	reference_allele char not null,
	alternative_allele char not null,
	depth varchar,
	population_id varchar not null,
  genotype varchar(3) ARRAY
);

CREATE TABLE CHROMOSOME_VARIATION_ANNOTATION (
	id serial,
	chromosome_id int,
	biologic_annotation_id int,
	variation_id int default 0
);

CREATE TABLE INDIVIDUAL (
	id int,
	individual_identification varchar,
	description varchar not null,
	phenotype varchar not null,
	population_id varchar
);
