# filetree.py

This Python script recursively parses the directory it is run from and outputs a single HTML file containing the directory tree with [jsTress](https://www.jstree.com/).

## Usage

The script can be called from the command line

```
usage: filetree.py [-h] [-a ASSETS] [-b BASE] [-p PREFIX] [-r] [-t TITLE]

Recurse directory into jsTree HTML.

optional arguments:
  -h, --help            show this help message and exit
  -a ASSETS, --assets ASSETS
                        path to assets directory relative to html file for
                        loading js and css locally
  -b BASE, --base BASE  directory that is the base for the tree
  -p PREFIX, --prefix PREFIX
                        absolute path prefix to add in paths
  -r, --restrict        restrict to known files
  -t TITLE, --title TITLE
                        title for the resulting document
```


