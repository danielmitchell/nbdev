# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/07_clean.ipynb (unless otherwise specified).

__all__ = ['rm_execution_count', 'clean_cell_output', 'cell_metadata_keep', 'nb_metadata_keep', 'clean_cell',
           'clean_nb', 'nbdev_clean_nbs']

# Cell
import io,sys,json
from fastscript import call_parse,Param
from .imports import Config

# Cell
def rm_execution_count(o):
    "Remove execution count in `o`"
    if 'execution_count' in o: o['execution_count'] = None

# Cell
def clean_cell_output(cell):
    "Remove execution count in `cell`"
    if 'outputs' in cell:
        for o in cell['outputs']: rm_execution_count(o)

# Cell
cell_metadata_keep = ["hide_input"]
nb_metadata_keep   = ["kernelspec", "jekyll", "jupytext"]

# Cell
def clean_cell(cell, clear_all=False):
    "Clean `cell` by removing superluous metadata or everything except the input if `clear_all`"
    rm_execution_count(cell)
    if 'outputs' in cell:
        if clear_all: cell['outputs'] = []
        else:         clean_cell_output(cell)
    cell['metadata'] = {} if clear_all else {k:v for k,v in cell['metadata'].items() if k in cell_metadata_keep}

# Cell
def clean_nb(nb, clear_all=False):
    "Clean `nb` from superfulous metadata, passing `clear_all` to `clean_cell`"
    for c in nb['cells']: clean_cell(c, clear_all=clear_all)
    nb['metadata'] = {k:v for k,v in nb['metadata'].items() if k in nb_metadata_keep }

# Cell
import io,sys,json

# Cell
def _print_output(nb):
    "Print `nb` in stdout for git things"
    _output_stream = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    x = json.dumps(nb, sort_keys=True, indent=1, ensure_ascii=False)
    _output_stream.write(x)
    _output_stream.write("\n")
    _output_stream.flush()

# Cell
@call_parse
def nbdev_clean_nbs(fname:Param("A notebook name or glob to convert", str)=None,
                    clear_all:Param("Clean all metadata and outputs", bool)=False,
                    disp:Param("Print the cleaned outputs", bool)=False,
                    read_input_stream:Param("Read input stram and not nb folder")=False):
    "Clean all notebooks in `fname` to avoid merge conflicts"
    #Git hooks will pass the notebooks in the stdin
    if read_input_stream and sys.stdin:
        input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
        nb = json.load(input_stream)
        clean_nb(nb, clear_all=clear_all)
        _print_output(nb)
        return
    files = Config().nbs_path.glob('**/*.ipynb') if fname is None else glob.glob(fname)
    for f in files:
        if not str(f).endswith('.ipynb'): continue
        nb = json.load(open(f, 'r', encoding='utf-8'))
        clean_nb(nb, clear_all=clear_all)
        if disp: _print_output(nb)
        else: json.dump(nb, open(f, 'w', encoding='utf-8'), sort_keys=True, indent=1, ensure_ascii=False)