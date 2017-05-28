# filetree.py

This Python script recursively parses the directory it is run from and outputs a single HTML file containing the directory tree with [jsTress](https://www.jstree.com/).

## Usage

The script can be called from the command line

```
usage: filetree.py [-h] [-a ASSETS] [-b BASE] [-e EXCLUDE]
                   [--exclude-from EXCLUDEFROM] [-p PREFIX] [-r] [-t TITLE]
                   [--autosearch-on] [--autosearch-off]

Recurse directory into jsTree HTML.

optional arguments:
  -h, --help            show this help message and exit
  -a ASSETS, --assets ASSETS
                        path to assets directory relative to html file for
                        loading js and css locally
  -b BASE, --base BASE  directory that is the base for the tree
  -e EXCLUDE, --exclude EXCLUDE
                        exclude pattern (repeat as needed)
  --exclude-from EXCLUDEFROM
                        load exclude patterns from file
  -p PREFIX, --prefix PREFIX
                        absolute path prefix to add in paths
  -r, --restrict        restrict to known files
  -t TITLE, --title TITLE
                        title for the resulting document
  --autosearch-on       pre-enable autosearch (default)
  --autosearch-off      autosearch not pre-enabled
```


