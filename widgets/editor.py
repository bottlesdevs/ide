import html
from textwrap import wrap
from gi.repository import Gtk, Gdk, GtkSource

from backend.debugger import Debugger
from backend.intellisense import Intellisense


class Editor(Gtk.Paned):

    __dbg_color = "#fa973a"
    intellisense = Intellisense()
    
    source_scroll = Gtk.ScrolledWindow(vexpand=True, hexpand=True)
    debug_scroll = Gtk.ScrolledWindow(vexpand=True, hexpand=True)
    lang_manager = GtkSource.LanguageManager()
    style_scheme_manager = GtkSource.StyleSchemeManager()
    debug_buffer = Gtk.TextBuffer()
    source_buffer = GtkSource.Buffer(
        highlight_syntax=True,
        highlight_matching_brackets=True,
        style_scheme=style_scheme_manager.get_scheme("oblivion"),
        language=lang_manager.get_language("yaml")
    )
    source_view = GtkSource.View(
        wrap_mode=Gtk.WrapMode.WORD, 
        auto_indent=True, 
        indent_width=4, 
        tab_width=4, 
        indent_on_tab=True, 
        show_line_numbers=True, 
        insert_spaces_instead_of_tabs=True,
        buffer=source_buffer
    )
    debug_view = Gtk.TextView(
        wrap_mode=Gtk.WrapMode.WORD, 
        editable=False,
        buffer=debug_buffer
    )

    def __init__(self, app):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.app = app
        self.set_position(600)
        self.build_widgets()
    
    def build_widgets(self):
        self.source_view.get_completion().add_provider(self.intellisense)
        self.debug_view.get_style_context().add_class("debug-view")
        
        self.source_buffer.connect("changed", self.on_text_changed)

        self.source_scroll.add(self.source_view)
        self.debug_scroll.add(self.debug_view)
        self.add1(self.source_scroll)
        self.add2(self.debug_scroll)
    
    @property
    def text_iter(self, pos=None):
        iters = self.source_buffer.get_start_iter(), self.source_buffer.get_end_iter()
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
        text = self.source_buffer.get_text(self.text_iter[0], self.text_iter[1], False)
        validation = Debugger.validate_yaml(text)
        current = self.app.storage.get_current_file()
        self.source_view.do_show_completion(self.source_view)
        
        '''
        cursor_iter = self.source_buffer.get_iter_at_mark(self.source_buffer.get_insert())
        start_iter = cursor_iter.copy()
        start_iter.backward_word_start()
        word = self.source_buffer.get_text(start_iter, cursor_iter, False)

        if len(word) > 2:
            suggestions = self.intellisense.get_suggestions(word)
            if len(suggestions) > 0:
                coords = self.source_view.get_iter_location(cursor_iter)
                self.intellisense_popover.set_suggestions(suggestions, self.source_view, coords)
        '''
        
        if current:
            self.app.storage.set_file_err(current, html.escape(str(validation)))
            validation = html.escape(str(validation))
            _markup = f"<span color='{self.__dbg_color}'>{validation}</span>"
            self.debug_buffer.set_text("")
            self.debug_buffer.insert_markup(self.debug_iter[1], _markup, -1)

        self.app.toolbar.knock()
    
    def set_text(self, text):
        self.source_buffer.set_text(text)
        self.source_buffer.set_modified(False)
        self.source_view.set_cursor_visible(True)
        self.source_view.grab_focus()
    
    def get_text(self):
        return self.source_buffer.get_text(self.text_iter[0], self.text_iter[1], False)
    
    def knock(self):
        current = self.app.storage.get_current_file()
        if current:
            self.set_text(self.app.storage.get_file(current)["content"])
            self.debug_buffer.set_text(self.app.storage.get_file(current)["err"])
        else:
            self.set_text("")
            self.debug_buffer.set_text("")