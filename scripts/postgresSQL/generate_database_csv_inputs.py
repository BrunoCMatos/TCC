input_files_directory = "/home/bruno/Documentos/unifesp/tcc/arquivos/commons/"
postgreSQL_csv_entry_files_directory = "/home/bruno/Documentos/unifesp/tcc/arquivos/postgreSQL/"

def generate_biologic_annotation_csv():
    biologic_annotations_file_name = input_files_directory + "all.locus_brief_info.7.0"
    biologic_annotations_entries = []

    with open(biologic_annotations_file_name, 'r') as biologic_annotations_file:
        annotation_info = biologic_annotations_file.readlines()[1:]
        i = 1
        biologic_annotations_entries.append(("%s& 0& 0& 0& intron\n") % (str(i)))
        for line in annotation_info:
            i += 1
            line_fields = line.split('\t')
            chrom = line_fields[0].split('r')[1]
            if chrom.isdigit():
                chrom = int(line_fields[0].split('r')[1])
            else:
                break
            start_position = int(line_fields[3])
            end_position = int(line_fields[4])
            annotation = line_fields[9]
            if (len(annotation.split("'")) > 0):
                annotation_aux = annotation.split("'")
                annotation = ""
                for x in annotation_aux:
                    annotation += x
                biologic_annotations_entries.append(("%s& %s& %s& %s& %s") % (str(i), chrom, start_position, end_position, annotation))

    with open(postgreSQL_csv_entry_files_directory + "biologic_annotation_table_input.csv", "w") as biologic_annotation_table_input:
        biologic_annotation_table_input.writelines(biologic_annotations_entries)

def generate_chromosome_csv():
    chromosomes_entries = []
    for i in range(12):
        chromosomes_file_name = input_files_directory + "Oryza_sativa.IRGSP-1.0.dna_rm.chromosome." + str(i + 1) + ".fa"
        reference_id = "Oryza_sativa.IRGSP-1.0.dna_rm.all_chromosomes"
        with open(chromosomes_file_name, 'r') as chromosome_file:
            chromosome_file_lines = chromosome_file.readlines()
            header_line = chromosome_file_lines[0]
            chromosome_description = header_line[1:]
            chromosomes_entries.append(("%s,%s,%s") % (str(i + 1), reference_id, chromosome_description))

    with open(postgreSQL_csv_entry_files_directory + "chromosome_table_input.csv", "w") as chromosome_table_input_file:
        chromosome_table_input_file.writelines(chromosomes_entries)

def generate_reference_csv():
    with open(postgreSQL_csv_entry_files_directory + "reference_table_input.csv", "w") as reference_table_input_file:
        dir_path = input_files_directory
        file_name = "Oryza_sativa.IRGSP-1.0.dna_rm.all_chromosomes"
        reference_entry = "%s,%s,%s" % (file_name, dir_path, 'none')
        reference_table_input_file.write(reference_entry)

def separate_biologic_annotations_by_chromosome(biologic_annotations):
    biologic_annotations_by_chromosome = {}
    for i in range(0, 13):
        biologic_annotations_by_chromosome[i] = []
    for biologic_annotation in biologic_annotations:
        biologic_annotation_fields = biologic_annotation.split('&')
        biologic_annotation_chrom = int(biologic_annotation_fields[1])
        biologic_annotations_by_chromosome[biologic_annotation_chrom].append(biologic_annotation)

    return biologic_annotations_by_chromosome

def generate_chromosome_variation_annotation_csv():
    chromosome_variation_annotation_entries = []
    with open(postgreSQL_csv_entry_files_directory + "variation_table_input.csv", "r") as variations_file:
        with open(postgreSQL_csv_entry_files_directory + "biologic_annotation_table_input.csv", "r") as biologic_annotations_file:
            variations = variations_file.readlines()
            biologic_annotations = biologic_annotations_file.readlines()
            biologic_annotations_by_chromosome = separate_biologic_annotations_by_chromosome(biologic_annotations)
            for variation in variations:
                variation_fields = variation.split(',')
                variation_chrom = int(variation_fields[1])
                variation_pos = int(variation_fields[3])
                variation_id = int(variation_fields[0])
                print(variation_id)
                has_annotation = False
                for biologic_annotation in biologic_annotations_by_chromosome[variation_chrom]:
                    biologic_annotation_fields = biologic_annotation.split('&')
                    biologic_annotation_starting_position = int(biologic_annotation_fields[2])
                    biologic_annotation_ending_position = int(biologic_annotation_fields[3])
                    biologic_annotation_chrom = int(biologic_annotation_fields[1])
                    biologic_annotation_id = int(biologic_annotation_fields[0])
                    if (biologic_annotation_starting_position <= variation_pos and biologic_annotation_ending_position >= variation_pos and variation_chrom == biologic_annotation_chrom):
                        has_annotation = True
                        chromosome_variation_annotation_entries.append(("%s,%s,%s \n") % (str(variation_chrom), str(biologic_annotation_id), str(variation_id)))

                if not has_annotation:
                    # relate to biologic annotation saved as intron
                    chromosome_variation_annotation_entries.append(("%s, %s, %s \n") % (str(variation_chrom), "1", str(variation_id)))

    with open(postgreSQL_csv_entry_files_directory + "chromosome_variation_annotation_table_input.csv", "w") as chromosome_variation_annotation_input_file:
        chromosome_variation_annotation_input_file.writelines(chromosome_variation_annotation_entries)

print("generating csv chromosomes")
generate_chromosome_csv()
print("generating csv reference")
generate_reference_csv()
print("generating csv annotations")
generate_biologic_annotation_csv()
print("generating csv chromosome variation annotations")
generate_chromosome_variation_annotation_csv()