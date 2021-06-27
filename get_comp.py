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
    print("\033[0;33mVendor...\033[0;38m", end="\r")
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
            print("\033[0;32mVendor : " + cpu_vendor + " - OK\033[0;38m")
            cpus_family = []
            family_ok = False
            for cpui in cpus_vendor:
                if cpu_family == cpui["family"]:
                    family_ok = True
                    cpus_family.append(cpui)
            if family_ok:
                print("\033[0;32mFamily : " + cpu_family + " - OK\033[0;38m")
                model_ok = False
                for cpui in cpus_family:
                    if cpu_model == cpui["model"]:
                        model_ok = True
                if model_ok:
                    print("\033[0;32mModel : " + cpu_model + " - OK\033[0;38m")
                else:
                    print("\033[0;31mModel : " + cpu_model + " - Not compatible\033[0;38m")
                    win11_compat = False
            else:
                print("\033[0;31mFamily : " + cpu_family + " - Not compatible\033[0;38m")
                win11_compat = False
        else:
            print("\033[0;31mVendor : " + cpu_vendor + " - Not compatible\033[0;38m")
            win11_compat = False
else:
    print("\033[0;31mArchitecture : " + cpu_arch + " - Not compatible\033[0;38m")
    win11_compat = False

print(" ")

print("===    HARD DRIVE    ===")
dd_stats = shutil.disk_usage("C:\\")
dd_total_space = dd_stats.total / 1073741824
if dd_total_space >= 64:
    print("\033[0;32mCapacity : " + str(round(dd_total_space)) + " Go - OK\033[0;38m")
else:
    print("\033[0;31mCapacity : " + str(round(dd_total_space)) + " Go - Not compatible\033[0;38m")
    win11_compat = False

print(" ")

print("===       RAM        ===")
ram_stats = psutil.virtual_memory()
ram_total = ram_stats.total / 1073741824
if ram_total > 3:
    print("\033[0;32mTotal RAM : " + str(round(ram_total)) + " Go - OK\033[0;38m")
else:
    print("\033[0;31mTotal RAM : " + str(round(ram_total)) + " Go - Not compatible\033[0;38m")
    win11_compat = False

print(" ")

print("===      SCREEN      ===")
user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)
if (screen_height >= 720):
    print("\033[0;32mResolution : " + str(screen_width) + "x" + str(screen_height) + " - OK\033[0;38m")
else:
    print("\033[0;31mResolution : " + str(screen_width) + "x" + str(screen_height) + " - Not compatible\033[0;38m")
    win11_compat = False

print(" ")


print("===       UEFI       ===")
uefi_result = subprocess.check_output("powershell $env:firmware_type", shell=True)
if uefi_result == b'UEFI\r\n':
    print("\033[0;32mUEFI Mode : Enabled - OK\033[0;38m")
else:
    print("\033[0;31mUEFI Mode - Disabled - Not compatible\033[0;38m")
    win11_compat = False

print(" ")

print("===       TPM        ===")
tpm_result = subprocess.check_output("tpmtool getdeviceinformation", shell=True)
if str(tpm_result).split("-TPM pr\\x82sent\\xff: ")[1].split("\\r\\n")[0] == "Vrai":
    print("\033[0;32mTPM Present : Yes - OK")
    if str(tpm_result).split("-Version du TPM\\xff: ")[1].split("\\r\\n")[0] == "2.0":
        print("\033[0;32mTPM Version : 2.0 - OK\033[0;38m")
    else:
        print("\033[0;31mTPM Version : " + str(tpm_result).split("-Version du TPM\\xff: ")[1].split("\\r\\n")[0] + " - Not compatible\033[0;38m")
        win11_compat = False
else:
    print("\033[0;31mTPM Present : No - Not compatible")
    win11_compat = False

print(" ")

print("========================")
print("=        RESULT        =")
print("========================")

if win11_compat:
    print("\033[0;32mYour computer is compatible with Windows 11 !\033[0;38m")
else:
    print("\033[0;31mYour computer isn't compatible with Windows 11 !\033[0;38m")
