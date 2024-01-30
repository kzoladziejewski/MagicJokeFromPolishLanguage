from pathlib import Path
DATABASE_NAME = 'mjfpl.db'
PATH_TO_DATABASE = Path(__file__).parent.joinpath('instance').joinpath(f'{DATABASE_NAME}').resolve()