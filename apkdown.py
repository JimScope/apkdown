import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import json
import sys
import requests
from concurrent.futures.thread import ThreadPoolExecutor
from playstore.playstore import Playstore

# Default credentials file location.
credentials_default_location = 'credentials.json'

# Default directory where to save the downloaded applications.
downloaded_apk_default_location = 'Downloads'


class ApiData:
    """Retrieve data of the apk through the api"""

    def __init__(self, package_name):
        self.package_name = package_name
        self.icon = False

        try:
            app = api.app_details(self.package_name).docV2
        except:
            print(
                'Error when downloading "{0}". Unable to get app\'s details.'.
                format(self.package_name))
            sys.exit(1)

        self.details = {
            'package_name': app.docid,
            'title': app.title,
            'creator': app.creator
        }

        for image in app.image:
            if image.imageType == 4:
                response = requests.get(image.imageUrl)
                if response.status_code == 200:
                    with open('apk_icon.png', 'wb') as f:
                        f.write(response.content)
                    self.icon = True
                    break



class Downloader(Gtk.Window):
    """docstring for Downloader"""

    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("gui.glade")
        self.builder.connect_signals(self)

        # Load windows from gui.glade
        self.window = self.builder.get_object("MainWindow")
        self.AboutDialog = self.builder.get_object("AboutDialog")
        self.WindowConf = self.builder.get_object("WindowConf")

        # Load objects from gui.glade
        self.apk_image = self.builder.get_object("apk_image")
        self.progressbar = self.builder.get_object("progressbar")
        self.input_address = self.builder.get_object("input_address")
        self.label_package = self.builder.get_object("label_package")
        self.label_title = self.builder.get_object("label_title")
        self.label_developer = self.builder.get_object("label_developer")

    def on_MainWindow_destroy(self, *args):
        thread.shutdown(wait=True)
        Gtk.main_quit(*args)

    def on_btn_about_clicked(self, widget):
        self.AboutDialog.run()
        self.AboutDialog.hide()

    def on_btn_conf_clicked(self, button):
        self.WindowConf.show()

    def on_btn_save_clicked(self, button):
        pass

    def on_btn_download_clicked(self, button):
        pass

    def check_url(self, widget):
        thread.submit(self.check)

    def check(self):
        package = self.input_address.get_text()
        if package != '':
            data = ApiData(package)

            info = data.details
            self.label_package.set_text(info['package_name'])
            self.label_title.set_text(info['title'])
            self.label_developer.set_text(info['creator'])

            if data.icon == True:
                self.apk_image.set_from_file('apk_icon.png')
            else:
                pass


if __name__ == '__main__':
    try:
        api = Playstore(credentials_default_location)
    except:
        print("Connect to Internet")
    thread = ThreadPoolExecutor(1)
    win = Downloader()
    win.window.connect("delete_event", Gtk.main_quit)
    win.window.show_all()
    Gtk.main()
