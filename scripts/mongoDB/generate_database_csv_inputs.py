import json
import threading

# importar csv grande: mongoimport --db snps --collection variation --file /home/bruno/Documentos/unifesp/tcc/arquivos/mongoDB/annotations_chrom_1.json

input_files_directory = "/home/bruno/Documentos/unifesp/tcc/arquivos/commons/"
mongoDB_csv_entry_files_directory = "/home/bruno/Documentos/unifesp/tcc/arquivos/mongoDB/"

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
    variation_annotation_json = {
        "id" : variation[0],
        "chrom" : variation[1]
    }
    if len(string_annotations) > 1:
        variation_annotation_json["variation_identification"] = variation[2]
        variation_annotation_json["pos"] = variation[3]
        variation_annotation_json["reference_allele"] = variation[4]
        variation_annotation_json["alternative_allele"] = variation[5]
        variation_annotation_json["annotations"] = string_annotations
    else:
        variation_annotation_json["variation_identification"] = variation[2]
        variation_annotation_json["pos"] = variation[3]
        variation_annotation_json["reference_allele"] = variation[4]
        variation_annotation_json["alternative_allele"] = variation[5]

    # [:-1] é pra ignorar o \n do final da linha
    variation_annotation_json["population_id"] = str(variation[7][:-1])
    return variation_annotation_json

def func(variations, annotations, current_chrom):
    file_name = "annotations_chrom_" + str(current_chrom) + ".json"
    print("Começando %s, tamanhos-> V: %s, A: %s" % (file_name, len(variations), len(annotations)))
    variations_annotations = []
    for variation in variations:
        annotations_from_this_variation = []
        for annotation in annotations:
            if (annotation[0] <= int(variation[3]) and annotation[1] >= int(variation[3])):
                annotations_from_this_variation.append(annotation)
        variations_annotations.append(fill_json(variation, annotations_from_this_variation))

    print("Persistindo chromossomo " + str(current_chrom))
    with open(mongoDB_csv_entry_files_directory + file_name, "w") as output:
        for variations_annotation in variations_annotations:
            json.dump(variations_annotation, output)
            output.write('\n')

def generate_variation_biologic_annotation_csv():
    variations_csv = open(mongoDB_csv_entry_files_directory + "variation_table_input.csv", "r")
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
    with open(mongoDB_csv_entry_files_directory + "chromosome_table_input.json", 'w') as output:
        for i in range(12):
            file_name = input_files_directory + "Oryza_sativa.IRGSP-1.0.dna_rm.chromosome." + str(i + 1) + ".fa"
            reference_id = "Oryza_sativa.IRGSP-1.0.dna_rm.all_chromosomes"
            with open(file_name, 'r') as reference_file:
                reference_file_lines = reference_file.readlines()
                for line in reference_file_lines:
                    if line[0] == '>':
                        #print(line)
                        chromosome_description = line[1:-1]
                        chromosome = {"id" : i + 1,
                                 "reference_id" : reference_id,
                                 "chromosome_description" : chromosome_description}
                        json.dump(chromosome, output)
                        output.write('\n')

def generate_individual_csv():
    with open(mongoDB_csv_entry_files_directory + 'individual_table_input.csv', 'r') as csv_file:
        with open(mongoDB_csv_entry_files_directory + "individual_table_input.json", 'w') as output:
            header = ["id", "individual_identification", "description", "phenotype", "population_id"]
            for csv_line in csv_file.readlines():
                csv_line = csv_line[:-1]
                individual = {}
                for key, value in zip(header, csv_line.split(',')):
                    individual[key] = value
                json.dump(individual, output)
                output.write('\n')

def generate_population_csv():
    with open(mongoDB_csv_entry_files_directory + 'population_table_input.csv', 'r') as csv_file:
        with open(mongoDB_csv_entry_files_directory + "population_table_input.json", 'w') as output:
            header = ["id", "experiment"]
            for csv_line in csv_file.readlines():
                csv_line = csv_line[:-1]
                population = {}
                for key, value in zip(header, csv_line.split(',')):
                    population[key] = value
                json.dump(population, output)
                output.write('\n')

def generate_reference_csv():
    with open(mongoDB_csv_entry_files_directory + "reference_table_input.json", 'w') as output:
        for i in range(1):
            dir_path = input_files_directory
            file_name = "Oryza_sativa.IRGSP-1.0.dna_rm.all_chromosomes"
            associated_paper = "none"
            reference = {"id": file_name,
                         "reference_file_address": dir_path,
                         "associated_paper_address": associated_paper}
            json.dump(reference, output)
            output.write('\n')



#main
print("generating chromosome csv")
generate_chromosome_csv()
print("generating individual csv")
generate_individual_csv()
print("generating population csv")
generate_population_csv()
print("generating reference csv")
generate_reference_csv()
print("generating variation/annotation csv")
generate_variation_biologic_annotation_csv()