from pyapp.gui.icons.iconfont import IconSpec
from pyapp.gui.icons.thirdparty.codicons import Codicons
from pyapp.gui.icons.thirdparty.codicons import names as codicon_names

NewIcon = IconSpec.generate_iconspec(Codicons, glyph=codicon_names.new_file)
OpenIcon = IconSpec.generate_iconspec(Codicons, glyph=codicon_names.folder_opened)  # noqa: E501
SaveIcon = IconSpec.generate_iconspec(Codicons, glyph=codicon_names.save)
SaveAsIcon = IconSpec.generate_iconspec(Codicons, glyph=codicon_names.save_as)
ConfigIcon = IconSpec.generate_iconspec(Codicons, glyph=codicon_names.json)
