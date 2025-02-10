import csv

with open("fitlife_emotional_dataset.csv", "r", newline="") as fin:
    with open("student_dataset.csv", "w", newline="") as fout:
        reader = csv.reader(fin)
        writer = csv.writer(fout)
        types = {}
        next(reader, None)
        for row in reader:
            (_, _, _, _, occupation, time, type, _, _, duration, _, _, _, before, after, _, _) = row
            if occupation == "Student":
                if types.get(type):
                    type = types[type]
                else:
                    types[type] = input(type + ": ")
                    type = types[type]
                writer.writerow([time, type, duration, before, after])
