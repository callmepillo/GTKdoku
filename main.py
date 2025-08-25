import sudoku as sdku
from gui import Gtk, on_activate

def main():
    app = Gtk.Application(application_id='com.example.GtkApplication')
    app.connect('activate', on_activate)
    app.run(None)

if __name__=="__main__":
    main()