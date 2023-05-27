from src.acutils.file import tmnt_generate_documentation
import os



if __name__ == '__main__':
    import os

    pydir = os.path.join(os.path.dirname(__file__), 'src', 'acutils')
    mddir = os.path.join(os.path.dirname(__file__), 'doc')

    for name in ['handler', 'file', 'image', 'multiprocess',
                 'sheet', 'pathology', 'gpu', 'video']:
        tmnt_generate_documentation(os.path.join(pydir, f'{name}.py'), mddir)