import os
from gi.repository import Gtk


class Toolbar(Gtk.HeaderBar):
    __ico_size = Gtk.IconSize.BUTTON

    def __init__(self, app):
        Gtk.HeaderBar.__init__(self, show_close_button=True)
        self.app = app
        self.build_widgets()
        self.connect_signals()
        self.set_status("ok")
    
    def build_widgets(self):
        self.btn_open = Gtk.Button.new_from_icon_name("document-open-symbolic", self.__ico_size)
        self.btn_save = Gtk.Button.new_from_icon_name("document-save-symbolic", self.__ico_size)
        self.status_box = Gtk.Box()
        self.title = Gtk.Label.new("Bottles IDE")
        self.debug_box = Gtk.Box()

        self.btn_open.set_tooltip_text("Open a file")
        self.btn_save.set_tooltip_text("Save the file")
        self.pack_start(self.btn_open)
        self.pack_start(self.btn_save)

        self.debug_box.set_size_request(460, -1)
        self.debug_box.get_style_context().add_class("omnibar")
        self.title.set_halign(Gtk.Align.CENTER)
        self.title.set_size_request(400, -1)
        self.debug_box.add(self.status_box)
        self.debug_box.add(self.title)

        self.set_custom_title(self.debug_box)
    
    def connect_signals(self):
        self.btn_open.connect("clicked", self.on_open_clicked)
        # self.btn_save.connect("clicked", self.on_save_clicked)
    
    def on_open_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Open File", None, Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.title.set_text(os.path.basename(dialog.get_filename()))
            self.set_status("ok")
        
        file_name = dialog.get_filename()
        content = open(dialog.get_filename(), "r").read()
        self.app.storage.add_file(file_name, content)
        self.app.storage.set_current_file(file_name)
        self.app.knock()

        dialog.destroy()
    
    def set_status(self, status):
        statues = {
            "error": "dialog-error-symbolic",
            "ok": "object-select-symbolic"
        }
        for w in self.status_box.get_children():
            self.status_box.remove(w)
        
        ico = Gtk.Image.new_from_icon_name(statues[status], self.__ico_size)
        self.status_box.add(ico)
        self.status_box.show_all()
    
    def knock(self):
        current = self.app.storage.get_current_file()
        if current:
            file = self.app.storage.get_file(current)
            status = "ok" if len(file["err"]) == 0 else "error"
            self.title.set_text(file["name"])
            self.set_status(status)
        else:
            self.title.set_text("Bottles IDE")
