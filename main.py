from src.gui import App
from configparser import ConfigParser
import os

configfile = 'gg.ini'
if not os.path.isfile(configfile):
    config = ConfigParser()
    config.add_section('database')
    config.set('database', 'path', 'grades.db')
    with open(configfile, 'w') as cf:
        config.write(cf)

if __name__ == "__main__":
    app = App()
    app.mainloop()
