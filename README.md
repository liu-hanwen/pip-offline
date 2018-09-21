# pip-offline
Automatically download packages and generate install.sh for Python packages offline installations.

## Requirements

1. An online machine with Python and pip
2. An offline machine with Python and pip

## Usage

```shell
python pip-offline.py [-i PKG_NAME1 PKG_NAME2...] [-o OUTPUT_PATH] [-n OUTPUT_NAME] [-f OUTPUT_FORMAT]
```

### Arguments
  
- -i: Download packages list.
- -o: Output path, should be available. (default: ./)
- -n: Output name, should not have suffix. (default: offline_installer)
- -f: Output format, can only be [tar, tar.gz, tar.bz2, zip]. (default: tar)


## Example

- Step1: Download or clone the project on the online machine.
- Step2: Using the pip-offline.py to generate an offline-installer.
- Step3: Transfer the offline-installer to the offline machine.
- Step4: Run the install.sh in the installer.

```shell
# On the online machine
git clone https://github.com/liu-hanwen/pip-offline.git
cd pip-offline
python pip-offline.py -o /tmp -n offline_installer -f tar.gz -i pandas flask
```

```shell
# On the offline machine
tar -xf offline_installer.tar
cd offline_installer
sh install.sh
```
