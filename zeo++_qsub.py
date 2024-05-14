from pathlib import Path
from glob import glob
import subprocess
from tqdm import tqdm

# parameters #####################
input_path = '/home/users/kimjuneho4/foundation_mof/moftf_hmof_2_cif/success'
log_path = '/home/users/kimjuneho4/foundation_mof/zeo++/moftf_hmof_2/moftf_hmof_2_log'
qsub_path= '/home/users/kimjuneho4/foundation_mof/zeo++/moftf_hmof_2/moftf_hmof_2_qsub'
sa_path = '/home/users/kimjuneho4/foundation_mof/zeo++/moftf_hmof_2/sa'
res_path = '/home/users/kimjuneho4/foundation_mof/zeo++/moftf_hmof_2/res'
vol_path = '/home/users/kimjuneho4/foundation_mof/zeo++/moftf_hmof_2/vol'
# run_path = '/home/users/kimjuneho4/foundation_mof/grid_gen.py'
zeo_path = '/home/users/kimjuneho4/zeo++-0.3/network'
group = 'moftf_hmof_2'

NUM_QSUB = 49
NUM_CORE = 1
CORE = 'aa'
##################################

# obtain python path
python_path = subprocess.check_output("which python", shell=True).strip()
python_path = python_path.decode('utf-8')
print(python_path)

# obtain absolute path
input_path = Path(input_path).resolve()
log_path = Path(log_path).resolve()
qsub_path = Path(qsub_path).resolve()
# run_path = Path(run_path).resolve()
zeo_path = Path(zeo_path).resolve()
sa_path = Path(sa_path).resolve()
res_path = Path(res_path).resolve()
vol_path = Path(vol_path).resolve()

# error: path does not exist
if not input_path.exists():
    raise ValueError()

if not zeo_path.exists():
    raise ValueError()

# make path
log_path.mkdir(exist_ok=True, parents=True)
qsub_path.mkdir(exist_ok=True, parents=True)
sa_path.mkdir(exist_ok=True, parents=True)
res_path.mkdir(exist_ok=True, parents=True)
vol_path.mkdir(exist_ok=True, parents=True)

n = len(list(input_path.glob('*.cif'))) // NUM_QSUB

def write_qsub(cif_path, N):

    qsub_file = qsub_path / f"{group}_{N}.qsub"
    log_file = log_path / f'{group}_log_{N}.out'

    if not log_file.exists():
        with open(log_file, 'w') as t:
            t.write(f'{group}_log_{N} start!\n')

    if not qsub_file.exists():
        with open(qsub_file, 'w') as f:
            f.write("#!/bin/sh\n")
            f.write("#PBS -r n\n")
            f.write("#PBS -q long\n")
            f.write(f"#PBS -l nodes=1:ppn={NUM_CORE}:{CORE}\n")
            f.write("cd $PBS_O_WORKDIR\n\n")


    with open(qsub_file, 'a') as f:
        sa_save_path = sa_path / f'{cif_path.stem}.sa'
        res_save_path = res_path / f'{cif_path.stem}.res'
        vol_save_path = vol_path / f'{cif_path.stem}.vol'

        f.write(f'{str(zeo_path)} -ha -sa 1.2 1.2 2000 {str(sa_save_path)} {str(cif_path)} 1>>{log_file} 2>&1\n')
        f.write(f'{str(zeo_path)} -ha -res {str(res_save_path)} {str(cif_path)} 1>>{log_file} 2>&1\n')
        f.write(f'{str(zeo_path)} -ha -vol 1.2 1.2 50000 {str(vol_save_path)} {str(cif_path)} 1>>{log_file} 2>&1\n')

for i, cif_path in tqdm(enumerate(input_path.glob('*.cif'))):
    N = i // n
    write_qsub(cif_path, N)


    