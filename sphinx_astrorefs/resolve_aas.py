# Quick script to replace all AAS macros in a bibtex file
import os.path
from sphinx.errors import ExtensionError

aas_macros_dict= {
    '\\apjsupp' : 'Astrophys. J. Supp.',
    '\\apjs'    : 'Astrophys. J. Supp.',
    '\\apjlett': 'Astrophys. J. Lett.',
    '\\apjl'   : 'Astrophys. J. Lett.',
    '\\apj'     : 'Astrophys. J.',
    '\\aj'      : 'Astron. J.',
    '\\mnras'   : 'Mon. Not. Roy. Astron. Soc.',
    '\\baas'    : 'Bull. AAS',
    '\\bain'    : 'Bull. Astron. Inst. Netherlands',
    '\\aapr'    : 'Astron. & Astrophys. Rev.',
    '\\aaps'    : 'Astron. & Astrophys. Supp.',
    '\\astap'   : 'Astron. & Astrophys.',
    '\\aap'     : 'Astron. & Astrophys.',
    '\\araa'    : 'Ann. Rev. Astron. Astrophys.',
    '\\actaa'   : 'Acta Astronomica',
    '\\apss'    : 'Astrophys. & Space Sci.',
    '\\jcap'    : 'J. Cosmo & Astropart. Phys.',
    '\\nat'     : 'Nature',
    '\\nar'     : 'New Astron. Rev.',
    '\\na'      : 'New Astron.',
    '\\pra'     : 'Phys. Rev. A',
    '\\prb'     : 'Phys. Rev. B',
    '\\prc'     : 'Phys. Rev. C',
    '\\prd'     : 'Phys. Rev. D',
    '\\pre'     : 'Phys. Rev. E',
    '\\prl'     : 'Phys. Rev. Lett.',
    '\\pasa'    : 'Pub. Astron. Soc. Aus.',
    '\\pasp'    : 'Pub. Astron. Soc. Pac.',
    '\\pasj'    : 'Pub. Astron. Soc. Japan',
    '\\rmxaa'   : 'Rev. Mex. Astron. & Astrofys.',
    '\\ssr'     : 'Space Sci. Rev.',
    '\\applopt' : 'Appl. Opt.',
    '\\ao'      : 'Appl. Opt.',
    '\\azh'     : 'Astron. Zhu.',
    '\\bac'     : 'Bull. Astron. Czech.',
    '\\caa'     : 'Chin. Astron. Astrophys.',
    '\\cjaa'    : 'Chin. J. Astron. Astrophys.',
    '\\icarus'  : 'Icarus',
    '\\jrasc'   : 'J. RAS Can.',
    '\\memras'  : 'Mem. RAS',
    '\\qjras'   : 'Quat. J. RAS',
    '\\skytel'  : 'Sky & Telescope',
    '\\solphys' : 'Sol. Phys.',
    '\\sovast'  : 'Sov. Astron.',
    '\\zap'     : 'ZeitSch. Astrophys.',
    '\\iaucirc' : 'IAU Circs.',
    '\\aplett'  : 'Astrophys. Lett.',
    '\\apspr'   : 'Astrophys. Space Phys. Res.',
    '\\fcp'     : 'Fund. Cosm. Phys.',
    '\\gca'     : 'Geochim. Cosmochim. Acta',
    '\\grl'     : 'Geophys. Res. Lett',
    '\\jcp'     : 'J. Chem. Phys.',
    '\\jgr'     : 'J. Geophys. Res.',
    '\\jqsrt'   : 'J. Quant. Spec. Rad. Trans.',
    '\\memsai'  : 'Mem. Soc. Astron. Ital.',
    '\\nphysa'  : 'Nucl. Phys. A',
    '\\physrep' : 'Phys. Rep.',
    '\\physscr' : 'Phys. Scrip.',
    '\\planss'  : 'Plan. Space. Sci.',
    '\\procspie': 'Proc. SPIE'
    }

def resolve(app):
    if not app.config.astrorefs_resolve_aas_macros:
        return
    if app.config.astrorefs_resolve_aas_macros_infile is None \
       or app.config.astrorefs_resolve_aas_macros_outfile is None:
        raise ExtensionError('sphinx-astrorefs: when resolving AAS macros, need to give original and target bib file name as "astrorefs_resolve_aas_macros_infile" and "astrorefs_resolve_aas_macros_outfile"')
    with open(os.path.join(app.env.srcdir,
                        app.config.astrorefs_resolve_aas_macros_infile),'r') \
                      as infile:
        with open(os.path.join(app.env.srcdir,
                        app.config.astrorefs_resolve_aas_macros_outfile),'w') \
                        as outfile:
            for line in infile:
                for key in aas_macros_dict.keys():
                    line= line.replace(key,aas_macros_dict[key])
                outfile.write(line)
    # Re-do this initialization to make sure the bibtex file is found
    if hasattr(app.config,'bibtex_bibfiles'):
        app.env.get_domain('cite').__init__(app.env)
