from pymongo import MongoClient

try:
    conn = MongoClient()
    print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")

db = conn.snps
collection = db.individual

csv_file = open('/home/brunocarmonia/Documents/Unifesp/ICBD/csv_files_mongo/inserts_individual.csv', 'r')
collection.drop()
header = ["id", "individual_identification", "description", "phenotype", "population_id"]

individuals = []
for csv_line in csv_file.readlines():
    csv_line = csv_line[:-1]
    individual = {}
    for key, value in zip(header, csv_line.split(',')):
        individual[key] = value
    individuals.append(individual)

collection.insert_many(individuals)
