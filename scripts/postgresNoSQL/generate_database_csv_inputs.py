import threading

input_files_directory = "/home/bruno/Documentos/unifesp/tcc/arquivos/commons/"
postgreNoSQL_csv_entry_files_directory = "/home/bruno/Documentos/unifesp/tcc/arquivos/postgresNoSQL/"

def separate_annotation_by_chromosome(file_path):
    annotation_by_chromosome = {}
    with open(file_path, "r") as file:
        file_lines = file.readlines()
        current_chrom = 1
        for i in range(12):
            annotation_by_chromosome[i + 1] = []
        for line in file_lines[1:]:
            line_fields = line.split('\t')
            chrom = line_fields[0].split('r')[1]
            if chrom.isdigit():
                chrom = int(chrom)
            else:
                break
            start_position = int(line_fields[3])
            end_position = int(line_fields[4])
            annotation = ""
            for x in line_fields[9].split("'"):
                annotation += " %s" % x
            if(current_chrom != chrom):
                current_chrom += 1
            annotation_by_chromosome[chrom].append([start_position, end_position, annotation])

    return annotation_by_chromosome

def fill_json(variation, annotations):
    string_annotations = "["
    for annotation in annotations:
        string_annotations += "\"%s\"," % str(annotation[2])
    string_annotations = string_annotations.replace("\n", "")
    string_annotations = string_annotations[:-1] + "]"
    if len(string_annotations) > 1:
        variation_annotation_json = '\'{\"variation_identification\":"%s",\"pos\":%s,\"reference_allele\":"%s",\"alternative_allele\":"%s",\"annotations\":%s}\'' % (variation[2], variation[3], variation[4], variation[5], string_annotations)
    else:
        variation_annotation_json = '\'{\"variation_identification\":"%s",\"pos\":%s,\"reference_allele\":"%s",\"alternative_allele\":"%s"}\'' % (variation[2], variation[3], variation[4], variation[5])
    return variation_annotation_json

def func(variations, annotations, current_chrom):
    file_name = "annotations_chrom_" + str(current_chrom) + ".csv"
    print("Começando %s, tamanhos-> V: %s, A: %s" % (file_name, len(variations), len(annotations)))
    variations_annotations = []
    for variation in variations:
        annotations_from_this_variation = []
        for annotation in annotations:
            if (annotation[0] <= int(variation[3]) and annotation[1] >= int(variation[3])):
                annotations_from_this_variation.append(annotation)
        variations_annotations.append(str(variation[0]) + ";" + str(variation[1]) + ";" + fill_json(variation, annotations_from_this_variation) + ";" + str(variation[7]))

    print("Ecrevendo em " + file_name)
    with open(postgreNoSQL_csv_entry_files_directory + file_name, "w") as file:
        file.writelines(variations_annotations)

def generate_variation_biologic_annotation_csv():
    with open(postgreNoSQL_csv_entry_files_directory + "variation_table_input.csv", "r") as variations_csv:
        annotation_by_chromosome = separate_annotation_by_chromosome(input_files_directory + "all.locus_brief_info.7.0")

        variation_lines = []
        current_chrom = 1
        chrom_current_pool = {}
        while (True):
            variation_line = variations_csv.readline()
            if (len(variation_line) != 0):
                variation_line_fields = variation_line.split('\t')

            if (len(variation_line) == 0 or int(variation_line_fields[1]) != current_chrom):
                chrom_current_pool[current_chrom] = variation_lines
                print(current_chrom)
                if (current_chrom % 4 == 0):
                    threading.Thread(target=func, args=(
                    chrom_current_pool[current_chrom - 3], annotation_by_chromosome[current_chrom - 3],
                    current_chrom - 3)).start()
                    threading.Thread(target=func, args=(
                    chrom_current_pool[current_chrom - 2], annotation_by_chromosome[current_chrom - 2],
                    current_chrom - 2)).start()
                    threading.Thread(target=func, args=(
                    chrom_current_pool[current_chrom - 1], annotation_by_chromosome[current_chrom - 1],
                    current_chrom - 1)).start()
                    threading.Thread(target=func, args=(
                    chrom_current_pool[current_chrom], annotation_by_chromosome[current_chrom], current_chrom)).start()
                    chrom_current_pool = {}
                current_chrom += 1
                variation_lines = []
                variation_lines.append(variation_line_fields)
            else:
                variation_lines.append(variation_line_fields)

            if (len(variation_line) == 0):
                break

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

    with open(postgreNoSQL_csv_entry_files_directory + "chromosome_table_input.csv", "w") as chromosome_table_input_file:
        chromosome_table_input_file.writelines(chromosomes_entries)



def generate_reference_csv():
    with open(postgreNoSQL_csv_entry_files_directory + "reference_table_input.csv", "w") as reference_table_input_file:
        dir_path = input_files_directory
        file_name = "Oryza_sativa.IRGSP-1.0.dna_rm.all_chromosomes"
        reference_entry = "%s,%s,%s" % (file_name, dir_path, 'none')
        reference_table_input_file.write(reference_entry)

print("generating csv chromosomes")
generate_chromosome_csv()
print("generating csv reference")
generate_reference_csv()
print("generating csv chromosome variation annotations")
generate_variation_biologic_annotation_csv()