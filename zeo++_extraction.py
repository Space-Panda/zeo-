import re
import json
from pathlib import Path
from glob import glob

# settings
group = 'moftf_hmof_1'
res_path = f'./{group}/res'
sa_path = f'./{group}/sa'
vol_path = f'./{group}/vol'
fail_path = f'./{group}/{group}_fail_list.txt'

# path sanity check
res_path = Path(res_path).resolve()
sa_path = Path(sa_path).resolve()
vol_path = Path(vol_path).resolve()
fail_path = Path(fail_path).resolve()

if not res_path.exists() or not sa_path.exists() or not vol_path.exists():
    raise ValueError()

mof_list = list(f.stem for f in res_path.glob('*.res'))
fail_list = []
with open(fail_path, 'r') as f:
    lines = f.readlines()
    for line in lines:
        fail_list.append(line.strip())

# data extraction
res_output = {}

i = 1
for mof in mof_list:
    if mof in fail_list:
        print(f'res: {i}/{len(mof_list)}', flush=True)
        i += 1
        continue

    with open(f'{res_path}/{mof}.res', 'r') as f:
        line = f.readline().strip()
        di, df, _, dif = line.split('    ')[1].split(' ')

        res_output[mof] = {'di':di, 'df':df, 'dif':dif}

    # break
    print(f'res: {i}/{len(mof_list)}', flush=True)
    i += 1
    

sa_output = {}

i = 1
for mof in mof_list:
    if mof in fail_list:
        print(f'res: {i}/{len(mof_list)}', flush=True)
        i += 1
        continue

    with open(f'{sa_path}/{mof}.sa', 'r') as f:
        data = f.read()
        prop = re.search(r"ASA_m\^2/cm\^3: (?P<num>[0-9.]+)", data)
        
        sa_output[mof] = {'sa':float(prop.group('num'))}

    # break
    print(f'sa: {i}/{len(mof_list)} ({mof})', flush=True)    
    i += 1

vol_output = {}

i = 1
for mof in mof_list:
    if mof in fail_list:
        print(f'res: {i}/{len(mof_list)}', flush=True)
        i += 1
        continue

    with open(f'{vol_path}/{mof}.vol', 'r') as f:
        data = f.read()
        prop_1 = re.search(r"Unitcell_volume: (?P<num>[0-9.]+)", data)
        prop_2 = re.search(r"Density: (?P<num>[0-9.]+)", data)
        prop_3 = re.search(r"AV_Volume_fraction: (?P<num>[0-9.]+)", data)

        vol_output[mof] = {'cv':float(prop_1.group('num')), 'density':float(prop_2.group('num')), 'vf':float(prop_3.group('num'))}

    # break
    print(f'vol: {i}/{len(mof_list)}', flush=True)
    i += 1

with open(f'/home/users/kimjuneho4/foundation_mof/zeo++/{group}/{group}_res.json', 'w') as f:
    json.dump(res_output, f)

with open(f'/home/users/kimjuneho4/foundation_mof/zeo++/{group}/{group}_sa.json', 'w') as f:
    json.dump(sa_output, f)

with open(f'/home/users/kimjuneho4/foundation_mof/zeo++/{group}/{group}_vol.json', 'w') as f:
    json.dump(vol_output, f)



