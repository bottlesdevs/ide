from gi.repository import Gtk


class FileEntry(Gtk.ListBoxRow):
    def __init__(self, app, file):
        super().__init__()
        self.app = app
        self.file = file
        self.build_widgets()

    def build_widgets(self):
        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.btn_close = Gtk.Button.new_from_icon_name("window-close-symbolic", Gtk.IconSize.BUTTON)
        self.label = Gtk.Label(self.file["name"], xalign=0)
        
        self.label.get_style_context().add_class("file-entry")
        self.btn_close.set_relief(Gtk.ReliefStyle.NONE)

        self.label.set_tooltip_text(self.file["path"])
        self.btn_close.set_tooltip_text("Close this file")

        self.btn_close.connect("clicked", self.on_close_clicked)

        self.box.pack_start(self.btn_close, False, False, 0)
        self.box.pack_start(self.label, True, True, 0)

        self.add(self.box)

    def on_click(self, widget):
        self.app.storage.set_current_file(self.file["name"])
    
    def on_close_clicked(self, widget):
        self.app.storage.remove_file(self.file["path"])
        self.app.knock()


class Sidebar(Gtk.Box):

    def __init__(self, app):
        Gtk.Box.__init__(self)
        self.app = app
        self.build_widgets()
    
    def build_widgets(self):
        self.files_list = Gtk.ListBox(vexpand=True, hexpand=True, selection_mode=Gtk.SelectionMode.SINGLE, activate_on_single_click=True)
        self.files_list.connect("row-activated", self.on_row_activated)
        self.add(self.files_list)
    
    def on_row_activated(self, widget, row):
        self.app.storage.set_current_file(row.file["path"])
        self.app.editor.knock()
        self.app.toolbar.knock()
    
    def add_file(self, file):
        _file = FileEntry(self.app, file)
        self.files_list.add(_file)
        self.files_list.show_all()
    
    def remove_file(self, file_name):
        for row in self.files_list.get_children():
            if row.get_child().get_text() == file_name:
                self.files_list.remove(row)
                break
        
        self.files_list.show_all()
    
    def knock(self):
        self.files_list.foreach(self.files_list.remove)
        for file_name in self.app.storage.get_files():
            _file = self.app.storage.get_file(file_name)
            self.add_file(_file)
