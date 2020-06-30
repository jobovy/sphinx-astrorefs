import pybtex_astro
__version__= "0.1.dev0"

def setup(app):
    pybtex_astro.register()
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
