import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '3.0')
from gi.repository import Gtk, Gdk

from backend.storage import FilesStorage

from widgets.toolbar import Toolbar
from widgets.sidebar import Sidebar
from widgets.editor import Editor
    

class BottlesIDE(Gtk.ApplicationWindow):

    storage = FilesStorage()

    def __init__(self):
        Gtk.Window.__init__(self, title="Bottles IDE", resizable=True)
        self.set_default_size(1200, 800)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_stylesheet()

        self.toolbar = Toolbar(self)
        self.sidebar = Sidebar(self)
        self.editor = Editor(self)
        
        self.build_widgets()
    
    def set_stylesheet(self):
        settings = Gtk.Settings.get_default()
        settings.set_property("gtk-application-prefer-dark-theme", True)

        css_provider = Gtk.CssProvider()
        css_provider.load_from_path('style.css')
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
    
    def knock(self):
        self.sidebar.knock()
        self.editor.knock()
    
    def build_widgets(self):
        self.set_titlebar(self.toolbar)

        self.main_box = Gtk.Paned()
        self.main_box.set_position(300)
        self.main_box.add1(self.sidebar)
        self.main_box.add2(self.editor)
        self.add(self.main_box)


if __name__ == "__main__":
    window = BottlesIDE()
    window.connect("delete-event", Gtk.main_quit)
    window.show_all()
    Gtk.main()