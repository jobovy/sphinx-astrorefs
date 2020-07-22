from pathlib import Path
from . import pybtex_astro
from . import reformat
from . import resolve_aas
__version__= "0.2"

def append_static_path(app,config):
    config.html_static_path.append(
        str(Path(__file__).parent.joinpath("_static").absolute()))

def setup(app):
    app.add_config_value('astrorefs_resolve_aas_macros',False,'env')
    app.add_config_value('astrorefs_resolve_aas_macros_infile',None,'env')
    app.add_config_value('astrorefs_resolve_aas_macros_outfile',None,'env')
    app.connect("config-inited",reformat.setup_latex)
    app.connect("config-inited",append_static_path)
    app.connect("env-before-read-docs",resolve_aas.resolve)
    app.connect("build-finished",reformat.reformat_output)
    app.add_css_file("sphinx_astrorefs.css")
    pybtex_astro.register()
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
