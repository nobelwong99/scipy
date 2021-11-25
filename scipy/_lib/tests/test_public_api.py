"""
This test script is adopted from:
    https://github.com/numpy/numpy/blob/main/numpy/tests/test_public_api.py
"""

import pkgutil
import types
import importlib
import warnings

import scipy


def check_dir(module, module_name=None):
    """Returns a mapping of all objects with the wrong __module__ attribute."""
    if module_name is None:
        module_name = module.__name__
    results = {}
    for name in dir(module):
        item = getattr(module, name)
        if (hasattr(item, '__module__') and hasattr(item, '__name__')
                and item.__module__ != module_name):
            results[name] = item.__module__ + '.' + item.__name__
    return results


def test_scipy_namespace():
    # None of these objects are publicly documented to be part of the main
    # SciPy namespace (some are useful though, others need to be cleaned up)
    undocumented = {
        'LowLevelCallable': 'scipy._lib._ccallback.LowLevelCallable'
    }
    # We override dir to not show these members
    allowlist = undocumented
    bad_results = check_dir(scipy)
    # pytest gives better error messages with the builtin assert than with
    # assert_equal
    assert bad_results == allowlist


def test_dir_testing():
    """Assert that output of dir has only one "testing/tester"
    attribute without duplicate"""
    assert len(dir(scipy)) == len(set(dir(scipy)))


# Historically SciPy has not used leading underscores for private submodules
# much.  This has resulted in lots of things that look like public modules
# (i.e. things that can be imported as `import scipy.somesubmodule.somefile`),
# but were never intended to be public.  The PUBLIC_MODULES list contains
# modules that are either public because they were meant to be, or because they
# contain public functions/objects that aren't present in any other namespace
# for whatever reason and therefore should be treated as public.
PUBLIC_MODULES = ["scipy." + s for s in [
    "cluster",
    "cluster.vq",
    "cluster.hierarchy",
    "constants",
    "fft",
    "fftpack",
    "integrate",
    "interpolate",
    "io",
    "io.arff",
    "io.matlab",
    "io.wavfile",
    "linalg",
    "linalg.blas",
    "linalg.cython_blas",
    "linalg.lapack",
    "linalg.cython_lapack",
    "linalg.interpolative",
    "misc",
    "ndimage",
    "odr",
    "optimize",
    "signal",
    "signal.windows",
    "sparse",
    "sparse.linalg",
    "sparse.csgraph",
    "spatial",
    "spatial.distance",
    "spatial.transform",
    "special",
    "stats",
    "stats.distributions",
    "stats.mstats",
    "stats.qmc",
]]

# The PRIVATE_BUT_PRESENT_MODULES list contains modules that look public (lack
# of underscores) but should not be used.  For many of those modules the
# current status is fine.  For others it may make sense to work on making them
# private, to clean up our public API and avoid confusion.
# These private modules support will be removed in SciPy v2.0.0
PRIVATE_BUT_PRESENT_MODULES = [
    'scipy.constants.codata',
    'scipy.constants.constants',
    'scipy.fftpack.basic',
    'scipy.fftpack.convolve',
    'scipy.fftpack.helper',
    'scipy.fftpack.pseudo_diffs',
    'scipy.fftpack.realtransforms',
    'scipy.integrate.dop',
    'scipy.integrate.lsoda',
    'scipy.integrate.vode',
    'scipy.interpolate.dfitpack',
    'scipy.interpolate.fitpack',
    'scipy.interpolate.fitpack2',
    'scipy.interpolate.interpnd',
    'scipy.interpolate.interpolate',
    'scipy.interpolate.ndgriddata',
    'scipy.interpolate.polyint',
    'scipy.interpolate.rbf',
    'scipy.io.arff.arffread',
    'scipy.io.harwell_boeing',
    'scipy.io.idl',
    'scipy.io.mmio',
    'scipy.io.netcdf',
    'scipy.io.matlab.byteordercodes',
    'scipy.io.matlab.mio',
    'scipy.io.matlab.mio4',
    'scipy.io.matlab.mio5',
    'scipy.io.matlab.mio5_params',
    'scipy.io.matlab.mio5_utils',
    'scipy.io.matlab.mio_utils',
    'scipy.io.matlab.miobase',
    'scipy.io.matlab.streams',
    'scipy.linalg.basic',
    'scipy.linalg.decomp',
    'scipy.linalg.decomp_cholesky',
    'scipy.linalg.decomp_lu',
    'scipy.linalg.decomp_qr',
    'scipy.linalg.decomp_schur',
    'scipy.linalg.decomp_svd',
    'scipy.linalg.flinalg',
    'scipy.linalg.matfuncs',
    'scipy.linalg.misc',
    'scipy.linalg.special_matrices',
    'scipy.misc.common',
    'scipy.misc.doccer',
    'scipy.ndimage.filters',
    'scipy.ndimage.fourier',
    'scipy.ndimage.interpolation',
    'scipy.ndimage.measurements',
    'scipy.ndimage.morphology',
    'scipy.odr.models',
    'scipy.odr.odrpack',
    'scipy.optimize.cobyla',
    'scipy.optimize.cython_optimize',
    'scipy.optimize.lbfgsb',
    'scipy.optimize.linesearch',
    'scipy.optimize.minpack',
    'scipy.optimize.minpack2',
    'scipy.optimize.moduleTNC',
    'scipy.optimize.nonlin',
    'scipy.optimize.optimize',
    'scipy.optimize.slsqp',
    'scipy.optimize.tnc',
    'scipy.optimize.zeros',
    'scipy.signal.bsplines',
    'scipy.signal.filter_design',
    'scipy.signal.fir_filter_design',
    'scipy.signal.lti_conversion',
    'scipy.signal.ltisys',
    'scipy.signal.signaltools',
    'scipy.signal.spectral',
    'scipy.signal.spline',
    'scipy.signal.waveforms',
    'scipy.signal.wavelets',
    'scipy.signal.windows.windows',
    'scipy.sparse.base',
    'scipy.sparse.bsr',
    'scipy.sparse.compressed',
    'scipy.sparse.construct',
    'scipy.sparse.coo',
    'scipy.sparse.csc',
    'scipy.sparse.csr',
    'scipy.sparse.data',
    'scipy.sparse.dia',
    'scipy.sparse.dok',
    'scipy.sparse.extract',
    'scipy.sparse.lil',
    'scipy.sparse.linalg.dsolve',
    'scipy.sparse.linalg.eigen',
    'scipy.sparse.linalg.interface',
    'scipy.sparse.linalg.isolve',
    'scipy.sparse.linalg.matfuncs',
    'scipy.sparse.sparsetools',
    'scipy.sparse.sputils',
    'scipy.spatial.ckdtree',
    'scipy.spatial.kdtree',
    'scipy.spatial.qhull',
    'scipy.spatial.transform.rotation',
    'scipy.special.add_newdocs',
    'scipy.special.basic',
    'scipy.special.cython_special',
    'scipy.special.orthogonal',
    'scipy.special.sf_error',
    'scipy.special.specfun',
    'scipy.special.spfun_stats',
    'scipy.stats.biasedurn',
    'scipy.stats.contingency',
    'scipy.stats.kde',
    'scipy.stats.morestats',
    'scipy.stats.mstats_basic',
    'scipy.stats.mstats_extras',
    'scipy.stats.mvn',
    'scipy.stats.statlib',
    'scipy.stats.stats',
]


def is_unexpected(name):
    """Check if this needs to be considered."""
    if '._' in name or '.tests' in name or '.setup' in name:
        return False

    if name in PUBLIC_MODULES:
        return False

    if name in PRIVATE_BUT_PRESENT_MODULES:
        return False

    return True


SKIP_LIST = [
    'scipy.conftest',
    'scipy.version',
]


def test_all_modules_are_expected():
    """
    Test that we don't add anything that looks like a new public module by
    accident.  Check is based on filenames.
    """

    modnames = []
    for _, modname, ispkg in pkgutil.walk_packages(path=scipy.__path__,
                                                   prefix=scipy.__name__ + '.',
                                                   onerror=None):
        if is_unexpected(modname) and modname not in SKIP_LIST:
            # We have a name that is new.  If that's on purpose, add it to
            # PUBLIC_MODULES.  We don't expect to have to add anything to
            # PRIVATE_BUT_PRESENT_MODULES.  Use an underscore in the name!
            modnames.append(modname)

    if modnames:
        raise AssertionError(f'Found unexpected modules: {modnames}')


# Stuff that clearly shouldn't be in the API and is detected by the next test
# below
SKIP_LIST_2 = [
    'scipy.char',
    'scipy.rec',
    'scipy.emath',
    'scipy.math',
    'scipy.random',
    'scipy.ctypeslib',
    'scipy.ma'
]


def test_all_modules_are_expected_2():
    """
    Method checking all objects. The pkgutil-based method in
    `test_all_modules_are_expected` does not catch imports into a namespace,
    only filenames.
    """

    def find_unexpected_members(mod_name):
        members = []
        module = importlib.import_module(mod_name)
        if hasattr(module, '__all__'):
            objnames = module.__all__
        else:
            objnames = dir(module)

        for objname in objnames:
            if not objname.startswith('_'):
                fullobjname = mod_name + '.' + objname
                if isinstance(getattr(module, objname), types.ModuleType):
                    if is_unexpected(fullobjname) and fullobjname not in SKIP_LIST_2:
                        members.append(fullobjname)

        return members

    unexpected_members = find_unexpected_members("scipy")
    for modname in PUBLIC_MODULES:
        unexpected_members.extend(find_unexpected_members(modname))

    if unexpected_members:
        raise AssertionError("Found unexpected object(s) that look like "
                             "modules: {}".format(unexpected_members))


def test_api_importable():
    """
    Check that all submodules listed higher up in this file can be imported
    Note that if a PRIVATE_BUT_PRESENT_MODULES entry goes missing, it may
    simply need to be removed from the list (deprecation may or may not be
    needed - apply common sense).
    """
    def check_importable(module_name):
        try:
            importlib.import_module(module_name)
        except (ImportError, AttributeError):
            return False

        return True

    module_names = []
    for module_name in PUBLIC_MODULES:
        if not check_importable(module_name):
            module_names.append(module_name)

    if module_names:
        raise AssertionError("Modules in the public API that cannot be "
                             "imported: {}".format(module_names))

    with warnings.catch_warnings(record=True) as w:
        warnings.filterwarnings('always', category=DeprecationWarning)
        warnings.filterwarnings('always', category=ImportWarning)
        for module_name in PRIVATE_BUT_PRESENT_MODULES:
            if not check_importable(module_name):
                module_names.append(module_name)

    if module_names:
        raise AssertionError("Modules that are not really public but looked "
                             "public and can not be imported: "
                             "{}".format(module_names))