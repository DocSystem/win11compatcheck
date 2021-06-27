import shutil
import psutil
import ctypes
import os
import subprocess
import json

win11_compat = True

print("===       CPU        ===")
print("\033[0;33mArchitecture...\033[0;38m", end="\r")
cpu_arch = str(subprocess.check_output("powershell -Command $ProgressPreference = 'SilentlyContinue' ; $(Get-ComputerInfo).CsProcessors.Architecture", shell=False)).split("b'")[1].split("\\r\\n")[0]
if cpu_arch == "x64":
    # On continue, pour le moment c'est compatible
    print("\033[0;32mArchitecture : " + cpu_arch + " - OK\033[0;38m")
    print("\033[0;33mMarque...\033[0;38m", end="\r")
    cpu_name = str(subprocess.check_output("powershell -Command $ProgressPreference = 'SilentlyContinue' ; $(Get-ComputerInfo).CsProcessors.Name", shell=False)).split("b'")[1].split("\\r\\n")[0]
    cnp = cpu_name.split(" ")
    cpu_vendor = cnp[0]
    cpu_family = cnp[1]
    cpu_model = cnp[2]
    with open("compatible_cpus.json", "r") as f:
        cpus = json.load(f)
        cpus_vendor = []
        vendor_ok = False
        for cpui in cpus:
            if cpu_vendor == cpui["vendor"]:
                vendor_ok = True
                cpus_vendor.append(cpui)
        if vendor_ok:
            print("\033[0;32mMarque : " + cpu_vendor + " - OK\033[0;38m")
            cpus_family = []
            family_ok = False
            for cpui in cpus_vendor:
                if cpu_family == cpui["family"]:
                    family_ok = True
                    cpus_family.append(cpui)
            if family_ok:
                print("\033[0;32mFamille : " + cpu_family + " - OK\033[0;38m")
                model_ok = False
                for cpui in cpus_family:
                    if cpu_model == cpui["model"]:
                        model_ok = True
                if model_ok:
                    print("\033[0;32mModèle : " + cpu_model + " - OK\033[0;38m")
                else:
                    print("\033[0;31mModèle : " + cpu_model + " - Incompatible\033[0;38m")
                    win11_compat = False
            else:
                print("\033[0;31mFamille : " + cpu_family + " - Incompatible\033[0;38m")
                win11_compat = False
        else:
            print("\033[0;31mMarque : " + cpu_vendor + " - Incompatible\033[0;38m")
            win11_compat = False
else:
    print("\033[0;31mArchitecture : " + cpu_arch + " - Incompatible\033[0;38m")
    win11_compat = False

print(" ")

print("===    DISQUE DUR    ===")
dd_stats = shutil.disk_usage("C:\\")
dd_total_space = dd_stats.total / 1073741824
if dd_total_space >= 64:
    print("\033[0;32mCapacité : " + str(round(dd_total_space)) + " Go - OK\033[0;38m")
else:
    print("\033[0;31mCapacité : " + str(round(dd_total_space)) + " Go - Incompatible\033[0;38m")
    win11_compat = False

print(" ")

print("===       RAM        ===")
ram_stats = psutil.virtual_memory()
ram_total = ram_stats.total / 1073741824
if ram_total > 3:
    print("\033[0;32mMémoire vive : " + str(round(ram_total)) + " Go - OK\033[0;38m")
else:
    print("\033[0;31mMémoire vive : " + str(round(ram_total)) + " Go - Incompatible\033[0;38m")
    win11_compat = False

print(" ")

print("===      ECRAN       ===")
user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)
if (screen_height >= 720):
    print("\033[0;32mRésolution : " + str(screen_width) + "x" + str(screen_height) + " - OK\033[0;38m")
else:
    print("\033[0;31mRésolution : " + str(screen_width) + "x" + str(screen_height) + " - Incompatible\033[0;38m")
    win11_compat = False

print(" ")


print("===       UEFI       ===")
uefi_result = subprocess.check_output("powershell $env:firmware_type", shell=True)
if uefi_result == b'UEFI\r\n':
    print("\033[0;32mUEFI Mode : Activé - OK\033[0;38m")
else:
    print("\033[0;31mUEFI Mode - Désactivé - Incompatible\033[0;38m")
    win11_compat = False

print(" ")

print("===       TPM        ===")
tpm_result = subprocess.check_output("tpmtool getdeviceinformation", shell=True)
if str(tpm_result).split("-TPM pr\\x82sent\\xff: ")[1].split("\\r\\n")[0] == "Vrai":
    print("\033[0;32mTPM Présent : Oui - OK")
    if str(tpm_result).split("-Version du TPM\\xff: ")[1].split("\\r\\n")[0] == "2.0":
        print("\033[0;32mVersion du TPM : 2.0 - OK\033[0;38m")
    else:
        print("\033[0;31mVersion du TPM : " + str(tpm_result).split("-Version du TPM\\xff: ")[1].split("\\r\\n")[0] + " - Incompatible\033[0;38m")
        win11_compat = False
else:
    print("\033[0;31mTPM Présent : Non - Incompatible")
    win11_compat = False

print(" ")

print("========================")
print("=       RESULTAT       =")
print("========================")

if win11_compat:
    print("\033[0;32mVotre PC est compatible avec Windows 11 !\033[0;38m")
else:
    print("\033[0;31mVotre PC n'est pas compatible avec Windows 11 !\033[0;38m")
