#!/usr/bin/env python3

import os
import datetime
import shlex
import argparse
import fnmatch

now = datetime.datetime.now()

parser = argparse.ArgumentParser(description='Recurse directory into jsTree HTML.')
parser.add_argument('-a', '--assets', default=None,
                   help='path to assets directory relative to html file for loading js and css locally')
parser.add_argument('-b', '--base', default='.',
                   help='directory that is the base for the tree')
parser.add_argument('-e', '--exclude', action='append',
                   help='exclude pattern (repeat as needed)')
parser.add_argument('--exclude-from', dest='excludefrom', default=None,
                   help='load exclude patterns from file')
parser.add_argument('-p', '--prefix', default='',
                   help='absolute path prefix to add in paths')
parser.add_argument('-r', '--restrict', dest='restrict', action='store_true',
                   help='restrict to known files')
parser.set_defaults(restrict=False)
parser.add_argument('-t', '--title', default='Filetree',
                   help='title for the resulting document')
parser.add_argument('--autosearch-on', dest='autosearch', action='store_true',
                   help='pre-enable autosearch (default)')
parser.add_argument('--autosearch-off', dest='autosearch', action='store_false',
                   help='autosearch not pre-enabled')
parser.set_defaults(autosearch=True)
args = parser.parse_args()

try:
    if args.exclude is None:
        args.exclude = []
    if args.excludefrom is not None:
        with open(args.excludefrom, "r") as ins:
            for line in ins:
                args.exclude.append(line.strip())
except FileNotFoundError:
    pass


def human_size(number):
    supportedunits = ['B', 'KB', 'MB', 'GB', 'TB']
    if number == 0: return '0 B'
    i = 0
    while number >= 1024 and i < len(supportedunits)-1:
        number /= 1024.
        i += 1
    dezimal = ('%.2f' % number).rstrip('0').rstrip('.')
    return '%s %s' % (dezimal, supportedunits[i])

def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def select_icon(filename):
    extension = os.path.splitext(filename)[1].lower()
    if extension in ['.txt']:
        return 'fa fa-file-text-o'
    elif extension in ['.pdf']:
        return 'fa fa-file-pdf-o'
    elif extension in ['.zip','.tar','.gzip','.tgz']:
        return 'fa fa-file-archive-o'
    elif extension in ['.doc','.docx','.odt','.rtf']:
        return 'fa fa-file-word-o'
    elif extension in ['.xls','.xlsx','.ods','.gnumeric']:
        return 'fa fa-file-excel-o'
    elif extension in ['.ppt','.pptx','.odp']:
        return 'fa fa-file-powerpoint-o'
    elif extension in ['.jpg','.jpeg','.png','.tiff','.psd','.xcf']:
        return 'glyphicon glyphicon-picture'
    elif extension in ['.mp3','.ogg','.flac','m4a','.wav']:
        return 'glyphicon glyphicon-music'
    elif extension in ['.iso','.img']:
        return 'glyphicon glyphicon-cd'
    elif extension in ['.mkv','.mp4','.avi','.flv','.mpg','.m2ts','.wmv']:
        return 'glyphicon glyphicon-film'
    elif extension in ['.srt']:
        return 'glyphicon glyphicon-subtitles'
    elif extension in ['.nfo']:
        return 'glyphicon glyphicon-tags'
    else:
        return 'glyphicon glyphicon-leaf'

def get_filepathlink(a,f):
    return shlex.quote(os.path.normpath(os.path.join(args.prefix, a, f)))

def check_excluded(f):
    for exclude_item in args.exclude:
        if fnmatch.fnmatch(f, exclude_item) or  fnmatch.fnmatch(f, os.path.join(args.base,exclude_item)):
            return True
    return False

def tracing(a):
    files = []
    dirs = []
    for item in os.listdir(a):
        ### do NOT trace links and check excludes
        if not os.path.islink(os.path.join(a, item)) and not check_excluded(os.path.join(a, item)):
            if os.path.isfile(os.path.join(a, item)):
                files.append(item)
            else:
                dirs.append(item)
    for d in sorted(dirs):
        print ("<li data-path=\"", get_filepathlink(a, d), "\" title=\"Size: ", human_size(get_size(os.path.join(a, d))), "\">", d, "\n<ul>",sep="")
        tracing(os.path.join(a, d))
        print ("</ul></li>\n")
    for f in sorted(files):
        if not (args.restrict and select_icon(f) == "glyphicon glyphicon-leaf"):
           print ("<li data-path=\"", get_filepathlink(a, f), "\" title=\"Size: ", human_size(os.path.getsize(os.path.join(a, f))), "\" data-jstree='{\"icon\":\"", select_icon(f), "\"}'>", f, "</li>\n",sep="")

def print_head():
    print ("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset=\"utf-8\">
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
        <title>""",args.title,"</title>")
    if args.assets != None:
        print ("<link rel=\"stylesheet\" href=\"",args.assets,"bootstrap.min.css\">",sep="")
        print ("<link rel=\"stylesheet\" href=\"",args.assets,"bootstrap-theme.min.css\">",sep="")
        print ("<link rel=\"stylesheet\" href=\"",args.assets,"font-awesome.min.css\">",sep="")
        print ("<link rel=\"stylesheet\" href=\"",args.assets,"style.min.css\" >",sep="")
    else:
        print ("""
            <link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css\">
            <link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css\">
            <link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css\">
            <link rel=\"stylesheet\" href=\"https://cdnjs.cloudflare.com/ajax/libs/jstree/3.3.4/themes/default/style.min.css\" >
            """)
    print ("""
        <style>
        .formarea:after {
            content: '';
            display: block;
            clear: both;
        }
        .filetree-grey {
            color: grey;
        }
        </style>
    </head>
    <body>
        <h1>""",args.title,"""</h1>
        <h4>Last Update: <span class="label label-info">
        """)
    print (now.strftime("%Y-%m-%d %H:%M"))
    if (args.autosearch):
        autosearch_string = 'checked'
    else:
        autosearch_string = ''
    print ("""
        </span></h4>
        <div class="formarea">

          <div class="row">

            <div class="col-md-3">
              <form id="search">
                <div class="input-group">
                  <input type="text" id="treesearch" class="form-control" placeholder="Search for...">
                  <span class="input-group-btn">
                    <button id="searchbutton" class="btn btn-default" type="submit">Go!</button>
                  </span>
                </div>
              </form>
            </div>

            <div class=\"col-md-1\">
              <div class=\"checkbox\">
                <label><input type=\"checkbox\" class=\"checkbox-inline\" id=\"autosearch\" """,autosearch_string,""">Autosearch</label>
              </div>
            </div>

            <div class="col-md-3">
              <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#selectionModal">
                Selection
              </button>
            </div>

          </div>

        </div>
        <div id=\"tree\">
        <ul>
        """)

def print_bottom():
    print ("""
        </ul>
        </div>
        <div class="modal fade" id="selectionModal" tabindex="-1" role="dialog" aria-labelledby="selectionModalLabel">
          <div class="modal-dialog" role="document">
            <div class="modal-content">
              <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                <h4 class="modal-title" id="selectionModalLabel">Current selection</h4>
              </div>
              <div class="modal-body">
                ...
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
              </div>
            </div>
          </div>
        </div>
        """)
    if args.assets != None:
        print ("<script src=\"",args.assets,"jquery-1.12.4.min.js\"></script>",sep="")
        print ("<script src=\"",args.assets,"bootstrap.min.js\"></script>",sep="")
        print ("<script src=\"",args.assets,"jstree.min.js\"></script>",sep="")
    else:
        print ("""
            <script src=\"https://code.jquery.com/jquery-1.12.4.min.js\"></script>
            <script src=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js\"></script>
            <script src=\"https://cdnjs.cloudflare.com/ajax/libs/jstree/3.3.4/jstree.min.js\"></script>
            """)

    print ("""
        <script>
          function searchFunction() {
              $('#tree').jstree('close_all');
              $('#tree').jstree(true).settings.search.show_only_matches = true;
              $('#tree').jstree(true).settings.search.show_only_matches_children = true;
              $('#tree').jstree(true).search($('#treesearch').val());
          }
          $('#tree').jstree({
            "plugins" : [ "search","checkbox" ]
          });
          $('#search').submit(function(e) {
              e.preventDefault();
              searchFunction();
          });
          $('#tree').on('changed.jstree', function (e, data) {
            if(data && data.selected && data.selected.length) {
              $('#selectedpath').val(data.node.data.path);
            }
          });
          $(function () {
            var to = false;
            $('#treesearch').keyup(function () {
              if ($('#autosearch').is(':checked')) {
                if(to) { clearTimeout(to); }
                to = setTimeout(function () {
                  searchFunction();
                }, 350);
              }
            });
          });
          $('#selectionModal').on('show.bs.modal', function (event) {
            $(this).find('.modal-body').html("<pre></pre>");
            var selectedElementsPaths = [];
            var selectedElements = $('#tree').jstree("get_selected", true);
            $.each(selectedElements, function() {
              selectedElementsPaths.push(this.data.path+'\\n');
            });
            $(this).find('.modal-body pre').append(selectedElementsPaths);
          });
        </script>
    </body>
    </html>
    """)

if __name__ == "__main__":
    # execute only if run as a script
    print_head()
    tracing(args.base)
    print_bottom()

