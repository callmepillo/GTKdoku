import os
os.environ["GSK_RENDERER"] = "cairo"

# Load Gtk
import gi

from sudoku import all_is_valid

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk, Gio, GLib

# Load sudoku
import sudoku as sud

class AppWindow(Gtk.ApplicationWindow):
    def __init__(self, app, **kargs):
        super().__init__(application=app, **kargs, title='Hello World')
        self.set_resizable(False)
        self.set_default_size(400, 400)
        self.table = []
        self.arr = []
        self.selected = None

        # box
        box = Gtk.Box(orientation=1, spacing=6)
        self.set_child(box)

        # grid
        grid = Gtk.Grid(column_spacing=0, row_spacing=0)
        box.append(grid)

        for i in range(81):
            btn = Gtk.ToggleButton(label=f"")
            btn.connect('toggled', self.on_sudoku_clicked, i)
            btn.add_css_class("simple-button")

            row = i // 9
            col = i % 9
            if row % 3 == 0 and row != 0:
                btn.add_css_class("thick-top")
            if col % 3 == 0 and col != 0:
                btn.add_css_class("thick-left")

            self.table.append(btn)
            aspect = Gtk.AspectFrame.new(0, 0.5, 1/1, False)
            aspect.set_child(btn)
            grid.attach(aspect, i%9, i//9, 1, 1)

        gen_sudoku = Gtk.Button.new_with_mnemonic(label='_Sudoku')
        gen_sudoku.connect('clicked', self.on_gen_sudoku)
        box.append(gen_sudoku)

        exit_btn = Gtk.Button.new_with_mnemonic(label='_Goodbye')
        exit_btn.props.hexpand = True
        exit_btn.connect('clicked', self.on_button_close)
        box.append(exit_btn)

        self.cor = Gtk.Label(label="nothing now")
        box.append(self.cor)

        self.add_keybinding()
        self.load_css()

    def on_sudoku_clicked(self, button, name):
        if button.props.active:
            state = 'on'
            self.selected = button
            for btn in self.table:
                if btn.props.active and btn is not button:
                    btn.props.active = False
        else:
            state = 'off'
            if self.selected is button:
                self.selected = None

        print('Button', name, 'was turned', state)
        if self.selected is not None:
            print('Selected: ', self.table.index(self.selected))
        else:
            print('Selected: None')

    def on_gen_sudoku(self, _widget):
        self.restart_board()
        self.arr = sud.shadow_elements(sud.get_sudoku(), 81-76)

        for i in range(81):
            if self.arr[i] != 0:
                self.table[i].set_label(f"{self.arr[i]}")
                self.table[i].set_sensitive(False)
            else:
                self.table[i].set_label(f"")
                self.table[i].set_sensitive(True)
        self.update_board(0)

    def on_button_close(self, _widget):
        print('bye')
        self.close()

    def load_css(self):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path("style.css")

        display = Gdk.Display.get_default()
        Gtk.StyleContext.add_provider_for_display(
            display,
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def add_keybinding(self):
        # Create the action
        for i in range(10):
            name = f"press_{i}"
            action = Gio.SimpleAction.new(name, None)
            action.connect("activate", self.on_press_number, i)
            self.add_action(action)

            # Set the shortcut (accelerator)
            self.get_application().set_accels_for_action(f"win.{name}", [f"{i}"])

    def on_press_number(self, action, param, num):
        if not self.arr:
            return
        if self.selected is None:
            return
        item = self.table.index(self.selected)
        if num != 0:
            self.selected.set_label(f"{num}")
            self.arr[item] = num
        else:
            self.selected.set_label("")
            self.arr[item] = 0
        self.update_board(item)

    def update_board(self, item):
        if not self.arr:
            return
        val, info, a, b = sud.is_valid(self.arr, item)
        self.cor.set_text(f"{val}, {info}, {a}, {b}")

        for btn in self.table:
            btn.remove_css_class("red-button")
            btn.add_css_class("simple-button")

        if not val:
            a = self.table[a]
            a.remove_css_class("simple-button")
            a.add_css_class("red-button")
            b = self.table[b]
            b.remove_css_class("simple-button")
            b.add_css_class("red-button")
            return

        if all_is_valid(self.arr):
            self.game_over()

    def game_over(self):
        for btn in self.table:
            btn.remove_css_class("simple-button")
            btn.add_css_class("green-button")
            btn.set_sensitive(False)

    def restart_board(self):
        for btn in self.table:
            btn.remove_css_class("green-button")
            btn.add_css_class("simple-button")
            btn.set_sensitive(True)


class App(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.example.GridKeybinding")
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        window = AppWindow(app)
        window.present()



# When the application is launched…
def on_activate(app):
    # create an app
    app = App()
    # run it
    app.run()

