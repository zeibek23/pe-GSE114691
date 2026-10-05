import pandas as pd

# ----- Get the metadata from the 1st Script -----
meta = pd.read_csv("data/processed/metadata.csv", index_col="gsm")
print(meta.shape)
print(meta.head(5))

# ----- Read the four count files -----
ctrl = pd.read_csv("data/raw/GSE114691_MasterCount_ControlONLY.txt", sep="\t", index_col=0)
print(ctrl.shape)
print(ctrl.head(10))
print(ctrl.iloc[:3, :5])

pe = pd.read_csv("data/raw/GSE114691_MasterCount_PEONLY.txt", sep="\t", index_col=0)
print(pe.shape)
print(pe.head(10))
print(pe.iloc[:3, :5])

pe_iugr = pd.read_csv("data/raw/GSE114691_MasterCount_PEIUGR.txt", sep="\t", index_col=0)
print(pe_iugr.shape)
print(pe_iugr.head(10))
print(pe_iugr.iloc[:3, :5])

iugr = pd.read_csv("data/raw/GSE114691_MasterCount_IUGRONLY.txt",sep="\t", index_col=0 )
print(iugr.shape)
print(iugr.head(10))
print(iugr.iloc[:3, :5])

# ----- Same rows, same order -----
assert list(ctrl.index) == list(pe.index)
assert list(pe_iugr.index) == list(pe.index)
assert list(iugr.index) == list(pe.index)

# ----- Glue side by side -----
counts = pd.concat([ctrl, pe, pe_iugr, iugr], axis=1)
print (counts.shape)
print(counts.head(5))

# ----- Every metadata code must exist in counts -----
missing = []
for code in meta["sample_code"]:
    if code not in counts.columns:
        missing.append(code)
print("codes in metadata but not in counts:", missing)
assert len(missing) == 0

# ----- Columns in counts that are NOT in metadata -----
codes = list(meta["sample_code"])      # Series -> plain list, so 'in' checks the values

extra = []
for col in counts.columns:             # walk through the 79 column names of counts
    if col not in codes:               # is this column name missing from metadata?
        extra.append(col)              # yes -> remember it

print("columns in counts but not in metadata:", extra)
assert len(extra) == 0                 # must be empty: 21+20+20+18 = 79 = len(meta)

# ----- Put columns in metadata order, rename to GSM -----
counts = counts[meta["sample_code"]]
assert list(counts.columns) == list(meta["sample_code"])
counts.columns = meta.index
print(counts.iloc[:3, :4])

# ----- Are these RAW counts?? -----
print(counts.dtypes.value_counts())

# ----- SAVING -----
counts.to_csv("data/processed/counts_transcript.csv")
print("saved data/processed/counts_transcript.csv  shape:", counts.shape)