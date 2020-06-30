# Quick script to replace all AAS macros in a bibtex file
import sys
import os.path
import re
from sphinx.errors import ExtensionError

aas_macros_dict= {
    '\\apjs'    : 'Astrophys. J. Supp.',
    '\\appjlett': 'Astrophys. J. Lett.',
    '\\apj'     : 'Astrophys. J.',
    '\\aj'      : 'Astron. J.',
    '\\mnras'   : 'Mon. Not. Roy. Astron. Soc.',
    '\\baas'    : 'Bull. AAS',
    '\\aapr'    : 'Astron. & Astrophys. Rev.',
    '\\aaps'    : 'Astron. & Astrophys. Supp.',
    '\\aap'     : 'Astron. & Astrophys.',
    '\\araa'    : 'Ann. Rev. Astron. Astrophys.',
    '\\actaa'   : 'Acta Astronomica',
    '\\apss'    : 'Astrophys. & Space Sci.',
    '\\jcap'    : 'J. Cosmo & Astropart. Phys.',
    '\\na'      : 'New Astron.',
    '\\pra'     : 'Phys. Rev. A',
    '\\prd'     : 'Phys. Rev. D',
    '\\prl'     : 'Phys. Rev. Lett.',
    '\\pasa'    : 'Pub. Astron. Soc. Aus.',
    '\\pasp'    : 'Pub. Astron. Soc. Pac.',
    '\\pasj'    : 'Pub. Astron. Soc. Japan',
    '\\rmxaa'   : 'Rev. Mex. Astron. & Astrofys.',
    '\\ssr'     : 'Space Sci. Rev.',
    '\\nat'     : 'Nature'
    }

def resolve(app,env,docnames):
    if not app.config.astrorefs_resolve_aas_macros:
        return
    if app.config.astrorefs_resolve_aas_macros_infile is None \
       or app.config.astrorefs_resolve_aas_macros_outfile is None:
        raise ExtensionError('sphinx-astrorefs: when resolving AAS macros, need to give original and target bib file name as "astrorefs_resolve_aas_macros_infile" and "astrorefs_resolve_aas_macros_outfile"')
    with open(os.path.join(env.srcdir,
                        app.config.astrorefs_resolve_aas_macros_infile),'r') \
                      as infile:
        with open(os.path.join(env.srcdir,
                        app.config.astrorefs_resolve_aas_macros_outfile),'w') \
                        as outfile:
            for line in infile:
                for key in aas_macros_dict.keys():
                    line= line.replace(key,aas_macros_dict[key])
                outfile.write(line)
