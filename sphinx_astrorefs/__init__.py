from . import pybtex_astro
from . import reformat
from . import resolve_aas
__version__= "0.1.dev0"

def setup(app):
    app.add_config_value('astrorefs_resolve_aas_macros',False,'env')
    app.add_config_value('astrorefs_resolve_aas_macros_infile',None,'env')
    app.add_config_value('astrorefs_resolve_aas_macros_outfile',None,'env')
    app.connect("config-inited",reformat.setup_latex)
    app.connect("env-before-read-docs",resolve_aas.resolve)
    app.connect("build-finished",reformat.reformat_output)
    pybtex_astro.register()
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
