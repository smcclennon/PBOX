# PBOX - Python Toolbox
# github.com/smcclennon/PBOX
import os, traceback
from time import sleep


data = {
    "meta": {
        "name": "PBOX",
        "ver": "0.2.0",
        "id": "6",
        "sentry": {
            "share_ip": False,  # Used to track unique cases of envountered errors
            "import_success": False,
            "dsn": "https://8fe72b3641fd42d69fdf8e03dc32acc5@o457336.ingest.sentry.io/5453156"
        },
        "standard_message": {
            "return_to_main_menu": "Press Ctrl+C to return to the main menu"
        }
    },
    "setup": {
        "os": (os.name)
    },
    "program": {
        "id": {
            1: {
                "name": "Volute",
                "description": "Force unmute your system audio",
                "function": "program_volute",
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
                "function": "program_taskkiller",
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
                "function": "program_pshell",
                "compatibility": {
                    "supported_os": ['nt']
                }
            },
            4: {
                "name": "Terminal",
                "description": "Command prompt (cannot change current working directory!)",
                "function": "program_terminal",
                "compatibility": {
                    "supported_os": ['nt']
                }
            },
            5: {
                "name": "System Usage",
                "description": "Basic CPU/RAM usage info",
                "function": "program_systemusage",
                "compatibility": {
                    "supported_os": ['nt', 'posix']
                },
                "settings": {
                    "delay": 1
                }
            },
            6: {
                "name": "Archiver",
                "description": "Create and extract zip files",
                "function": "program_archiver",
                "compatibility": {
                    "supported_os": ['nt', 'posix']
                },
                "settings": {
                    "zip_file_extension": ".z_ip",
                    "extract_foldername_append": "_decompressed"
                }
            }
        },
        "selected": 0
    }
}


pbox_ascii = f""":::::::::  :::::::::   ::::::::  :::    :::
:+:    :+: :+:    :+: :+:    :+: :+:    :+:
+:+    +:+ +:+    +:+ +:+    +:+  +:+  +:+
+#++:++#+  +#++:++#+  +#+    +:+   +#++:+   {data["meta"]["ver"]}
+#+        +#+    +#+ +#+    +#+  +#+  +#+
#+#        #+#    #+# #+#    #+# #+#    #+#
###        #########   ########  ###    ###"""


def smart_import(module, **kwargs):
    # https://stackoverflow.com/a/24773951
    package = kwargs.get('package', module)
    install_only = kwargs.get('install_only', False)
    import importlib
    try:
        globals()[module] = importlib.import_module(module)  # Try to import the module
        if install_only:
            del globals()[module]  # Don't allow the module to be called (essentially un-import it)
        return True
    except ImportError:
        import subprocess, sys
        print(f'Installing {package}...')
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--user", "--quiet", "--quiet"])
        except Exception as e:
            print(f'Unable to install {package}:\n{e}')
            return False
    finally:
        # https://stackoverflow.com/a/25384923
        import site
        importlib.reload(site)  # Refresh sys.path
        try:
            globals()[module] = importlib.import_module(module)  # Try to import the module
            if install_only:
                del globals()[module]  # Don't allow the module to be called (essentially un-import it)
            return True
        except ModuleNotFoundError as e:
            print(f'Unable to import {module}: {e}')
            return False



print(pbox_ascii)


# Initialise Sentry
# We use Sentry to automatically log bugs
print('Importing Sentry...', end='\r')
if smart_import('sentry_sdk', install_only=True):
    print('Initialising Sentry...', end='\r')
    import sentry_sdk
    sentry_sdk.init(
        dsn=data["meta"]["sentry"]["dsn"],
        sample_rate=1.0,
        traces_sample_rate=1.0,
        release=data["meta"]["name"]+'-'+data["meta"]["ver"],
        attach_stacktrace=True,
        with_locals=True
    )
    data["meta"]["sentry"]["import_success"] = True
    import platform
    with sentry_sdk.configure_scope() as scope:
        scope.set_context("OS", {
            "Platform": platform.platform(),
            "System": platform.system(),
            "Release": platform.release(),
            "Version": platform.version(),
            "Machine": platform.machine()
        })
        scope.set_context("data dict", {
            "all": data
        })
        sentry_user_scope = {}
        if data["meta"]["sentry"]["share_ip"]:
            import urllib.request
            try:
                print('Obtaining IP...       ', end='\r')
                sentry_user_scope["ip_address"] = urllib.request.urlopen('http://ip.42.pl/raw').read()
            except:
                pass
        try:
            print('Obtaining username...     ',end='\r')
            sentry_user_scope["username"] = (lambda: os.environ["USERNAME"] if "C:" in os.getcwd() else os.environ["USER"])()
        except:
            pass
        try:
            print('Obtaining hostname...     ', end='\r')
            sentry_user_scope["hostname"] = os.environ['COMPUTERNAME']
        except:
            pass
        scope.user = sentry_user_scope

    def bug_send(event_id, name, email, comments):
        url = 'https://sentry.io/api/0/projects/smcclennon/pbox/user-feedback/'
        headers = {'Authorization': f'DSN {data["meta"]["sentry"]["dsn"]}'}
        payload = {
            "event_id": str(event_id),
            "name": str(name),
            "email": str(email),
            "comments": str(comments)
        }
        if smart_import('requests', install_only=True):
            import requests
            response = requests.post(url, headers=headers, data=payload)
            return response
        else:
            return 'ImportError'

def bug_report():
    traceback.print_exc()
    if data["meta"]["sentry"]["import_success"]:
        event_id = sentry_sdk.last_event_id()
        if event_id != None:  # If Sentry has detected an error
            print(f'\n\nWe\'ve encountered an error. (event_id: {event_id})')
            print('Would you like to fill in a quick bug report so we can fix the bug quicker?')
            try:
                bug_report_consent = input('Fill in bug report [Y/n]: ').upper()
            except (KeyboardInterrupt, EOFError):
                bug_report_consent = 'N'
            if bug_report_consent != 'N':
                try:
                    while True:
                        print('\n[1/3] Please enter your name')
                        name = input('Name: ')
                        if len(name) > 0:
                            break
                        else:
                            print('**Please don\'t leave this field blank**')
                            sleep(1)
                    import re
                    while True:
                        print('\n[2/3] Please enter your email address (we\'ll use this to get back to you regarding your bug report)')
                        email = input('Email: ')
                        if email != None and re.match('[^@]+@[^@]+\.[^@]+', email):
                            break
                        else:
                            print('**Please enter a valid email address**')
                            sleep(1)
                    while True:
                        print('\n[3/3] Please tell us about the bug and how to reproduce it\nAdd any details that you think may help us find what\'s causing the bug\nIf you can remember, please include steps to reproduce the bug')
                        comments = input('Bug details: ')
                        if comments != None and len(comments) >= 10:
                            break
                        else:
                            print('**Please type at least 10 characters**')
                            sleep(1)
                except (KeyboardInterrupt, EOFError):
                    print('Bug report cancelled')
                    return

                print('Sending bug report...')
                try:
                    response = bug_send(event_id, name, email, comments)
                    if str(response) == '<Response [200]>':
                        print(f'Bug report sent successfully! Thank you for helping contribute towards {data["meta"]["name"]}')
                    elif str(response) == '<Response [400]>':
                        print('We weren\'t able to recieve your bug report because there was a problem with it. This is typically an invalid field')
                    elif str(response) == 'ImportError':
                        print('We were unable to import required modules for sending the bug report')
                    elif response != None:
                        print(f'We weren\'t able to recieve your bug report: {response.status_code} {response.reason}')
                    else:
                        print('We weren\'t able to recieve your bug report')
                except (KeyboardInterrupt, SystemExit, EOFError):
                    pass
                except:
                    print('Unable to send bug report')
            else:
                return  # Exit function if user chose not to fill in a bug report


# If sentry loaded successfully, check if an error has occurred at exit, and prompt the user to fill in a bug report if an error has occurred
if data["meta"]["sentry"]["import_success"]:
    import atexit
    atexit.register(bug_report)

def update():
    # -==========[ Update code ]==========-
    # Updater: Used to check for new releases on GitHub
    # github.com/smcclennon/Updater

    # ===[ Constant Variables ]===
    updater = {
        "proj": data["meta"]["name"],
        "proj_id": data["meta"]["id"],
        "current_ver": data["meta"]["ver"]
    }

    # ===[ Changing code ]===
    updater["updater_ver"] = "2.0.4"
    import os  # detecting OS type (nt, posix, java), clearing console window, restart the script
    from distutils.version import LooseVersion as semver  # as semver for readability
    import urllib.request, json  # load and parse the GitHub API, download updates
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

    for i in range(3):  # Try to retry the update up to 3 times if an error occurs
        print(f'Checking for updates...({i+1})', end='\r')
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

    if github_releases != [] and semver(github_releases[0]['tag_name'].replace('v', '')) > semver(updater["current_ver"]):
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
            except KeyboardInterrupt:
                return  # Exit the function
            except:  # Anything else, soft fail
                traceback.print_exc()

        for release in changelog[::-1]:  # Step backwards, print latest patch notes last
            print(f'{release[0]}:\n{release[1]}\n')

        try:
            confirm = input(str('Update now? [Y/n] ')).upper()
        except KeyboardInterrupt:
            confirm = 'N'
        if confirm != 'N':
            print('Downloading new file...')
            try:
                urllib.request.urlretrieve(update_api["project"][updater["proj_id"]]["github_api"]["latest_release"]["release_download"], os.path.basename(__file__)+'.update_tmp')  # download the latest version to cwd
            except KeyboardInterrupt:
                return  # Exit the function
            os.rename(os.path.basename(__file__), os.path.basename(__file__)+'.old')
            os.rename(os.path.basename(__file__)+'.update_tmp', os.path.basename(__file__))
            os.remove(os.path.basename(__file__)+'.old')
            os.system('cls||clear')  # Clear console window
            if os.name == 'nt':
                os.system('"'+os.path.basename(__file__)+'" 1')  # Open the new file on Windows
            else:
                os.system('python3 "'+os.path.basename(__file__)+'" || python "'+os.path.basename(__file__)+'"')  # Open the new file on Linux/MacOS
            quit()
    # -==========[ Update code ]==========-

update()



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
    valid_id = []
    print('')
    for program_id in data["program"]["id"]:
        valid_id.append(str(program_id))
        if data["setup"]["os"] in data["program"]["id"][program_id]["compatibility"]["supported_os"]:
            compatible = True
        else:
            compatible = False
        print(f'[{program_id if compatible else len(str(program_id))*"!"}]: {data["program"]["id"][program_id]["name"]} - {data["program"]["id"][program_id]["description"]}')
        sleep(0.02)
    try:
        selected_program = input('\nEnter a number and press enter to choose a program\n> ')
    except (KeyboardInterrupt, EOFError):
        exit()

    if selected_program in valid_id:
        if data["setup"]["os"] in data["program"]["id"][int(selected_program)]["compatibility"]["supported_os"]:
            data["program"]["selected"] = int(selected_program)
            menu_meta()
            program_meta()
            try:
                program_function = data["program"]["id"][int(selected_program)]["function"]
                globals()[program_function]()
            except (KeyboardInterrupt, EOFError):
                pass
        else:
            print(f'Sorry, {data["program"]["id"][int(selected_program)]["name"]} is not compatible with your OS.')
            sleep(1.2)
    elif selected_program.lower() == 'a number':
        print('Very funny.')
        sleep(0.8)
    else:
        print(f'Sorry, "{selected_program}" is not a valid program id"')
        sleep(0.8)



def program_volute():
    from threading import Thread
    from ctypes import cast, POINTER

    if (smart_import('comtypes', install_only=True) != True
    or smart_import('pycaw', install_only=True) != True):
        sleep(5)
        return  # Exit the function

    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    data["program"]["id"][1]["settings"]["active_threads"] = 0

    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'

    def unmuteThread():
        thread_id = data["program"]["id"][1]["settings"]["active_threads"]
        while thread_id <= data["program"]["id"][1]["settings"]["active_threads"]:
            volume.SetMute(0, None)

    print('How Volute works:')
    print('-  Volute creates threads, which are like mini background programs. These are used to unmute your system.')
    print('-  Each thread contains a loop which sends an unmute signal to your system over and over again.')
    print('-  Volute is only useful for combatting other applications continuously muting your system')

    print('\nHow many threads should I use?')
    print('-  Continuously sending unmute signals can lead to a lot of CPU usage, especially with more threads.')
    print('-  You should increase/decrease threads according to how choppy your audio is.')
    print('-  If your machine begins to lag or become hotter than usual, kill some Volute threads immediately.')

    print('\n== Controls ==')
    print('-  Create 1 thread: Press enter')
    print('-  Kill 1 thread: Press Ctrl+C')
    print('   To exit Volute and return to the main menu, kill all active threads\n')

    # Start initial threads
    for i in range(0, data["program"]["id"][1]["settings"]["threads"]):
        data["program"]["id"][1]["settings"]["active_threads"] += 1
        Thread(target = unmuteThread).start()

    while True:
        try:
            print(f'Active threads: {data["program"]["id"][1]["settings"]["active_threads"]} ', end='')
            try:
                input()
                print(CURSOR_UP_ONE + ERASE_LINE, end='\r')
                data["program"]["id"][1]["settings"]["active_threads"] += 1
                Thread(target = unmuteThread).start()
            except (KeyboardInterrupt, EOFError):
                print(ERASE_LINE, end='\r')
                data["program"]["id"][1]["settings"]["active_threads"] -= 1
                if data["program"]["id"][1]["settings"]["active_threads"] <= 0:
                    print('Shutting down Volute...')
                    break
        except:  # If the computer is very slow and a KeyboardInterrupt is sent during the previous exception handle
            pass  # Ignore and try the While loop again


    # Prevent PBOX immediately exiting on return to the main menu due to user holding down Ctrl+C
    while True:
        try:
            sleep(1)  # Try to sleep for 1 second
            break  # If Ctrl+C does not interrupt the sleep, exit the loop
        except KeyboardInterrupt:  # If Ctrl+C is still held down, loop again
            print('** Please let go of Ctrl+C **', end='\r')

def program_pshell():
    #os.system('color 1f')
    print('Type "exit" to return to the main menu\n')
    os.system('powershell.exe')

def program_terminal():
    print(data["meta"]["standard_message"]["return_to_main_menu"])
    os.system('ver')
    print('(c) Microsoft Corporation. All rights reserved.\n')
    import subprocess
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
        print(f'\n- Mode: {data["program"]["id"][data["program"]["selected"]]["settings"]["mode"]}')
        print("  To change modes, type '.toggle'")
        print("\nPress enter to refresh the tasklist")
        print(data["meta"]["standard_message"]["return_to_main_menu"])
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
    if smart_import('psutil', install_only=True) != True:
        sleep(5)
        return
    import psutil
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
            elif disk_partitions[i]["opts"][0] == 'ro':
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
        print(data["meta"]["standard_message"]["return_to_main_menu"])
        if data["program"]["id"][data["program"]["selected"]]["settings"]["delay"] <= 0:
            input('Press enter to refresh...')
        else:
            sleep(data["program"]["id"][data["program"]["selected"]]["settings"]["delay"])

def program_archiver():
    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'

    while True:
        if (data["setup"]["os"] != 'nt'
            or smart_import("easygui", install_only=True) != True):
            gui = False
            sleep(1)
        else:
            import easygui
            gui = True

        mode = None
        target_file_path = None

        def settings_print():
            final_print = ''
            if gui == True:
                final_print += 'Interface: GUI'
            elif gui == False:
                final_print += 'Interface: CLI'
            if mode == '1':
                final_print += '\nMode: **Create archive**'
                final_print += '\nSupported filetypes: ZIP'
            elif mode == '2':
                final_print += '\nMode: **Extract archive**'
                final_print += '\nSupported filetypes: ZIP'
            if target_file_path != None:
                final_print += f'\nTarget file: {target_file_path}'
            return final_print

        def clean_console():
            os.system('cls||clear')
            menu_meta()
            program_meta()
            print(settings_print())

        print('What is Archiver?')
        print('-  Archiver can create and extract zip files without needing the correct file extension.')
        print('-  This is useful if your organisation blocks the creation of .zip\n')

        print('-  **Known bug: When Keyboard Interrupting (Ctrl+C) during file selection, future interrupts get stuck**')
        print('-  **Temporary fix: To Keyboard Interrupt in the future, you may need to press return (enter) after interrupting**')

        print(data["meta"]["standard_message"]["return_to_main_menu"])

        print('\nWhat would you like to do?')
        print('1. Create an archive')
        print('2. Extract an archive\n')
        while True:
            try:
                mode = str(input('> '))
            except (EOFError):
                pass  # Ignore
            if mode != '1' and mode != '2':
                print('Please choose "1" or "2"')
                sleep(1)
                print(CURSOR_UP_ONE + ERASE_LINE, end='\r')
                print(CURSOR_UP_ONE + ERASE_LINE, end='\r')
            else:
                break


        import zipfile

        while True:
            clean_console()

            if gui == False:
                print('\n'+data["meta"]["standard_message"]["return_to_main_menu"])
                print('\nEnter the full path to the target file')
                print('Example: C:\\Users\\PBOX\\Downloads\\homework')

            elif mode == '1':
                print('\nPlease select a folder using the GUI file picker')
                print('All files within the selected folder will be added to the archive')
                print('To switch to the CLI file picker, exit the file picker GUI without selecting a file')

            elif mode == '2':
                print('\nPlease select the archive file using the GUI file picker')
                print('To switch to the CLI file picker, exit the file picker GUI without selecting a file')


            while True:
                if not gui: target_file_path = str(input('> '))

                elif mode == '1':
                    try:
                        target_file_path = easygui.diropenbox()  # Select any folder
                    except KeyboardInterrupt:
                        print('KeyboardInterrupt recieved whilst the GUI was open. To KeyboardInterrupt again, you may need to also press enter')
                        sleep(3)
                elif mode == '2':
                    try:
                        target_file_path = easygui.fileopenbox()  # Select any file
                    except KeyboardInterrupt:
                            print('KeyboardInterrupt recieved whilst the GUI was open. To KeyboardInterrupt again, you may need to also press enter')
                            sleep(3)

                if gui and target_file_path == None:
                    gui = False
                    print('**No file selected in GUI mode. Switching to CLI mode**')
                    sleep(1)
                    break
                else:
                    if mode == '1' and os.path.isdir(target_file_path):
                        break
                    if os.path.isfile(target_file_path):
                        break
                print('Invalid filepath. Please try again.')
                sleep(1.2)
                print(CURSOR_UP_ONE + ERASE_LINE, end='\r')
                print(CURSOR_UP_ONE + ERASE_LINE, end='\r')

            if target_file_path != None:  # If GUI filepicker did not exit without choosing a file, or CLI file picker was used
                break

        target_file_basename = os.path.basename(target_file_path)  # 'C:\users\PBOX\desktop\coolfile.2019.png' -> 'coolfile.2019.png'
        target_file_basename_no_ext = os.path.splitext(target_file_basename)[0]  # 'coolfile.2019.png' -> 'coolfile.2019'

        try:
            clean_console()
            print('\n'+data["meta"]["standard_message"]["return_to_main_menu"])
            print('\nProcessing...')

            if mode == '1':
                # https://stackoverflow.com/a/27992144/9457576
                file_output = target_file_basename+data["program"]["id"][6]["settings"]["zip_file_extension"]
                with zipfile.ZipFile(file_output, "w", zipfile.ZIP_DEFLATED) as zf:
                    abs_src = os.path.abspath(target_file_path)
                    i = 0
                    for dirname, subdirs, files in os.walk(target_file_path):
                        for filename in files:
                            absname = os.path.abspath(os.path.join(dirname, filename))
                            arcname = absname[len(abs_src) + 1:]
                            i += 1
                            print(f'{i}. Zipping: {os.path.join(dirname, filename)}\nAs: {arcname}\n')
                            try:
                                zf.write(absname, arcname)
                            except PermissionError as e:
                                print(e)


            elif mode =='2':
                file_output = target_file_basename+data["program"]["id"][6]["settings"]["extract_foldername_append"]
                if not os.path.exists(file_output):
                    os.makedirs(file_output)
                with zipfile.ZipFile(target_file_path, 'r') as zf:
                    zf.extractall(file_output)
            print('Done!\n')
            print(f'Find your files at: {os.path.abspath(file_output)}')
            if mode == '1':
                print('Add the file extension .zip to your file to extract it using the program of your choice')
                print('If you are unable to rename your file, you can use this program to extract it for you')

        except KeyboardInterrupt:
            print('Operation cancelled')
        except zipfile.BadZipFile as e:
            if str(e) == 'File is not a zip file':
                print('The archive you selected is not supported.')
                print(f'Supported archive extraction types: .zip')
            else:
                print('The archive you selected is corrupt')
            print(e)
            print(f'\nWe created the folder {file_output} which we were going to put your decompressed files into. It\'s likely empty as the archive failed. You might want to delete it.')
        try:
            input('\nPress enter to return to the menu')
        except (EOFError):
            pass
        menu_meta()
        program_meta()



def file_downloader():
    print('Download files with an alternative file extension')

if __name__ == "__main__":
    try:
        while True:
            menu_interface()
    except Exception as e:
        if data["meta"]["sentry"]["import_success"]:
            sentry_sdk.capture_exception(e)
        bug_report()

    input('\n\nPress enter to exit')
    os._exit(1)  # force kill task and all threads