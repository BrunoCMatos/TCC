
CREATE TABLE REFERENCE(
	id varchar (200),
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
	chrom int,
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
	id int,
	chrom int not null,
	variation_identification varchar(40) unique,
	pos int not null,
	reference_allele char not null,
	alternative_allele char not null,
	depth varchar (10),
	population_id varchar(40) not null,
	PRIMARY KEY (id),
	FOREIGN KEY (population_id) REFERENCES POPULATION (id)
);

CREATE TABLE CHROMOSOME_VARIATION_ANNOTATION (
	id serial,
	chromosome_id int,
	biologic_annotation_id int,
	variation_id int default 0,
	FOREIGN KEY (chromosome_id) REFERENCES CHROMOSOME (id),
	FOREIGN KEY (biologic_annotation_id) REFERENCES BIOLOGIC_ANNOTATION (id),
	FOREIGN KEY (variation_id) REFERENCES VARIATION (id),
	PRIMARY KEY (id)

);

CREATE TABLE INDIVIDUAL (
	id int,
	individual_identification varchar(40) unique,
	description varchar (200) not null,
	phenotype varchar (200) not null,
	population_id varchar(40),
	PRIMARY KEY (id),
	FOREIGN KEY (population_id) REFERENCES POPULATION (id)
);

CREATE INDEX variation_identification_index ON variation (variation_identification);
CREATE INDEX pos_index ON variation (pos);
CREATE INDEX chromosome_variation_annotation_index ON chromosome_variation_annotation (chromosome_id, biologic_annotation_id, variation_id);
CREATE INDEX biologic_annotation_index ON biologic_annotation (annotation);