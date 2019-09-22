
CREATE TABLE REFERENCE(
	id varchar (200), -- name of the reference file
	reference_file_address varchar(200) not null,
	associated_paper_address varchar (200),
	PRIMARY KEY (id)
);

CREATE TABLE CHROMOSOME(
	id serial,
	reference_id varchar (200),
	chromosome_description varchar (200) not null,
	FOREIGN KEY (reference_id) REFERENCES REFERENCE (id),
	PRIMARY KEY (id)
);

CREATE TABLE BIOLOGIC_ANNOTATION (
	id serial,
	starting_position int not null,
	ending_position int not null,
	annotation varchar (200) not null,
	PRIMARY KEY (id)
);

CREATE TABLE POPULATION (
	id varchar(40),
	experiment varchar not null,
	PRIMARY KEY (id)
);

CREATE TABLE VARIATION (
	id varchar(40),
	reference_allele char not null,
	alternative_allele char not null,
	depth varchar (10),
	population_id varchar(40) not null,
  genotype varchar(3) ARRAY,
	PRIMARY KEY (id),
	FOREIGN KEY (population_id) REFERENCES POPULATION (id)
);

CREATE TABLE CHROMOSOME_VARIATION_ANNOTATION (
	id int,
	chromosome_id int,
	biologic_annotation_id int,
	variation_id varchar(40) default 0,
	FOREIGN KEY (chromosome_id) REFERENCES CHROMOSOME (id),
	FOREIGN KEY (biologic_annotation_id) REFERENCES BIOLOGIC_ANNOTATION (id),
	FOREIGN KEY (variation_id) REFERENCES VARIATION (id),
	PRIMARY KEY (id)

);

CREATE TABLE INDIVIDUAL (
	id varchar(40),
	description varchar (200) not null,
	phenotype varchar (200) not null,
	population_id varchar(40),
	PRIMARY KEY (id),
	FOREIGN KEY (population_id) REFERENCES POPULATION (id)
);
