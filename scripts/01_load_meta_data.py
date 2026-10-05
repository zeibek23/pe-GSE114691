import pandas as pd

# ----- READ THE FILE -----
matrix_file = "data/raw/GSE114691_series_matrix.txt"

lines = []

with open(matrix_file) as f:
    for line in f:
        line = line.rstrip("\n")
        lines.append(line)

print("number of the lines:", len(lines))        

# ----- FIND THE REQUIRED LINES -----
gsm_line = None
title_line = None
group_line = None

for line in lines:
    if line.startswith("!Sample_geo_accession"):
        gsm_line = line
    if line.startswith("!Sample_title"):
        title_line = line
    if line.startswith("!Sample_characteristics_ch1") and "disease group:" in line:
        group_line = line

assert gsm_line is not None
assert title_line is not None
assert group_line is not None

# ----- SPLITTING EACH LINE -----
gsm_parts = gsm_line.split("\t")
title_parts = title_line.split("\t")
group_parts = group_line.split("\t")

print(gsm_parts[0])
print(gsm_parts[1])
print(len(gsm_parts))

# ----- CLEANING THE VALUES -----
gsm = []
for value in gsm_parts[1:]:
    value = value.strip('"')
    gsm.append(value)

title = []
for value in title_parts[1:]:
    value = value.strip('"')
    title.append(value)

group = []
for value in group_parts[1:]:
    value = value.strip('"')
    value = value.replace("disease group: ", "")
    group.append(value)

# ----- BUILDING the TABLE -----
meta = pd.DataFrame()
meta["gsm"] = gsm
meta["title"] = title
meta["group"] = group
meta = meta.set_index("gsm")

print(meta.head(10))
print(meta["group"].value_counts())

# ----- SHORT GROUP CODES -----
code_map = {
    "Control": "CTRL",
    "Preeclampsia only": "PE",
    "Preeclampsia and Intrauterine Growth Restriction": "PE_IUGR",
    "Intrauterine Growth Restriction only": "IUGR",
}

meta ["group_code"] = meta["group"].map(code_map)

assert meta["group_code"].isna().sum() == 0
print(meta["group_code"].value_counts())

# ----- FIND THE DESCRIPTION LINE -----
# there are TWO !Sample_description lines; the second one says "MasterCount..."
desc_line = None
for line in lines:
    if line.startswith("!Sample_description") and "MasterCount" not in line:
        desc_line = line
assert desc_line is not None

desc_parts = desc_line.split("\t")

# ----- CLEAN INTO R-STYLE CODES -----
code = []
for value in desc_parts[1:]:
    value = value.strip('"')
    value = value.replace(" ", "")
    value = value.replace("-", ".")
    if value[0].isdigit():            # starts with a digit -> R put an X in front
        value = "X" + value
    if value == "X396.10_a":          # GEO says 396-10_a, count file says X396.10
        value = "X396.10"
    code.append(value)

meta["sample_code"] = code
assert meta["sample_code"].duplicated().sum() == 0
print(meta.head(12))

# ----- SAVING -----
meta.to_csv ("data/processed/metadata.csv")
print("saved the metadata.csv inside data/processed", meta.shape)