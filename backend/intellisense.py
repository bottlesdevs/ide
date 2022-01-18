import re
import yaml
from gi.repository import Gtk, GObject, GtkSource


class Intellisense(GObject.GObject, GtkSource.CompletionProvider):
    
    suggestions = {
        "install_msi": {
            "name": "install_msi",
            "content": [{
                "action": "install_msi",
                "file_name": "Example.msi",
                "url": "https://example/Example.msi",
                "file_checksum": "MD5_CHECKSUM",
                "arguments": "--example"
            }]
        }
    }

    def do_get_name(self):
        return "Intellisense"

    def do_get_icon(self):
        return None

    def do_get_activation(self):
        return GtkSource.CompletionActivation.USER_REQUESTED

    def do_get_info_widget(self, context):
        return None

    def do_match(self, context):
        return True

    def do_populate(self, context):
        proposals = []
        icon = Gtk.IconTheme.get_default().load_icon("system-run-symbolic", Gtk.IconSize.MENU, 0)

        end_iter = context.get_iter()
        if not isinstance(end_iter, Gtk.TextIter):
            _, end_iter = context.get_iter()

        if end_iter:
            buffer = end_iter.get_buffer()
            cursor_iter = buffer.get_iter_at_mark(buffer.get_insert())
            start_iter = cursor_iter.copy()
            start_iter.backward_word_start()
            text = buffer.get_text(start_iter, cursor_iter, False)
            
            if text:
                for key, value in self.suggestions.items():
                    if re.search(text, key):
                        content = yaml.dump(value["content"], default_flow_style=False, indent=4, sort_keys=False)
                        proposals.append(GtkSource.CompletionItem(label=key, text=content, icon=icon, info=None))

        context.add_proposals(self, proposals, True)
        return
