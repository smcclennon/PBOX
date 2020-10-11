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
Download the [**Latest Release**](https://github.com/smcclennon/PBOX/releases/latest/download/PBOX.py) or save the [`Master raw file`](https://raw.githubusercontent.com/smcclennon/PBOX/main/PBOX.py) (or the [`dev raw file`](https://raw.githubusercontent.com/smcclennon/PBOX/dev/PBOX.py) to test new features, may be unstable)

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
|Archiver|Windows, Linux, MacOS|Create zip archives and extract most archive types (regardless of the file extension). Supported archive extraction types: *7z (.7z), ACE (.ace), ALZIP (.alz), AR (.a), ARC (.arc), ARJ (.arj), BZIP2 (.bz2), CAB (.cab), compress (.Z), CPIO (.cpio), DEB (.deb), DMS (.dms), GZIP (.gz), LRZIP (.lrz), LZH (.lha, .lzh), LZIP (.lz), LZMA (.lzma), LZOP (.lzo), RPM (.rpm), RAR (.rar), RZIP (.rz), TAR (.tar), XZ (.xz), ZIP (.zip, .jar) and ZOO (.zoo)*|Your organisation does not allow you to create or download archives, but you need to send a bundle of files or have received an archive but cannot use it. Download archives with an alternative file extension (for example `.zip.totallynotanarchive`) and extract them with Archiver. Create zip archives with the `.z_ip` file extension using Archiver, then rename the file extension back to `.zip` to extract it using your favourite archive program, or use Archiver to extract it for you without needing to rename the file|

## Screenshots
|Program|Image|
|:-:|:-:|
|Main Menu|![Main Menu](https://smcclennon.github.io/assets/images/screenshots/PBOX/main_menu.png)|
|Volute|![Volute](https://smcclennon.github.io/assets/images/screenshots/PBOX/volute.png)|
|Task Killer|![Task Killer](https://smcclennon.github.io/assets/images/screenshots/PBOX/task_killer.png)|
|Pshell|![Pshell](https://smcclennon.github.io/assets/images/screenshots/PBOX/pshell.png)|
|Terminal|![Terminal](https://smcclennon.github.io/assets/images/screenshots/PBOX/terminal.png)|
|System Usage|![System Usage](https://smcclennon.github.io/assets/images/screenshots/PBOX/system_usage.png)|
|Archiver|![Archiver](https://smcclennon.github.io/assets/images/screenshots/PBOX/archiver.png)

*Written in Python 3.8 on Windows 10*