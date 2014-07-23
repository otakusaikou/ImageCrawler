from HTMLParser import HTMLParser
import pygtk
pygtk.require('2.0')
import gtk
import os, glob
import urllib

# Set constant
imgList = []
pattern = ""
_tag = ""
_attr = ""

class GUI:
    def __init__(self):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.connect("destroy", lambda w: gtk.main_quit())
        window.set_title("Image Crawler")
        window.set_size_request(450, 350)
        window.show()

        mainbox = gtk.VBox(False, 5)
        window.add(mainbox)
        mainbox.show()
        
        self.menu_items = (
            ('/_File', None, None, 0, '<Branch>'),
            ('/File/_Reset', '<control>R', self.reset, 0, None),
            ('/File/sep1', None, None, 0,'<Separator>'),
            ('/File/_Quit', '<control>Q', gtk.main_quit, 0, None),
            ('/_Help', None, None, 0,'<LastBranch>'),
            ('/Help/About', 'F1', self.show_about, 0, None)        
        )
        
        # Menu bar
        menubar = self.get_main_menu(window)
        mainbox.pack_start(menubar, False, True, 0)
        menubar.show()
       
        mainhbox = gtk.HBox(False, 5)
        mainhbox.set_border_width(10)
        mainbox.pack_start(mainhbox, False, True, 0)
        mainhbox.show()

        # Web link block
        frame = gtk.Frame()
        mainhbox.pack_start(frame, True, True, 0)
        frame.set_label("Web Link")

        vbox = gtk.VBox(False, 5)
        vbox.set_border_width(10)
        frame.add(vbox) 
        vbox.show()
        frame.show() 

        # First part
        hbox = gtk.HBox(False, 5)
        vbox.pack_start(hbox, True, True, 0)
        hbox.show()

        label = gtk.Label("First Part:")
        label.set_size_request(100, 20)
        label.set_alignment(xalign=0, yalign=0.5)
        hbox.pack_start(label, False, True, 0)
        label.show()
        self.firstPart = gtk.Entry()
        self.firstPart.set_size_request(-1, 20)
        hbox.pack_start(self.firstPart, True, True, 0)
        self.firstPart.show()
        
        # Second part
        hbox = gtk.HBox(False, 5)
        vbox.pack_start(hbox, True, True, 0)
        hbox.show()
                
        label = gtk.Label("Second Part:")
        label.set_size_request(100, 20)
        label.set_alignment(xalign=0, yalign=0.5)
        hbox.pack_start(label, False, True, 0)
        label.show()
        self.secondPart = gtk.Entry()
        self.secondPart.set_size_request(-1, 20)
        hbox.pack_start(self.secondPart, True, True, 0)
        self.secondPart.show()

        # Third part
        hbox = gtk.HBox(False, 5)
        vbox.pack_start(hbox, True, True, 0)
        hbox.show()
                
        label = gtk.Label("Third Part:")
        label.set_size_request(100, 20)
        label.set_alignment(xalign=0, yalign=0.5)
        hbox.pack_start(label, False, True, 0)
        label.show()
        self.thirdPart = gtk.Entry()
        self.thirdPart.set_size_request(-1, 20)
        hbox.pack_start(self.thirdPart, True, True, 0)
        self.thirdPart.show()

        # Page Count 
        hbox = gtk.HBox(False, 5)
        vbox.pack_start(hbox, True, True, 0)
        hbox.show()
                
        label = gtk.Label("Number Of Page:")
        label.set_size_request(100, 20)
        label.set_alignment(xalign=0, yalign=0.5)
        hbox.pack_start(label, False, True, 0)
        label.show()
        
        adj = gtk.Adjustment(value = 1, lower = 1, upper = 1000, step_incr = 1, page_incr = 10)
        self.pageCount = gtk.SpinButton(adj, 0, 0)
        self.pageCount.set_size_request(-1, 25)
        hbox.pack_start(self.pageCount, False, True, 0)
        self.pageCount.show()
       
        # Image link pattern 
        hbox = gtk.HBox(False, 5)
        vbox.pack_start(hbox, True, True, 0)
        hbox.show()  
        
        label = gtk.Label("Link Pattern:")
        label.set_size_request(100, 20)
        label.set_alignment(xalign=0, yalign=0.5)
        hbox.pack_start(label, False, True, 0)
        label.show()
        self.linkPattern = gtk.Entry()
        self.linkPattern.set_size_request(-1, 20)
        hbox.pack_start(self.linkPattern, True, True, 0)
        self.linkPattern.show()

        # Output link header 
        hbox = gtk.HBox(False, 5)
        vbox.pack_start(hbox, True, True, 0)
        hbox.show()  
        
        label = gtk.Label("Link Header:")
        label.set_size_request(100, 20)
        label.set_alignment(xalign=0, yalign=0.5)
        hbox.pack_start(label, False, True, 0)
        label.show()
        self.linkHeader = gtk.Entry()
        self.linkHeader.set_size_request(-1, 20)
        hbox.pack_start(self.linkHeader, True, True, 0)
        self.linkHeader.show()
        
        # Start button
        hbox = gtk.HBox(False, 5)
        mainbox.pack_start(hbox, False, True, 0)
        hbox.show()  

        self.button = gtk.Button("Srart")
        self.button.set_size_request(70, 25)
        self.button.connect("clicked", self.start_button_callback)
        hbox.pack_start(self.button, True, False, 15)
        self.button.show()
        
        # Config settings block
        frame = gtk.Frame()
        mainhbox.pack_start(frame, False, True, 0)
        frame.set_label("Config Settings")

        vbox = gtk.VBox(False, 0)
        vbox.set_border_width(10)
        frame.add(vbox) 
        vbox.show()
        frame.show() 
        
        self.useProxy = gtk.CheckButton("Use Proxy")
        self.useProxy.set_active(False)
        vbox.pack_start(self.useProxy, False, False, 10)
        self.useProxy.show()
        
        self.singlePage = gtk.CheckButton("Single Page")
        self.singlePage.set_active(False)
        self.singlePage.connect("toggled", self.changeOption)
        vbox.pack_start(self.singlePage, False, False, 10)
        self.singlePage.show()
        
        # Encoding 
        hbox = gtk.HBox(False, 5)
        vbox.pack_start(hbox, False, True, 10)
        hbox.show()
                
        label = gtk.Label("Encoding:")
        label.set_size_request(60, 20)
        label.set_alignment(xalign=0, yalign=0.5)
        hbox.pack_start(label, False, True, 0)
        label.show()
        self.encoding = gtk.Entry()
        self.encoding.set_size_request(40, 20)
        hbox.pack_start(self.encoding, True, True, 0)
        self.encoding.show()
    
        # Tag 
        hbox = gtk.HBox(False, 5)
        vbox.pack_start(hbox, False, True, 10)
        hbox.show()
                
        label = gtk.Label("Tag:")
        label.set_size_request(60, 20)
        label.set_alignment(xalign=0, yalign=0.5)
        hbox.pack_start(label, False, True, 0)
        label.show()
        self.tag = gtk.Entry()
        self.tag.set_text("img")
        self.tag.set_size_request(40, 20)
        hbox.pack_start(self.tag, True, True, 0)
        self.tag.show()

        # Attribute 
        hbox = gtk.HBox(False, 5)
        vbox.pack_start(hbox, False, True, 10)
        hbox.show()
                
        label = gtk.Label("Attribute:")
        label.set_size_request(60, 20)
        label.set_alignment(xalign=0, yalign=0.5)
        hbox.pack_start(label, False, True, 0)
        label.show()
        self.attribute = gtk.Entry()
        self.attribute.set_text("src")
        self.attribute.set_size_request(40, 20)
        hbox.pack_start(self.attribute, True, True, 0)
        self.attribute.show()

    def get_main_menu(self, window):
        accel_group = gtk.AccelGroup()
        item_factory = gtk.ItemFactory(gtk.MenuBar, '<main>', accel_group)
        item_factory.create_items(self.menu_items)
        window.add_accel_group(accel_group)
        self.item_factory = item_factory
        return item_factory.get_widget('<main>')
     
    # Show about dialog 
    def show_about(self, widget, data):
        dialog = gtk.AboutDialog()
        dialog.set_name("Image Crawler")
        dialog.set_version("0.9")
        dialog.set_authors(["Li-Sheng Chen (Otakusaikou), otakuzyoutou@gmail.com"])
        dialog.set_artists(["Li-Sheng Chen (Otakusaikou), otakuzyoutou@gmail.com"])
        dialog.set_comments("This is an image crawler.")
        dialog.set_license("Otakusaikou (c) All RIGHTS RESERVED")

        # Show dialog
        dialog.run()

        # Destroy method must be called otherwise the "Close" button will not work.
        dialog.destroy()

    # Reset input arguments
    def reset(self, tag, widget):
        self.firstPart.set_text("")
        self.secondPart.set_text("")
        self.thirdPart.set_text("")
        self.pageCount.set_value(1)
        self.linkPattern.set_text("")
        self.linkHeader.set_text("")
        self.useProxy.set_active(False)
        self.singlePage.set_active(False)
        self.encoding.set_text("")
        self.tag.set_text("img")
        self.attribute.set_text("src")
        global pattern, imgList
        pattern = ""
        imgList = []
    
    # Enable/Disable secondPart entry and pageCount spinbox by value of singlePage checkbutton 
    def changeOption(self, widget):
        flag = not self.singlePage.get_active()
        self.secondPart.set_sensitive(flag)
        self.thirdPart.set_sensitive(flag)
        self.pageCount.set_sensitive(flag)
        
    def start_button_callback(self, widget):
        global pattern, _tag, _attr 
        # Get linkPattern and assign it to global variable pattern
        pattern = self.linkPattern.get_text()
        # Get tag and assign it to global variable _tag 
        _tag = self.tag.get_text()
        # Get attribute and assign it to global variable _attr 
        _attr = self.attribute.get_text()

        h = MyParse()

        # Get url  
        URL = self.firstPart.get_text()
        if not URL.startswith("http://"):
            URL = "http://" + URL

        # Set proxies
        proxies = {'http': 'http://proxy.hinet.net:80'}

        # Crawl only one page if singlePage checkbutton is activated
        if self.singlePage.get_active():
            print "Read page: " + URL

            # Use proxy is useProxy checkbutton is activated
            if self.useProxy.get_active():
                page = urllib.urlopen(URL, proxies = proxies).read()
            else:
                page = urllib.urlopen(URL).read()

            # Decode the content of page if encoding checkbutton is activated
            encoding = self.encoding.get_text()
            if encoding != "":
                page = page.decode(encoding)

            h.feed(page)
        # Crawl multiple pages with given pattern
        else:
            # Get page count
            pageCount = int(self.pageCount.get_text())

            for i in range(1, pageCount + 1):
                # process page url
                if i == 1:
                    pageURL = URL + self.thirdPart.get_text() 
                else:
                    pageURL = URL + (self.secondPart.get_text() % i) + self.thirdPart.get_text() 
                print "Read page: " + pageURL

                # Use proxy is useProxy checkbutton is activated
                if self.useProxy.get_active():
                    page = urllib.urlopen(pageURL, proxies = proxies).read()
                else:
                    page = urllib.urlopen(pageURL).read()

                # Decode the content of page if encoding checkbutton is activated
                encoding = self.encoding.get_text()
                if encoding != "":
                    page = page.decode(encoding)

                h.feed(page) 

        count = 1
        global imgList
        if len(imgList) != 0:
            # Create output directory
            if not os.path.exists(os.path.join(os.path.expanduser('~'), "Desktop", "001down")):
                os.mkdir(os.path.join(os.path.expanduser('~'), "Desktop", "001down"))
                os.chdir(os.path.join(os.path.expanduser('~'), "Desktop", "001down"))
            else:
                os.chdir(os.path.join(os.path.expanduser('~'), "Desktop"))
                os.mkdir(os.path.join(os.path.expanduser('~'), "Desktop", "%03ddown" % (int(glob.glob("0*down")[-1][:-4]) + 1)))
                os.chdir(os.path.join(os.path.expanduser('~'), "Desktop", "%03ddown" % (int(glob.glob("0*down")[-1][:-4]))))

        for img in imgList:
            try:
                img = self.linkHeader.get_text() + img
                fout = open("%02d.jpg" % count, "wb")
                print "Get image: " + img 
    
                # Use proxy is useProxy checkbutton is activated
                if self.useProxy.get_active():
                    fout.write(urllib.urlopen(img, proxies = proxies).read())
                else:
                    fout.write(urllib.urlopen(img).read())
    
                fout.close()
                count += 1
            except:
                pass

        imgList = []
        print "Done!"

class MyParse(HTMLParser):
    def handle_starttag(self, tag, attrs):
        try:
            if tag == _tag:
                global imgList
                if dict(attrs)[_attr].startswith(pattern):
                    imgList.append(dict(attrs)[_attr])
        except:
            pass
        
def main():
    gtk.main()
    return 0
    
if __name__ == "__main__":
    GUI()
    main()
        
