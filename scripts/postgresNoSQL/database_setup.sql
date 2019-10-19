
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

CREATE TABLE POPULATION (
    id varchar(40),
    experiment varchar not null,
    PRIMARY KEY (id)
);

CREATE TABLE VARIATION (
    id int,
    chrom int not null,
    snp_annotation jsonb not null,
    population_id varchar(40) not null,
    PRIMARY KEY (id),
    FOREIGN KEY (population_id) REFERENCES POPULATION (id),
    FOREIGN KEY (chrom) REFERENCES CHROMOSOME (id)
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

create index snp_annotation_index ON variation USING GIN((snp_annotation));
create index only_annotation_index ON variation USING GIN((snp_annotation->'annotations'));
create index only_variation_identification_index ON variation USING GIN((snp_annotation->'variation_identification'));
create index only_pos_index ON variation USING GIN((snp_annotation->'pos'));

