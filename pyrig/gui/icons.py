from pyapp.gui.icons.thirdparty.codicons import Codicons
from pyapp.gui.icons.thirdparty.codicons import names as codicon_names
from pyapp.gui.icons.iconfont import IconSpec


NewIcon = IconSpec.generate_iconspec(Codicons, codicon_names.new_file)
OpenIcon = IconSpec.generate_iconspec(Codicons, codicon_names.folder_opened)
SaveIcon = IconSpec.generate_iconspec(Codicons, codicon_names.save)
SaveAsIcon = IconSpec.generate_iconspec(Codicons, codicon_names.save_as)
ConfigIcon = IconSpec.generate_iconspec(Codicons, codicon_names.json)
