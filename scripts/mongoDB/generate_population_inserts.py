from pymongo import MongoClient

try:
    conn = MongoClient()
    print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")

db = conn.snps
collection = db.population

csv_file = open('/home/brunocarmonia/Documents/Unifesp/ICBD/csv_files_mongo/inserts_population.csv', 'r')
collection.drop()
header = ["id", "experiment"]

populations = []
for csv_line in csv_file.readlines():
    csv_line = csv_line[:-1]
    population = {}
    for key, value in zip(header, csv_line.split(',')):
        population[key] = value
    populations.append(population)

collection.insert_many(populations)
