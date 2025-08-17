from pathlib import Path

from pyapp import PyApp

from .logging import get_logger, DEBUG, log_func_call
from .models.avcad.constants import CFG_AVCAD_DB_KEY, CFG_AVCAD_LAYERS_KEY


class PyRigApp(PyApp):
    APP_NAME: str = 'PyRig'
    APP_LOG_PREFIX = 'PyRig'
    APP_PATH_KEYS = (
        # "local.delivery_config_dir",
        # "delivery_dir",
        CFG_AVCAD_DB_KEY,
        CFG_AVCAD_LAYERS_KEY,
        "avcad_sharedlib",
        "local.default_db_file",
        "local.ynab_token_file",
    )
    APP_GLOBAL_DEFAULTS = {
        # "local_config_file": "~/.pyrig_local_config.jsonc",
        # "delivery_dir": "${pkg_dir}/../deliveries",
        "avcad_sharedlib": "C:/Users/Public/SharedLibrary",
        CFG_AVCAD_DB_KEY: "${avcad_sharedlib}",
        CFG_AVCAD_LAYERS_KEY: "${avcad_sharedlib}/Settings/Layers.txt",
    }
    APP_LOCAL_DEFAULTS = {
        # "delivery_config_dir": "${assets_dir}/delivery_config",
        "default_db_file": "~/pyrig_data.db",
        "ynab_token_file": "~/ynab_token.txt",
        "ynab_token": None,
    }
    APP_ASSETS_DIR = "${package_dir}/assets"

    @classmethod
    @log_func_call
    def main(cls, input_data: dict | str | Path = None, *args,
             **kwargs):
        cls.init_main(input_data, True, **kwargs)
        log = get_logger()

        from .models.avcad.db import print_all_models, log_avcad_db_dir
        log_avcad_db_dir(DEBUG)
        if '--print-models' in args:
            log.info("Printing all models from the database...")
            print_all_models()

        from .models.db import check_pyrig_db
        check_pyrig_db()

        from .models.ynab import load_ynab_token
        load_ynab_token()

        from .gui import PyRigGui
        gui = PyRigGui(args)
        cls.gui = gui
        return gui.main(*args, **kwargs)

    @classmethod
    @log_func_call
    def preprocess_args(cls, args: list[str]):
        return args
