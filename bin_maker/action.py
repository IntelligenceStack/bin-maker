import glob
import json
import os
import shutil

from logzero import logger


def release():
    """
    release application,when run release action,bin-maker will compile python ,copy the 
    file to build path and remove all source code
    """
    for path in glob.glob('./build/lib.*'):
        dirs = os.listdir(path)
        for dir_name in dirs:
            source_path = os.path.join(path, dir_name)
            target_path = './%s' % dir_name
            logger.info('remove directory:[%s]' % dir_name)
            shutil.rmtree(target_path)

            logger.info('copy directory [%s] to [%s]' % (source_path, target_path))
            shutil.copytree(source_path, target_path)


def package():
    """
    package application with PyInstaller
    """

    pyinstall_spec = 'pyi-makespec ./main.py '

    config_entity = None
    if os.path.exists('./bin_maker.json'):
        logger.info('found bin_maker.json,load extra config')
        with open('./avalon-fsn.json', 'r', encoding='utf-8') as file:
            config_entity = json.load(file)
    
    if config_entity is not None:
        if config_entity['with_scikit'] == 'true':
            logger.info('hidden import sklearn package')

            pyinstall_spec += '--hiddenimport sklearn '
            pyinstall_spec += '--hiddenimport sklearn.ensemble '
            pyinstall_spec += '--hiddenimport sklearn.tree._utils '
            pyinstall_spec += '--hiddenimport sklearn.neighbors.typedefs '
            pyinstall_spec += '--hiddenimport sklearn.neighbors.ball_tree '
            pyinstall_spec += '--hiddenimport sklearn.neighbors.dist_metrics '
            pyinstall_spec += '--hiddenimport sklearn.neighbors.quad_tree '
            pyinstall_spec += '--hiddenimport sklearn.utils._cython_blas '
            pyinstall_spec += '--hiddenimport scipy._lib.messagestream '
        
        if config_entity['with_statics_model'] == 'true':
            logger.info('hidden import staics_model package')
            pyinstall_spec += '--hiddenimport statsmodels.tsa.statespace._filters '
            pyinstall_spec += '--hiddenimport statsmodels.tsa.statespace._filters._conventional '
            pyinstall_spec += '--hiddenimport statsmodels.tsa.statespace._filters._univariate '
            pyinstall_spec += '--hiddenimport statsmodels.tsa.statespace._filters._inversions '
            pyinstall_spec += '--hiddenimport statsmodels.tsa.statespace._smoothers '
            pyinstall_spec += '--hiddenimport statsmodels.tsa.statespace._smoothers._conventional '
            pyinstall_spec += '--hiddenimport statsmodels.tsa.statespace._smoothers._univariate '
            pyinstall_spec += '--hiddenimport statsmodels.tsa.statespace._smoothers._inversions '
            pyinstall_spec += '--hiddenimport statsmodels.tsa.statespace._smoothers._classical '
            pyinstall_spec += '--hiddenimport statsmodels.tsa.statespace._smoothers._alternative '
    os.system(pyinstall_spec)

    with open('./main.spec', 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write('import sys\nsys.setrecursionlimit(5000)\n' + content)
        
    os.system('pyinstaller --clean ./main.spec')
