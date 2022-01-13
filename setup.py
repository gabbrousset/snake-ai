import cx_Freeze

executables = [cx_Freeze.Executable("snake.py")]

packages = ['pygame']
include_files = []
options = {
    'build_exe': {
        'packages': packages,
        "include_files": include_files,
    },
}

cx_Freeze.setup(
    name = 'snek',
    options = options,
    version = '1',
    description = 'gb',
    executables = executables
)