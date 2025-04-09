import os, sys, logging, inspect, platform, subprocess

RESET = "\033[0m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"

def _clear_all():
    os.system('cls' if os.name == 'nt' else 'clear')

def _colored_print(color, text):
    print(f"{color}{text}{RESET}")

def __orly__(py_mod, pip_pkg, caller_globals):
    try:
        module = __import__(py_mod)
    except ImportError:
        _colored_print(YELLOW, f"[!] Module '{py_mod}' not found. Attempting to install '{pip_pkg}'...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pip_pkg])
            module = __import__(py_mod)
        except Exception as e:
            _colored_print(RED, f"[X] ERROR: Failed to install '{pip_pkg}'.")
            _colored_print(RED, f"[X] ERROR DETAILS: {e}")
            if platform.system() == "Linux":
                _colored_print(YELLOW, "[!] Some Linux VPS (Ubuntu, Debian) require --break-system-packages.")
                choice = input("[?] Try again with '--break-system-packages'? (Y/N): ").strip().lower()
                if choice == 'y':
                    try:
                        subprocess.check_call([sys.executable, "-m", "pip", "install", "--break-system-packages", pip_pkg])
                        module = __import__(py_mod)
                    except Exception as e:
                        _colored_print(RED, f"[X] ERROR: Even with '--break-system-packages', installation failed.")
                        _colored_print(RED, f"[X] ERROR DETAILS: {e}")
            input("[!] Press ENTER to continue (the script may crash)...")
            return None
        _clear_all()
    try:
        caller_globals[py_mod] = module
    except Exception as e:
        _colored_print(RED, f"[X] ERROR: Failed to inject '{py_mod}' into the global workspace.")
        _colored_print(RED, f"[X] ERROR DETAILS: {e}")

def _mute_all_loggers(mod_name):
    try:
        logger = logging.getLogger(mod_name)
        logger.setLevel(logging.CRITICAL)
        logger.propagate = False
        # Also disable sub-loggers whose name starts with mod_name
        for name in list(logging.root.manager.loggerDict.keys()):
            if name.startswith(mod_name):
                try:
                    sub_logger = logging.getLogger(name)
                    sub_logger.setLevel(logging.CRITICAL)
                    sub_logger.propagate = False
                except Exception:
                    pass
    except Exception:
        pass

def set(modules, silent=False):
    caller_globals = inspect.stack()[1].frame.f_globals
    for mod in modules:
        module_silent = silent
        if mod.endswith("*"):
            mod = mod.rstrip("*")
            module_silent = True

        python_module = pip_package = alias = None
        if "==" in mod:
            python_module, pip_package = mod.split("==", 1)
        elif "~~" in mod:
            python_module, alias = mod.split("~~", 1)
            pip_package = python_module
        else:
            python_module = pip_package = mod

        __orly__(python_module, pip_package, caller_globals)
        if alias:
            caller_globals[alias] = caller_globals[python_module]
        if module_silent:
            try:
                caller_globals[python_module].print = lambda *args, **kwargs: None
            except Exception:
                pass
            # Universal logger disablement for this module
            try:
                mod_name = caller_globals[python_module].__name__
                _mute_all_loggers(mod_name)
            except Exception:
                pass
        _clear_all()

__all__ = ['set']
