import sublime

import sys
import logging
import inspect

from os import path, environ, makedirs, chmod

handler = logging.StreamHandler(sys.stdout)
logger = None

_cache = '.cache'

# PlatformIO is not installed by Deviot, set where to find it:
# PIO_PATH is the `pio` executable, PYTHON_PATH the python used to run pip
# (updates). Both can be a full path or a name found in PATH.
PIO_PATH = 'pio'
PYTHON_PATH = 'python3'


def create_logger(name):
    global logger

    logger = logging.getLogger(name)
    logger.addHandler(handler)

    return logger


def set_logger_level(level='ERROR'):
    global logger

    from ..libraries.tools import get_setting

    setting_logger = get_setting('logger_level', None)

    if(setting_logger):
        level = setting_logger

    if(level == 'DEBUG'):
        level = logging.DEBUG
    elif(level == 'INFO'):
        level = logging.INFO
    elif(level == 'WARNING'):
        level = logging.WARNING
    elif(level == 'ERROR'):
        level = logging.ERROR
    else:
        level = logging.CRITICAL

    logger.setLevel(level)


def version():
    """
    return the plugin version
    """
    version = (2, 3, 0, '.dev13')
    v_format = ".".join([str(s) for s in version[:3]])
    if(len(version) > 3):
        v_format += version[3]
    return v_format


def header():
    """
    header to be used with the request module
    """
    deviot_v = version()
    sublime_v = sublime.version()
    user_agent = 'Deviot/%s (Sublime-Text/%s)' % (deviot_v, sublime_v)
    return {'User-Agent': user_agent}


def create_dirs(dirs):
    """
    Create a specifict path if it doesn't exists
    """
    import errno
    try:
        makedirs(dirs)
    except OSError as exc:
        if exc.errno is not errno.EEXIST:
            raise exc
        pass


def current_file_path():
    """
    full path of the current deviot.py file
    """
    return path.abspath(inspect.getfile(inspect.currentframe()))


def plugin_path():
    """
    path to Packages/Deviot (Arduino IDE)
    """
    current = current_file_path()
    return path.dirname(path.dirname(current))


def plugin_name():
    """
    Name of the plugin ex. Deviot (Arduino IDE)
    """
    plugin = plugin_path()
    return path.basename(plugin)


def packages_path():
    """
    Path to Packages/
    """
    plugin = plugin_path()
    return path.dirname(plugin)


def user_plugin_path():
    """
    Path to Packages/User/Deviot
    """
    packages = packages_path()
    return path.join(packages, 'User', 'Deviot')


def main_menu_path():
    """
    Path to Packages/Deviot/Main.sublime-menu
    """
    plugin = plugin_path()
    return path.join(plugin, 'Main.sublime-menu')


def presets_path():
    """
    Path to Packages/Deviot/presets
    """
    plugin = plugin_path()
    return path.join(plugin, 'presets')


def lang_list_path():
    """
    Path to Packages/Deviot/presets/languages.list
    """
    presets = presets_path()
    return path.join(presets, 'languages.list')


def quick_path():
    """
    Path to Packages/Deviot/presets/quick_panel.json
    """
    presets = presets_path()
    return path.join(presets, 'quick_panel.json')


def context_path():
    """
    Path to Packages/Deviot/presets/context_menu.json
    """
    presets = presets_path()
    return path.join(presets, 'context_menu.json')


def syntax_path():
    """
    Path to Packages/Deviot/presets/template.syntax
    """
    presets = presets_path()
    return path.join(presets, 'template.syntax')


def lang_path():
    """
    Path to Packages/Deviot/languages
    """
    plugin = plugin_path()
    return path.join(plugin, 'languages')


def cache_path():
    """
    Path to Packages/User/Deviot/.cache
    """
    plugin = user_plugin_path()
    return path.join(plugin, _cache)


def preset_file(file_name):
    """
    Path to /Packages/Deviot/presets/filename.json
    """
    presets = presets_path()
    return path.join(presets, file_name)


def temp_path(file_name=False):
    """
    Path to the temp folder depending on the O.S
    """
    tmp_path = '/tmp'
    os_name = sublime.platform()

    if(os_name == 'windows'):
        tmp_path = environ['tmp']

    tmp_path = path.join(tmp_path, 'Deviot')

    if(file_name):
        tmp_path = path.join(tmp_path, file_name)

    return tmp_path


def system_ini_path():
    """
    Path to Packages/User/Deviot/deviot.ini
    """
    user_plugin = user_plugin_path()
    return path.join(user_plugin, 'deviot.ini')


def setting_path():
    """
    Path to Packages/User/Deviot/deviot.ini
    """
    plugin = user_plugin_path()
    return path.join(plugin, 'deviot.ini')


def user_pio_path():
    """
    Path to Packages/User/Deviot/pio
    """
    user_path = user_plugin_path()
    return path.join(user_path, 'pio')


def pio_library(all=False):
    """
    Path to ~/.platformio/lib
    """
    user_path = path.expanduser('~')
    pio_lib = path.join(user_path, '.platformio', 'lib')

    create_dirs(pio_lib)
    chmod(pio_lib, 0o777)

    if(all):
        pio_lib = path.join(pio_lib, '*')

    return pio_lib


def pio_packages(all=True):
    """
    Path to ~/.platformio/packages
    """
    user_path = path.expanduser('~')
    pio_pack = path.join(user_path, '.platformio', 'packages')

    if(all):
        pio_pack = path.join(pio_pack, '*')

    return pio_pack


def boards_file_path():
    """
    Path to Packages/User/Deviot/pio/boards.json
    """
    user_data = user_pio_path()
    return path.join(user_data, 'boards.json')


def libraries_data_path():
    """
    Path to Packages/User/Deviot/pio/libraries.json
    """
    user_data = user_pio_path()
    return path.join(user_data, 'libraries.json')


def get_sysetting(key, default=None):
    """
    Stores the setting in the file:
    Packages/User/Deviot/deviot.ini
    """
    from ..libraries.readconfig import ReadConfig

    section = "config"
    setting_file = setting_path()

    config = ReadConfig()

    # remove config file if it's currupted
    if(config.bad_format()):
        ini = path.join(packages_path, 'User', 'Deviot', 'deviot.ini')

        if(path.exists(ini)):
            remove(ini)

    config.read(setting_file)

    if(not config.has_option(section, key)):
        return default

    output = config.get(section, key)[0]

    if(output == 'True' or output == 'False'):
        output = True if output == 'True' else False

    return output


def save_sysetting(key, value):
    """
    Gets the setting stored in the file
    Packages/User/Deviot/deviot.ini
    """
    from ..libraries.readconfig import ReadConfig

    section = "config"
    setting_file = setting_path()

    create_dirs(path.dirname(setting_file))

    config = ReadConfig()
    config.read(setting_file)

    if(not config.has_section(section)):
        config.add_section(section)

    config.set(section, key, value)

    with open(setting_file, 'w') as configfile:
        config.write(configfile)


def pio_command(options, verbose=False):
    """
    Completes PlatformIO command
    """
    command = ['"%s"' % PIO_PATH, '-f', '-c', 'sublimetext']
    command.extend(options)

    # verbose mode
    if(verbose and 'run' in options and '-e' in options):
        command.append('-v')
    return command


def run_command(command, cwd=None):
    '''Commands

    Run all the commands to install the plugin

    Arguments:
        command {list} -- list of commands

    Keyword Arguments:
        cwd {str} -- current working dir (default: None)

    Returns:
        [list] -- list[0]: return code list[1]: command output
    '''
    import subprocess

    command.append("2>&1")
    command = ' '.join(command)

    process = subprocess.Popen(command, stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE, cwd=cwd,
                               universal_newlines=True, shell=True)

    output = process.communicate()
    stdout = output[0]
    return_code = process.returncode

    return (return_code, stdout)


def folder_explorer(pathstr=None, callback=None, key=None):
    """Select a folder

    Opens the native folder picker of the OS (Sublime Text 4, build 4075+).
    It starts in 'pathstr', or in the 'last_path' setting, or in the home
    folder. The chosen folder is stored in the 'last_path' setting.

    When 'key' is given the callback is called like callback(key, path),
    otherwise callback(path). (The key argument is useful to work with the
    preferences)

    Keyword Arguments:
        pathstr {str} -- folder where the dialog starts (default: None)
        callback {function} -- called with the selected folder (default: None)
        key {str} -- key to use in the callback (default: None)
    """
    from ..libraries.tools import get_setting, save_setting

    def on_done(selected):
        # multi_select returns a list, the rest a string
        if(isinstance(selected, (list, tuple))):
            selected = selected[0] if selected else None

        if(not selected):
            return

        save_setting('last_path', selected)

        if(not key):
            return callback(selected)
        return callback(key, selected)

    start = pathstr or get_setting('last_path', None)

    if(not start or not path.isdir(start)):
        start = path.expanduser('~')

    sublime.select_folder_dialog(on_done, directory=start)


def save_board_list():
    """
    Stores the output of `pio boards --json-output` in
    Packages/User/Deviot/pio/boards.json
    """
    from ..libraries.file import File

    code, boards = run_command(pio_command(['boards', '--json-output']))

    if(code == 0):
        create_dirs(user_pio_path())
        File(boards_file_path()).write(boards)
