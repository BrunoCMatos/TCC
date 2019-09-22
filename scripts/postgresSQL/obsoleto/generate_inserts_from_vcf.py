import psycopg2

def generate_insert_population(population_id, description):
    query = "INSERT INTO POPULATION VALUES ('%s', '%s');" % (population_id, description)
    cursor.execute(query)
    conn.commit()


def generate_insert_individuals(individual_id, population_id, description, phenotype):
    query = "INSERT INTO INDIVIDUAL VALUES ('%s', '%s', '%s', '%s');" % (individual_id, description, phenotype, population_id)
    cursor.execute(query)
    conn.commit()


def generate_insert_genotype(individual_id, population_id, variation_id, genotype, depth):
    query = "INSERT INTO GENOTYPE VALUES ('%s', '%s', '%s', '%s', '%s');" % (population_id, individual_id, variation_id, genotype, depth)
    cursor.execute(query)
    conn.commit()


def generate_insert_variations(line_fields, vcf_fields, format_fields, population_id, individuals):
    query = "INSERT INTO VARIATION VALUES ('%s', '%s', '%s', '%s', '%s');" % (vcf_fields["ID"][1], vcf_fields["REF"][1], vcf_fields["ALT"][1], " ",population_id)
    cursor.execute(query)
    conn.commit()


    for individual_id, individual in zip(individuals, line_fields[vcf_fields["FORMAT"][0] + 1:]):
        individual_fields = individual.split(':')
        if "DP" in format_fields.keys():
            generate_insert_genotype(individual_id, population_id, vcf_fields["ID"][1], individual_fields[format_fields["GT"]], individual_fields[format_fields["DP"]])
        else:
            generate_insert_genotype(individual_id, population_id, vcf_fields["ID"][1], individual_fields[format_fields["GT"]], ".")

#main

conn_string = "host='localhost' dbname='BIODATA' user='carmonia' password='CarmoniaPower'"
conn = psycopg2.connect(conn_string)

cursor = conn.cursor()


vcf_path = "/Users/carmonia/Documents/saida3.vcf"
population_id = "rice1"
description_population = "rice"

generate_insert_population(population_id, description_population)

#initializing dictionary
vcf_fields = {}
vcf_fields["ID"] = [0] * 2
vcf_fields["REF"] = [0] * 2
vcf_fields["ALT"] = [0] * 2
vcf_fields["FORMAT"] = [0] * 2
vcf_fields["CHROM"] = [0] * 2

with open(vcf_path, 'r') as vcf_file:
    vcf_lines = vcf_file.readlines()

    #pass through metadata lines
    i = 0
    for line in vcf_lines:
        if(line[1] != '#'):
            break
        i = i + 1

    #process header line
    line = vcf_lines[i]
    i = i + 1
    header_fields = line.split('\t')

    for index, field in enumerate(header_fields):
        if field in vcf_fields.keys():
            vcf_fields[field][0] = index

        if field == "FORMAT":
            break

    individuals = []
    #process individuals id
    for individual in header_fields[vcf_fields["FORMAT"][0] + 1:]:
        generate_insert_individuals(individual, population_id, " ", " ")
        individuals.append(individual)

    #detach information
    for line in vcf_lines[i:]:
        line_fields = line.split('\t')

        for field in vcf_fields.keys():
            vcf_fields[field][1] = line_fields[vcf_fields[field][0]]

        #process information contained in the format field
        format_field_information = vcf_fields["FORMAT"][1].split(':')
        format_fields = {}
        for index, information in enumerate(format_field_information):
            format_fields[information] = index

        generate_insert_variations(line_fields, vcf_fields, format_fields, population_id, individuals)
