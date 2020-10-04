# PBOX
Collection of useful tools for dealing with locked-down systems, all within one Python file.

Some tools within PBOX have come from my other repository, [PYBY-Toolbox](https://github.com/smcclennon/PYBY-Toolbox)

[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/smcclennon/PBOX.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/smcclennon/PBOX/context:python)
[![Maintainability](https://api.codeclimate.com/v1/badges/a4e85e15988e4dab380f/maintainability)](https://codeclimate.com/github/smcclennon/PBOX/maintainability)
[![License](https://img.shields.io/github/license/smcclennon/PBOX)](LICENSE)
[![GitHub last commit](https://img.shields.io/github/last-commit/smcclennon/PBOX)](https://github.com/smcclennon/PBOX/commits)
[![HitCount](https://hits.dwyl.com/smcclennon/PBOX.svg)](https://hits.dwyl.com/smcclennon/PBOX)

## Features
- Multiple useful programs inside one, portable python file
- Automatically install required dependancies
- Automatically update PBOX when there is a new GitHub release
- Intuitive menu system. Exit any PBOX program (except Pshell) with a Keyboard Interrupt (`CTRL+C`) and return to the PBOX menu

## Installation
Download the [Latest Release](https://github.com/smcclennon/PBOX/releases/latest/download/PBOX.py) or save the [Latest Raw File](https://raw.githubusercontent.com/smcclennon/PBOX/master/PBOX.py)

#### Requirements:
- Python 3.6+
- Windows 10 for all features, Linux/MacOS for limited features

## Programs available in PBOX
|Script|OS|About|Usage case|
|:-:|:-:|:-|:--|
|Volute|Windows Only|Force unmute your system by using multiple threads to continuously unmute your system sound|A volume block as been put in place but you require audio, for example personal music or a video on an online course|
|Task Killer|Windows Only|List running task image names, PIDs, memory usage and more; kill tasks via their image name|Task manager has been disabled or placed behind UAC, and there is a runaway task or a hidden/background task you don't need running that is using resources|
|Pshell|Windows Only|Call `powershell.exe` from within python|Command Prompt/PwrShell  have been disabled and you require a full-feature command line|
|Terminal|Windows Only|Run Command Prompt commands via `os.system` and print the output. Bypass "Command Prompt disabled by your administrator". Does not support changing directory.|Command Prompt has been disabled and you require a basic command line (with no current working directory changing support)
|System Usage|Windows, Linux, MacOS|View CPU usage for each core; memory and swap usage; all fixed and removable disks storage usage, session read/write totals; IP address for each network adapter, session download/upload totals|Task manager has been disabled and you would like to view system resource usage|

## Screenshots
|Program|Image|
|:-:|:-:|
|Main Menu|![Main Menu](https://smcclennon.github.io/assets/images/screenshots/PBOX/main_menu.png)|
|Volute|![Volute](https://smcclennon.github.io/assets/images/screenshots/PBOX/volute.png)|
|Task Killer|![Task Killer](https://smcclennon.github.io/assets/images/screenshots/PBOX/task_killer.png)|
|Pshell|![Pshell](https://smcclennon.github.io/assets/images/screenshots/PBOX/pshell.png)|
|Terminal|![Terminal](https://smcclennon.github.io/assets/images/screenshots/PBOX/terminal.png)|
|System Usage|![System Usage](https://smcclennon.github.io/assets/images/screenshots/PBOX/system_usage.png)|

*Written in Python 3.8 on Windows 10*