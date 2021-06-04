# PAINT_COLOR_SEARCH

This is a Python library for collecting Dulux and Nippon's color codes and their RGB from official websites(cn). 

## To use
- git clone from this repo. 
```bash
git clone https://github.com/ccuulinay/PAINT_COLOR_SEARCH.git
```

- Create virtual environment or conda environment. (suggested)
```bash
conda create -n myenv python=3.7 pip
```

- (Activated environment) Install required packages listed from requirements.txt
```bash
pip install -r requirements.txt
```

- Run CLI paint_color_manager.py and checkout the usage
```bash
% python paint_color_manager.py --help

Usage: paint_color_manager.py [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.

  --help                          Show this message and exit.

Commands:
  refresh-dulux-data
  refresh-nippon-data
  usage

```

- Collect Dulux colors data
```bash
% python paint_color_manager.py refresh-dulux-data
INFO: 2021-06-04 18:25:48,492: paint_color_cli: Start getting data of dulux.
INFO: 2021-06-04 18:26:03,023: paint_color_cli: Total 1904 are collected and save to path ./.

```
