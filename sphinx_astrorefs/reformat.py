# reformat.py: reformat the HTML and LaTeX output to be more 'astro' like
import os, os.path
import shutil
import tempfile
import re
from packaging.version import parse as parse_version
import sphinx
from sphinx.locale import __
from sphinx.util import logging
if parse_version(sphinx.__version__) >= parse_version("6.1"):
    from sphinx.util.display import status_iterator
else:
    from sphinx.util import status_iterator
logger= logging.getLogger(__name__)
# No sphinxcontrib.bibtex.__version__, so need to version check the hard way...
_SPHX_BIBTEX_VERSION= 2
try:
    import sphinxcontrib.bibtex.domain
except ImportError:
    _SPHX_BIBTEX_VERSION= 1
_HREF_CLASS= "bibtex reference internal" if _SPHX_BIBTEX_VERSION == 1 \
    else "reference internal"

def setup_latex(app,config):
    if not 'preamble' in config.latex_elements:
        config.latex_elements['preamble']= ""
    config.latex_elements['preamble']+=r"""
\usepackage{natbib}

\makeatletter
\renewcommand\@biblabel[1]{}
\renewenvironment{sphinxthebibliography}[1]
     {\chapter*{\refname}%
      \addcontentsline{toc}{chapter}{References}
      \@mkboth{\MakeUppercase\refname}{\MakeUppercase\refname}%
      \list{}%
           {\leftmargin0pt
            \@openbib@code
            \usecounter{enumiv}}%
      \sloppy
      \clubpenalty4000
      \@clubpenalty \clubpenalty
      \widowpenalty4000%
      \sfcode`\.\@m}
     {\def\@noitemerr
       {\@latex@warning{Empty `thebibliography' environment}}%
      \endlist}
\makeatother
        """

def reformat_html(app):
    logger.info('sphinx_astrorefs HTML reformatting... ')
    # Get all output files (http://stackoverflow.com/a/33640970/1447225)
    pages= []
    for doc in app.env.found_docs:
        target_filename= app.builder.get_target_uri(doc)
        target_filename= os.path.join(app.outdir, target_filename)
        target_filename= os.path.abspath(target_filename)
        pages.append(target_filename)
    # Compile reg. expression
    if _SPHX_BIBTEX_VERSION == 1:
        re_bibtex_links= re.compile(r'<a class="{}" href="([^"]*)" id="([^"]*)">\[([^\]]*)\]</a>'.format(_HREF_CLASS))
    else:
        re_bibtex_links= re.compile(r'<span id="([^"]*)">\[<a class="{}" href="([^"]*)"><span>([^\]]*)</span></a>\]</span>'.format(_HREF_CLASS))
    # Reformat all pages
    for page in status_iterator(pages, __('sphinx_astrorefs reformatting... '),
                                "blue",
                                len(pages),app.verbosity):
        try:
            fd, tmp_path= tempfile.mkstemp()
            os.close(fd)
            with open(page,'r') as infile: 
                with open(tmp_path,'w') as outfile:
                    for line in infile:
                        if 'class="{}"'.format(_HREF_CLASS) in line:
                            line_adjust= 0 # account for the fact that g.start
                            # starts to deviate from the actual start, because
                            # we are editing the line
                            for g in re.finditer(re_bibtex_links,line):
                                try:
                                    ref= g.group(3)
                                except AttributeError:
                                    raise AttributeError('Line matched internal bibtex link, but fails to find [author(s) year] reference; assuming that the file has already been processed with this code and skipping the rest')
                                try:
                                    just_before= line[g.start()-1-line_adjust]
                                    rm_just_before= just_before == ':'
                                    if just_before == '(' or rm_just_before:
                                        parentheses= False
                                    else:
                                        parentheses= True
                                except:
                                    parentheses= True
                                    rm_just_before= False
                                if parentheses:
                                    replace_ref= ' '.join(ref.split(' ')[:-1])
                                    replace_ref+= ' ({})'.format(ref.split(' ')[-1])
                                else:
                                    replace_ref= ref
                                    line_adjust+= 2
                                if _SPHX_BIBTEX_VERSION == 1:
                                    line= line.replace('[{}]'.format(ref),
                                                           replace_ref,1)
                                else:
                                    replace_ref= '<a class="{}" href="{}" id="{}">{}</a>'.format(_HREF_CLASS,g.group(2),g.group(1),replace_ref)
                                    line= line.replace('<span id="{}">[<a class="{}" href="{}"><span>{}</span></a>]</span>'.format(g.group(1),_HREF_CLASS,g.group(2),g.group(3)),
                                                           replace_ref,1)
                                    # Taking out 2x <span></span>
                                    line_adjust+= 26
                                if rm_just_before:
                                    line_adjust+= 1
                                    line= line.replace(\
                                        ':<a class="{}"'.format(_HREF_CLASS),
                                        '<a class="{}"'.format(_HREF_CLASS),
                                        1)
                        outfile.write(line)
            shutil.move(tmp_path,page)
        except AttributeError as e:
            if str(e) == 'Line matched internal bibtex link, but fails to find [author(s) year] reference; assuming that the file has already been processed with this code and skipping the rest':
                pass
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

def reformat_latex(app):
    latex_file= os.path.join(app.builder.outdir,
                             app.builder.document_data[0][1])
    logger.info('sphinx_astrorefs LaTeX reformatting... ')
    re_bibtex_links= re.compile(r'\\sphinxcite{([^\}]*)}')
    re_bibitem= re.compile(r'\\bibitem\[([^\]]*)\]')
    try:
        fd, tmp_path= tempfile.mkstemp()
        os.close(fd)
        with open(latex_file,'r') as infile: 
            with open(tmp_path,'w') as outfile:
                for line in infile:
                    if 'sphinxcite' in line:
                        line_adjust= 0 # account for the fact that g.start
                        # starts to deviate from the actual start, because
                        # we are editing the line
                        for g in re.finditer(re_bibtex_links,line):
                            try:
                                ref= g.group(1)
                            except AttributeError:
                                raise AttributeError('Line matched internal bibtex link, but fails to find [author(s) year] reference; assuming that the file has already been processed with this code and skipping the rest')
                            try:
                                just_before= line[g.start()-1-line_adjust]
                                rm_just_before= just_before == ':'
                                if just_before == '(' or rm_just_before:
                                    parentheses= False
                                else:
                                    parentheses= True
                            except: parentheses= True
                            if parentheses:
                                line_adjust+= 5
                                line= line.replace(r'\sphinxcite{{{}}}'.format(ref),
                                                   r'\citet{{{}}}'.format(ref),1)
                            else:
                                line_adjust+= 3
                                line= line.replace(r'\sphinxcite{{{}}}'.format(ref),
                                                   r'\citealt{{{}}}'.format(ref),1)
                            if rm_just_before:
                                line_adjust+= 1
                                line= line.replace(r':\citealt{{{}}}'.format(ref),
                                                   r'\citealt{{{}}}'.format(ref),1)
                    elif 'bibitem' in line:
                        # Parses bibliography
                        g= re.search(re_bibitem,line)
                        ref= g.group(1)
                        if '(' in ref: # assume we already processed the file
                            break
                        replace_ref= ' '.join(ref.split(' ')[:-1])
                        replace_ref+= '({})'.format(ref.split(' ')[-1])
                        line= line.replace(ref,replace_ref,1)
                    elif r'\chapter{References}' in line \
                         or r'\label{\detokenize{references:references}}\label{\detokenize{references::doc}}' in line:
                        continue # remove these lines
                    outfile.write(line)
        shutil.move(tmp_path,latex_file)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

def reformat_output(app,exception):
    if exception is not None: # don't do anything if sphinx failed
        return
    if app.builder.name == 'html' \
       or (app.builder.name == 'readthedocs' and 'html' in app.builder.outdir):
        reformat_html(app)
    elif app.builder.name == 'latex' \
       or (app.builder.name == 'readthedocs' and 'latex' in app.builder.outdir):
        reformat_latex(app)
    else: # ignore other builders
        pass
