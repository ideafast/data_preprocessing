import glob
import csv

ecg = {}
vitals = {}

for filename in glob.glob("input/*.csv"):
    # OBTAIN DETAILS FROM THE FILENAME
    type = "vitals"
    if "ecg" in filename:
        type = "ecg"
    patch_id = ""
    #
    if type == "vitals":
        patch_id = filename.replace("_vitals.csv", "")
    else:
        patch_id = filename.replace("_ecg.csv", "")

    print("FILE NAME = " + filename)

    patch_id = patch_id[6:len(patch_id)]
    temp = patch_id[0:14]
    patch_id = patch_id.replace(temp, "")

    print("PATCH ID = " + patch_id)

    # READ THE FILE
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        if type == "vitals":
            for row in reader:
                if patch_id not in vitals:
                    vitals[patch_id] = [row, ]
                else:
                    vitals[patch_id].append(row)
        elif type == "ecg":
            for row in reader:
                value = []
                even = True
                for field in row:
                    if even:
                        try:
                            value.append(field)
                        except ValueError:
                            a = 1  # do nothing
                        even = False
                    else:
                        even = True
                        value.append(field)
                        if patch_id not in ecg:
                            ecg[patch_id] = [value, ]
                        else:
                            ecg[patch_id].append(value)
                        value = []

# CREATE VITAL FILE
for key, val in vitals.items():
    val.sort(key=lambda x: x[0])
    with open("output/" + key + "_vitals.csv", "w") as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        writer.writerows(val)

# CREATE ECG FILE
for key, val in ecg.items():
    val.sort(key=lambda x: x[0])
    with open("output/" + key + "_ecg.csv", "w") as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        writer.writerows(val)
