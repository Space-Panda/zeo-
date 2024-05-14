# zeo++ helper

### zeo++_qsub.py
Generate qsub and log files based on your inputs

1. INPUT_PATH: path for your inputs (e.g. cif)
2. LOG_PATH / QSUB_PATH: path for save log & qsub files
3. ZEO_PATH: path of ./zeo++-0.3/network
4. RES_PATH / SA_PATH / VOL_PATH: path for each zeo++ calculation

**CAUTIONS: You must check the path generation part for each calculation (e.g. res, as, vol ...)**

### zeo++_validation.py
Perform the sanity check on each calculation, and return the fail list

When you perform zeo++ calculation, the following two main problems often occur

1. Result files are not generated (Because of the Voronoi decomposition, some calculations of the same MOF can fail)
2. Fake result files are generated (Even though the Voronoi decomposition fails, empty file for calculations can be generated)

### zeo++_extraction.py
Extract the target value from the result files

**CAUTIONS: You should know about the regular expression**
