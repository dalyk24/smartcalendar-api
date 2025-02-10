import csv

with open("student_dataset.csv", "r", newline="") as fin:
    with open("student_dataset_sat.csv", "w", newline="") as fout:
        reader = csv.reader(fin)
        writer = csv.writer(fout)
        for row in reader:
            (_, _, _, before, after) = row
            before = int(before)
            after = int(after)
            sat = 0
            if before == after:
                sat = 3
            elif before > after + 2:
                sat = 1
            elif before > after:
                if after <= 3:
                    sat = 1
                else:
                    sat = 2
            elif before + 2 < after:
                sat = 5
            else:
                if after >= 8:
                    sat = 5
                else:
                    sat = 4
            writer.writerow(row[:3] + [sat])