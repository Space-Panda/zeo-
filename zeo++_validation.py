import os
from pathlib import Path
from glob import glob

# settings
group = 'E0_hmof'
cif_path = f'../{group}_cif/success'
res_path = f'./{group}/res'
sa_path = f'./{group}/sa'
vol_path = f'./{group}/vol'

# path sanity check
cif_path = Path(cif_path).resolve()
res_path = Path(res_path).resolve()
sa_path = Path(sa_path).resolve()
vol_path = Path(vol_path).resolve()

if not cif_path.exists() or not res_path.exists() or not sa_path.exists() or not vol_path.exists():
    raise ValueError()

cif_list = list(f.stem for f in cif_path.glob('*.cif'))
res_list = list(f.stem for f in res_path.glob('*.res'))
sa_list = list(f.stem for f in sa_path.glob('*.sa'))
vol_list = list(f.stem for f in vol_path.glob('*.vol'))

# sanity check
fail = []

i = 1
for cif in cif_list:
    # check generation
    if (cif not in res_list) or (cif not in sa_list) or (cif not in vol_list):
        fail.append(cif)
        print(f'MOF: {i}/{len(cif_list)}', flush=True)
        i += 1
    # check fake generation
    else:           
        res_file_path = f'{res_path}/{cif}.res'
        sa_file_path = f'{sa_path}/{cif}.sa'
        vol_file_path = f'{vol_path}/{cif}.vol'

        res_file_size = os.path.getsize(res_file_path)
        sa_file_size = os.path.getsize(sa_file_path)
        vol_file_size = os.path.getsize(vol_file_path)

        if res_file_size == 0 or sa_file_size == 0 or vol_file_size == 0:
            fail.append(cif)

        print(f'MOF: {i}/{len(cif_list)}', flush=True)
        i += 1

with open(f'./{group}_fail_list.txt', 'w') as f:
    for cif in fail:
        f.write(cif+'\n')

