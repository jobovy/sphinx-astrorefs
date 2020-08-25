# Test that AAS macros are correctly resolved (bc a little tricky sometimes...)
import os, os.path
import tempfile
import filecmp
from sphinx_astrorefs import resolve_aas

# Mock up classes that act like Sphinx' app and env used in resolve_aas
# (because I can't easily figure out how to use Sphinx's testing features)

class MockSphinxConfig:
    def __init__(self,
                 astrorefs_resolve_aas_macros=False,
                 astrorefs_resolve_aas_macros_infile=None,
                 astrorefs_resolve_aas_macros_outfile=None):
        self.astrorefs_resolve_aas_macros= \
            astrorefs_resolve_aas_macros
        self.astrorefs_resolve_aas_macros_infile= \
            astrorefs_resolve_aas_macros_infile
        self.astrorefs_resolve_aas_macros_outfile= \
            astrorefs_resolve_aas_macros_outfile

class MockSphinxApp:
    def __init__(self,
                 astrorefs_resolve_aas_macros=False,
                 astrorefs_resolve_aas_macros_infile=None,
                 astrorefs_resolve_aas_macros_outfile=None):
        self.config= MockSphinxConfig(\
     astrorefs_resolve_aas_macros=astrorefs_resolve_aas_macros,
     astrorefs_resolve_aas_macros_infile=astrorefs_resolve_aas_macros_infile,
     astrorefs_resolve_aas_macros_outfile=astrorefs_resolve_aas_macros_outfile)

class MockSphinxEnv:
    def __init__(self,srcdir=None):
        self.srcdir= srcdir
        
def test_resolve_aas():
    # Generate file to be resolved and the truth file
    file, resolve_file= tempfile.mkstemp(dir=os.getcwd())
    os.close(file) #Easier this way
    file, resolved_file= tempfile.mkstemp(dir=os.getcwd())
    os.close(file) #Easier this way
    file, truth_file= tempfile.mkstemp(dir=os.getcwd())
    os.close(file) #Easier this way
    try:
        with open(resolve_file,'w') as resolve:
            with open(truth_file,'w') as truth:
                for key in resolve_aas.aas_macros_dict:
                    resolve.write('{}\n'.format(key))
                    truth.write('{}\n'.format(resolve_aas.aas_macros_dict[key]))
        # Now resolve macros and check against truth
        app= MockSphinxApp(astrorefs_resolve_aas_macros=True,
                           astrorefs_resolve_aas_macros_infile=resolve_file,
                           astrorefs_resolve_aas_macros_outfile=resolved_file)
        env= MockSphinxEnv(srcdir='./')
        resolve_aas.resolve(app,env,None)
        # Now check resolved against truth
        assert filecmp.cmp(resolved_file,truth_file)
    except:
        raise
    finally:
        if os.path.exists(resolve_file):
            os.remove(resolve_file)
        if os.path.exists(resolved_file):
            os.remove(resolved_file)
        if os.path.exists(truth_file):
            os.remove(truth_file)
    return None
