from pathlib import Path

from PySide2.QtWidgets import QFileDialog
from PySide2.QtGui import QMouseEvent

from pyapp.gui.window import GuiWindow
from pyapp.gui.dialogs.config import ConfigTreeDialog

from ...logging import log_func_call
from ...models.avcad.db import (
    get_avcad_db_dir, set_avcad_db_dir, log_avcad_db_dir
)

from .view import MainWindowView


class MainWindow(GuiWindow[MainWindowView]):
    @log_func_call
    def __init__(self):
        from ...app import PyRigApp
        super().__init__(PyRigApp.APP_NAME)

    @log_func_call
    def create_gui_view(self, basetitle: str, *args,
                        **kwargs) -> MainWindowView:
        return MainWindowView(basetitle, self, *args, **kwargs)

    @log_func_call
    def click_new(self):
        print("New clicked")
        # Implement new file logic here

    @log_func_call
    def click_open(self):
        print("Open clicked")
        # Implement open file logic here

    @log_func_call
    def click_save(self):
        print("Save clicked")
        # Implement save file logic here

    @log_func_call
    def click_saveas(self):
        print("Save As clicked")
        # Implement save as file logic here

    @log_func_call
    def click_avcad_dbdir(self, event: QMouseEvent):
        dbdir: Path = get_avcad_db_dir()
        qtwin = self.gui_view.qtobj
        new_dir = QFileDialog.getExistingDirectory(
            qtwin, "Select AVCAD Database Directory", str(dbdir)
        )
        if new_dir:
            set_avcad_db_dir(new_dir)
            self.update_avcad_dbdir_label()

    @log_func_call
    def update_avcad_dbdir_label(self, qtwin: MainWindowView = None):
        if qtwin is None:
            qtwin = self.gui_view

        dbdir: Path = get_avcad_db_dir()
        qtwin.status_dbdir.setText(f"AVCAD Database: {dbdir.as_posix()}")
        log_avcad_db_dir()

    @log_func_call
    def click_config(self):
        dlg = ConfigTreeDialog(self)
        dlg.show()
