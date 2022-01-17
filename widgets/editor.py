import html
from textwrap import wrap
from gi.repository import Gtk, Gdk, GtkSource

from backend.debugger import Debugger
from backend.intellisense import Intellisense


class Editor(Gtk.Paned):

    __dbg_color = "#fa973a"
    intellisense = Intellisense()

    def __init__(self, app):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.app = app
        self.set_position(600)
        self.build_widgets()
    
    def build_widgets(self):
        self.text_scroll = Gtk.ScrolledWindow(vexpand=True, hexpand=True)
        self.debug_scroll = Gtk.ScrolledWindow(vexpand=True, hexpand=True)
        self.text_view = GtkSource.View(wrap_mode=Gtk.WrapMode.WORD, auto_indent=True, indent_width=4, tab_width=4, indent_on_tab=True, show_line_numbers=True, insert_spaces_instead_of_tabs=True)
        self.debug_view = Gtk.TextView(wrap_mode=Gtk.WrapMode.WORD, editable=False)

        self.text_view.get_completion().add_provider(self.intellisense)

        self.debug_view.get_style_context().add_class("debug-view")
        
        self.text_buffer = self.text_view.get_buffer()
        self.text_buffer.connect("changed", self.on_text_changed)

        self.debug_buffer = self.debug_view.get_buffer()

        self.text_scroll.add(self.text_view)
        self.debug_scroll.add(self.debug_view)
        self.add1(self.text_scroll)
        self.add2(self.debug_scroll)
    
    @property
    def text_iter(self, pos=None):
        iters = self.text_buffer.get_start_iter(), self.text_buffer.get_end_iter()
        if pos:
            return iters[pos]
        return iters
    
    @property
    def debug_iter(self, pos=None):
        iters = self.debug_buffer.get_start_iter(), self.debug_buffer.get_end_iter()
        if pos:
            return iters[pos]
        return iters

    def on_text_changed(self, widget):
        text = self.text_buffer.get_text(self.text_iter[0], self.text_iter[1], False)
        validation = Debugger.validate_yaml(text)
        current = self.app.storage.get_current_file()
        self.text_view.do_show_completion(self.text_view)
        
        '''
        cursor_iter = self.text_buffer.get_iter_at_mark(self.text_buffer.get_insert())
        start_iter = cursor_iter.copy()
        start_iter.backward_word_start()
        word = self.text_buffer.get_text(start_iter, cursor_iter, False)

        if len(word) > 2:
            suggestions = self.intellisense.get_suggestions(word)
            if len(suggestions) > 0:
                coords = self.text_view.get_iter_location(cursor_iter)
                self.intellisense_popover.set_suggestions(suggestions, self.text_view, coords)
        '''
        
        if current:
            self.app.storage.set_file_err(current, html.escape(str(validation)))
            validation = html.escape(str(validation))
            _markup = f"<span color='{self.__dbg_color}'>{validation}</span>"
            self.debug_buffer.set_text("")
            self.debug_buffer.insert_markup(self.debug_iter[1], _markup, -1)

        self.app.toolbar.knock()
    
    def set_text(self, text):
        self.text_buffer.set_text(text)
        self.text_buffer.set_modified(False)
        self.text_view.set_cursor_visible(True)
        self.text_view.grab_focus()
    
    def get_text(self):
        return self.text_buffer.get_text(self.text_iter[0], self.text_iter[1], False)
    
    def knock(self):
        current = self.app.storage.get_current_file()
        if current:
            self.set_text(self.app.storage.get_file(current)["content"])
            self.debug_buffer.set_text(self.app.storage.get_file(current)["err"])
        else:
            self.set_text("")
            self.debug_buffer.set_text("")