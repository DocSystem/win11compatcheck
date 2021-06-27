### CPUs Lists:
##  https://docs.microsoft.com/en-us/windows-hardware/design/minimum/supported/windows-11-supported-intel-processors
##  https://docs.microsoft.com/en-us/windows-hardware/design/minimum/supported/windows-11-supported-amd-processors
##  https://docs.microsoft.com/en-us/windows-hardware/design/minimum/supported/windows-11-supported-qualcomm-processors

import json

cpus = []

print("Input CPUs from Microsoft's website:")

while True:
    cpu = input()
    cpu = cpu.replace("®", "(R)")
    cpu = cpu.replace("™", "(TM)")
    if (cpu != ""):
        cpu_data = cpu.split("\t")
        cpus.append({ "vendor": cpu_data[0], "family": cpu_data[1], "model": cpu_data[2] })
    else:
        break

with open('compatible_cpus.json', 'w') as f:
    json.dump(cpus, f)
