
CREATE TABLE REFERENCE(
	id varchar (200), -- name of the reference file
	reference_file_address varchar(200) not null,
	associated_paper_address varchar (200)
);

CREATE TABLE CHROMOSOME(
	id serial,
	reference_id varchar (200),
	chromosome_description varchar (200) not null
);

CREATE TABLE BIOLOGIC_ANNOTATION (
	id serial,
	starting_position int not null,
	ending_position int not null,
	annotation varchar (200) not null
);

CREATE TABLE POPULATION (
	id varchar(40),
	experiment varchar not null
);

CREATE TABLE VARIATION (
	id varchar(40),
	pos int not null,
	reference_allele char not null,
	alternative_allele char not null,
	depth varchar (10),
	population_id varchar(40) not null,
  genotype varchar(3) ARRAY
);

CREATE TABLE CHROMOSOME_VARIATION_ANNOTATION (
	id serial,
	chromosome_id int,
	biologic_annotation_id int,
	variation_id varchar(40) default 0
);

CREATE TABLE INDIVIDUAL (
	id varchar(40),
	description varchar (200) not null,
	phenotype varchar (200) not null,
	population_id varchar(40)
);
