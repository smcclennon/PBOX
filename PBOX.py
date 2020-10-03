# PBOX - Python Toolbox
# github.com/smcclennon/PBOX
import subprocess, sys, os, traceback
from time import sleep

data = {}
def reset_data():
    global data
    data = {
        "meta": {
            "name": "PBOX",
            "ver": "0.0.0",
            "id": "6"
        },
        "setup": {
            "os": os.name,
            "import_status": 0,
            "target_package": ""
        },
        "program": {
            "id": {
                1: {
                    "name": "Volute",
                    "description": "Force unmute your system audio",
                    "function": "program_volute()",  # eval(data["program"]["id"][1]["function"])
                    "compatibility": {
                        "supported_os": ['nt']
                    },
                    "settings": {
                        "threads": 2
                    }
                },
                2: {
                    "name": "Task Killer",
                    "description": "View and kill running processes",
                    "function": "program_taskkiller()",
                    "compatibility": {
                        "supported_os": ['nt']
                    },
                    "settings": {
                        "mode": "basic"
                    }
                },
                3: {
                    "name": "Pshell",
                    "description": "Full-fledged P0wersh3ll",
                    "compatibility": {
                        "supported_os": ['nt']
                    },
                    "function": "program_pshell()"
                },
                4: {
                    "name": "Terminal",
                    "description": "Command prompt (cannot change current working directory!)",
                    "compatibility": {
                        "supported_os": ['nt']
                    },
                    "function": "program_terminal()"
                },
                5: {
                    "name": "System Usage",
                    "description": "Basic CPU/RAM usage info",
                    "function": "program_systemusage()",
                    "compatibility": {
                        "supported_os": ['nt', 'posix']
                    },
                    "settings": {
                        "delay": 1,
                        "cpu": True,
                        "ram": True,
                        "disk": True,
                        "network": True
                    }
                }
            },
            "selected": 0
        }
    }
reset_data()


pbox_ascii = f""":::::::::  :::::::::   ::::::::  :::    :::
:+:    :+: :+:    :+: :+:    :+: :+:    :+:
+:+    +:+ +:+    +:+ +:+    +:+  +:+  +:+
+#++:++#+  +#++:++#+  +#+    +:+   +#++:+   {data["meta"]["ver"]}
+#+        +#+    +#+ +#+    +#+  +#+  +#+
#+#        #+#    #+# #+#    #+# #+#    #+#
###        #########   ########  ###    ###"""



def update():
    # -==========[ Update code ]==========-
    # Updater: Used to check for new releases on GitHub
    # github.com/smcclennon/Updater
    updater = {
        "updater_ver": "2.0.0",
        "proj": data["meta"]["name"],
        "proj_id": data["meta"]["id"],
        "current_ver": data["meta"]["ver"]
    }

    import os  # detecting OS type (nt, posix, java), clearing console window, restart the script
    from distutils.version import LooseVersion as semver  # as semver for readability
    import urllib.request, json  # load and parse the GitHub API
    import platform  # Consistantly detect MacOS
    import traceback  # Printing errors

    # Disable SSL certificate verification for MacOS (very bad practice, I know)
    # https://stackoverflow.com/a/55320961
    if platform.system() == 'Darwin':  # If MacOS
        import ssl
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            # Legacy Python that doesn't verify HTTPS certificates by default
            pass
        else:
            # Handle target environment that doesn't support HTTPS verification
            ssl._create_default_https_context = _create_unverified_https_context

    print('Checking for updates...', end='\r')
    for i in range(3):  # Try to retry the update up to 3 times if an error occurs
        try:
            with urllib.request.urlopen("https://smcclennon.github.io/api/v2/update.json") as update_api:  # internal api
                update_api = json.loads(update_api.read().decode())
                #{'name': 'X', 'github_api': {'latest_release': {'info': 'https://api.github.com/repos/smcclennon/X/releases/latest', 'release_download': 'https://github.com/smcclennon/X/releases/latest/download/X.py'}, 'all_releases': {'info': 'https://api.github.com/repos/smcclennon/X/releases'}}}


                updater["proj"] = update_api["project"][updater["proj_id"]]["name"]  # Project name
            #with urllib.request.urlopen(update_api["project"][updater["proj_id"]]["github_api"]["latest_release"]["info"]) as github_api_latest:  # Latest release details
            #    latest_info = json.loads(github_api_latest.read().decode())['tag_name'].replace('v', '')  # remove 'v' from version number (v1.2.3 -> 1.2.3)

            github_releases = json.loads(urllib.request.urlopen(update_api["project"][updater["proj_id"]]["github_api"]["all_releases"]["info"]).read().decode())  # Get latest patch notes

            break
        except Exception as e:  # If updating fails 3 times
            github_releases = {0: {'tag_name': 'v0.0.0'}}
            if str(e) == "HTTP Error 404: Not Found":  # No releases found
                break
            elif str(e) == '<urlopen error [Errno 11001] getaddrinfo failed>':  # Cannot connect to website
                break
            else:
                print('Error encountered whilst checking for updates. Full traceback below...')
                traceback.print_exc()

    if semver(github_releases[0]['tag_name'].replace('v', '')) > semver(updater["current_ver"]):
        print('Update available!      ')
        print(f'Latest Version: {github_releases[0]["tag_name"]}\n')

        changelog = []
        for release in github_releases:
            try:
                if semver(release['tag_name'].replace('v', '')) > semver(updater["current_ver"]):
                    changelog.append([release["tag_name"], release["body"]])
                else:
                    break  # Stop parsing patch notes after the current version has been met
            except TypeError:  # Incorrect version format + semver causes errors (Example: semver('Build-1'))
                pass  # Skip/do nothing
            except:  # Anything else, soft fail
                traceback.print_exc()

        for release in changelog[::-1]:  # Step backwards, print latest patch notes last
            print(f'{release[0]}:\n{release[1]}\n')

        confirm = input(str('Update now? [Y/n] ')).upper()
        if confirm != 'N':
            print(f'Downloading new file...')
            urllib.request.urlretrieve(update_api["project"][updater["proj_id"]]["github_api"]["latest_release"]["release_download"], os.path.basename(__file__)+'.update_tmp')  # download the latest version to cwd

            os.rename(os.path.basename(__file__), os.path.basename(__file__)+'.old')
            os.rename(os.path.basename(__file__)+'.update_tmp', os.path.basename(__file__))
            os.remove(os.path.basename(__file__)+'.old')
            os.system('cls||clear')  # Clear console window
            if os.name == 'nt':
                os.system('"'+os.path.basename(__file__)+'" 1')
            else:
                os.system('python3 "'+os.path.basename(__file__)+'" || python2 "'+os.path.basename(__file__)+'"')
            quit()
    # -==========[ Update code ]==========-

print(pbox_ascii)
update()


def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--user"])


def import_rescue(e):
    if 'No module named' in str(e):
        unknown_module = str(e).replace("'", "").replace("No module named ", "")
        if data["setup"]["target_package"] == unknown_module:
            data["setup"]["import_status"] == -1
        else:
            data["setup"]["target_package"] == unknown_module

        print(f'\nError: unable to import "{unknown_module}"')
        if data["setup"]["import_status"] == -1:
            input('Press enter to exit...')
            exit()
        print('Installing dependancies...')
        try:
            install_package(unknown_module)
        except Exception as e:
            print(f'\n{e}\n\nFailed to install "{unknown_module}"\nPress enter to exit...')
            input()
            exit()
    else:
        print(f'{e}\nUnknown error occurred')
        input('Press enter to exit...')
        exit()


def menu_meta():
    if data["setup"]["os"] == "nt":
        os.system('cls')
    else:
        os.system('clear')
    print(pbox_ascii)
    print("A collection of useful tools for dealing with locked-down systems")
    if data["setup"]["os"] != "nt":
        print(f'NOTICE: {data["meta"]["name"]} may not work correctly on your OS')
def program_meta():
    selected_program = data["program"]["selected"]
    print(f'\n{selected_program}. {data["program"]["id"][int(selected_program)]["name"]} - {data["program"]["id"][int(selected_program)]["description"]}\n\n')

def menu_interface():
    menu_meta()
    reset_data()
    valid_id = []
    print('')
    for program_id in data["program"]["id"]:
        valid_id.append(str(program_id))
        if data["setup"]["os"] in data["program"]["id"][program_id]["compatibility"]["supported_os"]:
            compatible = True
        else:
            compatible = False
        print(f'[{program_id if compatible else len(str(program_id))*"!"}]: {data["program"]["id"][program_id]["name"]} - {data["program"]["id"][program_id]["description"]}')
        sleep(0.1)
    try:
        selected_program = input('\nEnter a number to select a program\n> ')
    except KeyboardInterrupt:
        exit()

    if selected_program in valid_id:
        if data["setup"]["os"] in data["program"]["id"][int(selected_program)]["compatibility"]["supported_os"]:
            data["program"]["selected"] = int(selected_program)
            menu_meta()
            program_meta()
            try:
                eval(data["program"]["id"][int(selected_program)]["function"])
            except KeyboardInterrupt:
                pass
            except Exception as e:
                print(f'\n\n\n\n\n\n\nFatal error occurred: {e}\n\n')
                print('<----=----=ERROR REPORT=----=---->')
                print(f'Meta: {data["meta"]}')
                print(f'Setup status: {data["setup"]}')
                print(f'Selected program: {data["program"]["selected"]}')
                print(f'Current imports: {list(sys.modules.keys())}')
                print('<----=Full Traceback:=---->')
                print(traceback.print_exc())
                print('<----=----=ERROR REPORT=----=---->\n')
                print('\nWhoops, we have encountered an error.')
                print('\nPlease create a new Github issue and paste the jibberish above')
                print('Include steps on how to reproduce the error, so we can do the same and know if we have fixed it')
                input(f'\nPress enter to open the Github Issue page... (github.com/smcclennon/{data["meta"]["name"]}/issues)')
                import webbrowser
                webbrowser.open(f'https://github.com/smcclennon/{data["meta"]["name"]}/issues/new')
                print('Webpage open. Please check your browser!')
                input('\nPress enter again to exit...')
                exit()
        else:
            print(f'Sorry, {data["program"]["id"][int(selected_program)]["name"]} is not compatible with your OS.')
            sleep(0.7)
    else:
        print(f'Sorry, "{selected_program}" is not a valid program id"')
        sleep(0.7)



def program_volute():
    while data["setup"]["import_status"] != 1:
        data["setup"]["import_status"] = 0
        try:
            import atexit
            from threading import Thread
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            data["setup"]["import_status"] = 1
        except ImportError as e:
            import_rescue(e)

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    run = True
    def exit_handler():
        print('Shutting down Volute...')
        run = False
    atexit.register(exit_handler)

    def unmuteThread():
        while run == True:
            volume.SetMute(0, None)

    print(f'Creating {data["program"]["id"][1]["settings"]["threads"]} threads...')

    for i in range(0, data["program"]["id"][1]["settings"]["threads"]):
        Thread(target = unmuteThread).start()
    print('Success!')

    print('\nYour system is being unmuted multiple times per second')
    print('If the audio is choppy, try altering the amount of threads generated.')
    print('\nPress ENTER to stop')
    try:
        input()
    except KeyboardInterrupt:
        pass
    run = False
    atexit.unregister(exit_handler)

def program_pshell():
    #os.system('color 1f')
    os.system('powershell.exe')

def program_terminal():
    os.system('ver')
    print('(c) Microsoft Corporation. All rights reserved.\n')
    while True:
        cwd = subprocess.getoutput('echo %cd%')
        try:
            cmd = input(f'{cwd}>')
            os.system(cmd)
        except KeyboardInterrupt:
            break

def program_taskkiller():
    while True:
        if data["program"]["id"][data["program"]["selected"]]["settings"]["mode"] == 'basic':
            os.system("tasklist")
        elif data["program"]["id"][data["program"]["selected"]]["settings"]["mode"] == 'advanced':
            os.system("tasklist /v")
        print("\n- Please enter the task that you would like to kill")
        print("  Example: 'notepad.exe'")
        print("- To refresh the tasklist, press enter")
        print(f'- Mode: {data["program"]["id"][data["program"]["selected"]]["settings"]["mode"]}')
        print("  To change modes, type '.toggle'")
        term=input("\n> ")
        if term=="":
            os.system("cls")
            menu_meta()
            program_meta()
        elif term==".toggle":
            if data["program"]["id"][data["program"]["selected"]]["settings"]["mode"] == 'basic':
                data["program"]["id"][data["program"]["selected"]]["settings"]["mode"] = 'advanced'
            elif data["program"]["id"][data["program"]["selected"]]["settings"]["mode"] == 'advanced':
                data["program"]["id"][data["program"]["selected"]]["settings"]["mode"] = 'basic'
            os.system("cls")
            menu_meta()
            program_meta()
        else:
            os.system("taskkill /f /im "+term+" /t")
def program_systemusage():
    while data["setup"]["import_status"] != 1:
        data["setup"]["import_status"] = 0
        try:
            import psutil
            data["setup"]["import_status"] = 1
        except ImportError as e:
            import_rescue(e)
    while True:
        ram = dict(psutil.virtual_memory()._asdict())  # {'total': 8507539456, 'available': 1167245312, 'percent': 86.3, 'used': 7340294144, 'free': 1167245312}
        swap = dict(psutil.swap_memory()._asdict())  # (total=2097147904, used=296128512, free=1801019392, percent=14.1, sin=304193536, sout=677842944)
        for key in ["total", "used", "free"]:
            ram[key] = round(ram[key] / 1073741824, 2)
            swap[key] = round(swap[key] / 1073741824, 2)
        cpu_stats = dict(psutil.cpu_stats()._asdict())  # (ctx_switches=20455687, interrupts=6598984, soft_interrupts=2134212, syscalls=0)
        cpu_freq = dict(psutil.cpu_freq()._asdict())  # (current=931.42925, min=800.0, max=3500.0)
        cpu_cores = psutil.cpu_percent(percpu=True)  # [15.2, 11.2, 18.7, 12.4, 16.4, 16.4, 22.1, 21.3]
        i = 0
        disk_partitions = {}
        disk_usage = {}
        disk_io = {}
        for entry in psutil.disk_partitions():
            disk_partitions[i] = entry._asdict()  # {0: {'device': 'C:\\', 'mountpoint': 'C:\\', 'fstype': 'NTFS', 'opts': 'rw,fixed'}, 1: {'device': 'D:\\', 'mountpoint': 'D:\\', 'fstype': 'NTFS', 'opts': 'rw,removable'}, 2: {'device': 'E:\\', 'mountpoint': 'E:\\', 'fstype': '', 'opts': 'removable'}}
            disk_partitions[i]["opts"] = disk_partitions[i]["opts"].split(',')
            if disk_partitions[i]["opts"][0] == 'rw':
                disk_partitions[i]["opts"][0] = 'Read/Write'
            elif disk_partitions[i]["opts"][0] == 'r':
                disk_partitions[i]["opts"][0] = 'Read only'
            try:
                disk_io[i] = psutil.disk_io_counters(perdisk=True)[f"PhysicalDrive{i}"]._asdict()  # {0: {'read_count': 3849381, 'write_count': 3138262, 'read_bytes': 93119674368, 'write_bytes': 88870555136, 'read_time': 2227, 'write_time': 1318, 'error': 0}, 1: {'read_count': 238, 'write_count': 123, 'read_bytes': 2912256, 'write_bytes': 569344, 'read_time': 2, 'write_time': 37, 'error': 0}, 2: {'error': KeyError('PhysicalDrive2')}}
                disk_io[i]["error"] = 0
            except Exception as e:
                disk_io[i] = {}
                disk_io[i]["error"] = e
            try:
                disk_usage[i] = psutil.disk_usage(disk_partitions[i]["device"])._asdict()  # (total=21378641920, used=4809781248, free=15482871808, percent=22.5)
                disk_usage[i]["error"] = 0
            except Exception as e:
                disk_usage[i] = {}
                disk_usage[i]["error"] = e
                pass
            i += 1
        del i
        #disk_usage = dict(psutil.disk_usage('/')._asdict())
        net_io = {}
        for item in list(psutil.net_io_counters(pernic=True).keys()):  # ['Local Area Connection', 'Local Area Connection* 10']
            net_io[item] = psutil.net_io_counters(pernic=True)[item]._asdict()  # {'Local Area Connection': {'bytes_sent': 47484220, 'bytes_recv': 968508712, 'packets_sent': 507245, 'packets_recv': 737484, 'errin': 0, 'errout': 0, 'dropin': 0, 'dropout': 0}, 'Local Area Connection* 10': {'bytes_sent': 0, 'bytes_recv': 0, 'packets_sent': 0, 'packets_recv': 0, 'errin': 0, 'errout': 0, 'dropin': 0, 'dropout': 0}}


        net_if = {}
        for parent in psutil.net_if_addrs():
            net_if[parent] = []
            for child in psutil.net_if_addrs()[parent]:
                net_if[parent].append(child._asdict())  # {'Local Area Connection': [{'family': <AddressFamily.AF_LINK: -1>, 'address': '00-FB-BF-F5-5D-F6', 'netmask': None, 'broadcast': None, 'ptp': None}, {'family': <AddressFamily.AF_INET: 2>, 'address': '10.17.0.6', 'netmask': '255.255.0.0', 'broadcast': None, 'ptp': None}, {'family': <AddressFamily.AF_INET6: 23>, 'address': 'ff90::293b:c151:763d:e64b', 'netmask': None, 'broadcast': None, 'ptp': None}], 'Local Area Connection* 10': [{'family': <AddressFamily.AF_LINK: -1>, 'address': '2C-14-A8-EF-DB-14', 'netmask': None, 'broadcast': None, 'ptp': None}, {'family': <AddressFamily.AF_INET: 2>, 'address': '169.265.254.140', 'netmask': '255.255.0.0', 'broadcast': None, 'ptp': None}]}

        usage_print = ''
        usage_print += f'CPU usage: {psutil.cpu_percent()}% {cpu_freq["current"]/1000}GHz\n'
        for i in range(len(cpu_cores)):
            usage_print += f'  Core {i+1}: {cpu_cores[i]}%\n'
        #usage_print += f'Cores: {psutil.cpu_count(logical=False)}\n'
        usage_print += '\n'
        usage_print += f'Memory usage: {ram["used"]}/{ram["total"]}GB ({ram["percent"]}%)\n'
        usage_print += f'  Free: {ram["free"]}GB ({round(100-ram["percent"], 2)}%)\n'
        usage_print += f'Swap usage: {swap["used"]}/{swap["total"]}GB ({swap["percent"]}%)\n'
        usage_print += f'  Free: {swap["free"]}GB ({round(100-swap["percent"], 2)}%)\n'
        usage_print += '\n'
        for disk in disk_partitions:
            usage_print += f'Disk: {disk_partitions[disk]["device"]}\n'
            if disk_usage[disk]["error"] == 0:
                usage_print += f'  Filesystem: {disk_partitions[disk]["fstype"]}\n'
                usage_print += f'  Type: {disk_partitions[disk]["opts"][1].title()} ({disk_partitions[disk]["opts"][0]})\n'
                usage_print += f'  Storage: {round(disk_usage[disk]["used"]/1073741824, 2)}/{round(disk_usage[disk]["total"]/1073741824, 2)}GB ({disk_usage[disk]["percent"]}%)\n'
                usage_print += f'    Free: {round(disk_usage[disk]["free"]/1073741824, 2)}GB ({round(100-disk_usage[disk]["percent"], 2)}%)\n'
                if disk_io[disk]["error"] == 0:
                    usage_print += f'    Session Read/Write: {round(disk_io[disk]["read_bytes"]/1073741824, 2)}GB / {round(disk_io[disk]["write_bytes"]/1073741824, 2)}GB\n'
                else:
                    usage_print += f'    {disk_io[disk]["error"]}\n'
            else:
                usage_print += f'    {disk_usage[disk]["error"]}\n'
        usage_print += '\n'
        for key in list(net_io):
            try:
                usage_print += f'Network Adapter: {key}\n'
                if len(net_if[key])-1 >= 1 and "address" in net_if[key][1]:
                    usage_print += f'  IPv4: {net_if[key][1]["address"]}\n'
                if len(net_if[key])-1 >= 2 and "address" in net_if[key][2]:
                    usage_print += f'  IPv6: {net_if[key][2]["address"]}\n'
                if net_io[key]["bytes_sent"] > 0 or net_io[key]["bytes_recv"] > 0:
                    usage_print += f'  Session Download/Upload: {round(net_io[key]["bytes_recv"]/1073741824, 2)}GB / {round(net_io[key]["bytes_sent"]/1073741824, 2)}GB\n'
            except KeyError:
                pass




        menu_meta()
        program_meta()
        print(usage_print, flush=True)
        if data["program"]["id"][data["program"]["selected"]]["settings"]["delay"] <= 0:
            input('Press enter to refresh...')
        else:
            sleep(data["program"]["id"][data["program"]["selected"]]["settings"]["delay"])


if __name__ == "__main__":
    while True:
        menu_interface()