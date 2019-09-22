from pymongo import MongoClient

try:
    conn = MongoClient()
    print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")

db = conn.snps
collection = db.chromosome
for i in range(12):
    file_name = "/home/brunocarmonia/Documents/Unifesp/ICBD/IniciacaoCientifica/references/Oryza_sativa.IRGSP-1.0.dna_rm.chromosome." + str(i + 1) + ".fa"
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
                collection.insert_one(chromosome)