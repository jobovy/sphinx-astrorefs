from . import pybtex_astro
from . import reformat
__version__= "0.1.dev0"

def setup(app):
    app.connect("config-inited",reformat.setup_latex)
    app.connect("build-finished",reformat.reformat_output)
    pybtex_astro.register()
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
