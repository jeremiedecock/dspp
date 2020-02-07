#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2012,2014,2020 Jérémie DECOCK (http://www.jdhp.org)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Debian packages required:
# - python3-poppler-qt5

# See: http://stackoverflow.com/questions/10562945/how-to-display-pdf-with-python-poppler-qt4
#      http://web.archive.org/web/20120417095851/http://www.rkblog.rk.edu.pl/w/p/rendering-pdf-files-pyqt4-pypoppler-qt4/
#      http://bazaar.launchpad.net/~j-corwin/openlp/pdf/annotate/head:/openlp/plugins/presentations/lib/pdfcontroller.py

# Pointeur Boulanger (xev):
# - left: keycode 112 (keysym 0xff55, Prior) (PgPrec)
# - right: keycode 117 (keysym 0xff56, Next) (PgSuiv)
# - fullscreen: keycode 50 (keysym 0xffe1, Shift_L) + keycode 71 (keysym 0xffc2, F5)
# - Echap: keycode 9 (keysym 0xff1b, Escape)

REMOTE_CONTROL=True

"""
Dual Screen PDF Presenter.
"""

#######################################

import sys
import argparse

try:
    from PyQt5 import QtGui, QtCore
    from PyQt5.QtGui import QPixmap
    from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QLabel, QVBoxLayout
except ImportError as e:
    print("Error: PyQt5 is not installed or not found.")
    sys.exit(1)
    
try:
    import popplerqt5
except ImportError as e:
    print("Error: Poppler for Qt5 is not installed or not found.")
    sys.exit(1)

#######################################

DEFAULT_SCALE_FACTOR = 1.0
DEFAULT_SCREEN0_ID = 0
DEFAULT_SCREEN1_ID = 1

class Screen():
    """
    A class which represent a computer's screen.
    """
    def __init__(self, num, geometry):
        self.num = num
        self.geometry = geometry
        self.top = geometry.top()
        self.bottom = geometry.bottom()
        self.left = geometry.left()
        self.right = geometry.right()
        self.width = geometry.width()
        self.height = geometry.height()

    def __str__(self):
        return "Screen {0} [{1}, {2}, {3}, {4}] ({5}, {6})".format(self.num, self.top, self.bottom, self.left, self.right, self.width, self.height)

class PDFController():
    # TODO
    def __init__(self, window_slides, window_notes):
        self.window_slides = window_slides
        self.window_notes = window_notes

        self.current_page_num = -1
        self.num_pages = max(self.window_slides.num_pages, self.window_notes.num_pages)

    def update(self, e):
        """
        Handle keypress envents:
            Escape:   Quit
            Return:   Next slide
            Space:    Next slide
            PageUp:   Slide - 5
            PageDown: Slide + 5
            Home:     Go to the first slide
            End:      Go to the first slide
            Left:     Previous slide
            Right:    Next slide
            Up:       Previous slide
            Down:     Next slide
            Plus:     Zoom in
            Minus:    Zoom out
            Tab:      Switch screens
        """
        # See http://pyqt.sourceforge.net/Docs/PyQt4/qt.html#Key-enum for all keys
        if e.key() == QtCore.Qt.Key_Escape:
            if REMOTE_CONTROL:
                pass
            else:
                self.window_slides.close()
                self.window_notes.close()

        if e.key() == QtCore.Qt.Key_Q:
            self.window_slides.close()
            self.window_notes.close()

        elif e.key() == QtCore.Qt.Key_Return:
            self.current_page_num = min(self.current_page_num + 1, self.num_pages - 1)
            self.renderCurrentPage()

        elif e.key() == QtCore.Qt.Key_Space:
            self.current_page_num = min(self.current_page_num + 1, self.num_pages - 1)
            self.renderCurrentPage()

        elif e.key() == QtCore.Qt.Key_PageUp:
            if REMOTE_CONTROL:
                self.current_page_num = max(self.current_page_num - 1, 0)
            else:
                self.current_page_num = max(self.current_page_num - 5, 0)
            self.renderCurrentPage()

        elif e.key() == QtCore.Qt.Key_PageDown:
            if REMOTE_CONTROL:
                self.current_page_num = min(self.current_page_num + 1, self.num_pages - 1)
            else:
                self.current_page_num = min(self.current_page_num + 5, self.num_pages - 1)
            self.renderCurrentPage()

        elif e.key() == QtCore.Qt.Key_K:
            self.current_page_num = max(self.current_page_num - 5, 0)
            self.renderCurrentPage()

        elif e.key() == QtCore.Qt.Key_J:
            self.current_page_num = min(self.current_page_num + 5, self.num_pages - 1)
            self.renderCurrentPage()

        elif e.key() == QtCore.Qt.Key_H:
            self.current_page_num = max(self.current_page_num - 10, 0)
            self.renderCurrentPage()

        elif e.key() == QtCore.Qt.Key_L:
            self.current_page_num = min(self.current_page_num + 10, self.num_pages - 1)
            self.renderCurrentPage()

        elif e.key() == QtCore.Qt.Key_Home:
            self.current_page_num = 0
            self.renderCurrentPage()

        elif e.key() == QtCore.Qt.Key_End:
            self.current_page_num = self.num_pages - 1
            self.renderCurrentPage()

        elif e.key() == QtCore.Qt.Key_Left:
            self.current_page_num = max(self.current_page_num - 1, 0)
            self.renderCurrentPage()

        elif e.key() == QtCore.Qt.Key_Right:
            self.current_page_num = min(self.current_page_num + 1, self.num_pages - 1)
            self.renderCurrentPage()

        elif e.key() == QtCore.Qt.Key_Up:
            self.current_page_num = max(self.current_page_num - 1, 0)
            self.renderCurrentPage()

        elif e.key() == QtCore.Qt.Key_Down:
            self.current_page_num = min(self.current_page_num + 1, self.num_pages - 1)
            self.renderCurrentPage()

        elif e.key() == QtCore.Qt.Key_Plus:
            self.window_slides.scale_factor += 0.1
            self.renderCurrentPage()

        elif e.key() == QtCore.Qt.Key_Minus:
            self.window_slides.scale_factor -= 0.1
            self.renderCurrentPage()

        elif e.key() == QtCore.Qt.Key_Tab:
            # Switch screen
            self.window_slides.screen, self.window_notes.screen = self.window_notes.screen, self.window_slides.screen

            self.window_slides.showNormal() # required
            self.window_notes.showNormal()  # required

            self.window_slides.move(self.window_slides.screen.left, self.window_slides.screen.top)
            self.window_notes.move(self.window_notes.screen.left, self.window_notes.screen.top)

            self.window_slides.showFullScreen()
            self.window_notes.showFullScreen()

            self.renderCurrentPage()

    def renderCurrentPage(self):
        self.window_slides.updatePdfPagePixmap()
        self.window_notes.updatePdfPagePixmap()



class Window(QWidget):
    """
    Extends Qt widget class.
    """

    def __init__(self, name, doc, screen):
        super(Window, self).__init__()

        self.name = name
        self.pdf_controller = None
        self.scale_factor = DEFAULT_SCALE_FACTOR

        self.doc = doc
        self.screen = screen

        self.num_pages = self.doc.numPages()

        # Create a label with the pixmap
        self.label = QLabel(self)
        #self.label.setAlignment(QtCore.Qt.AlignCenter)  # To center the label (ie the image)  # TODO
        self.label.setAlignment(QtCore.Qt.AlignHCenter)  # To center the label (ie the image)  # TODO

        # Create the layout
        vbox = QVBoxLayout()
        vbox.addWidget(self.label)

        # Set the layout
        self.setLayout(vbox)

        self.resize(800, 600)
        self.setWindowTitle(name)
        self.setStyleSheet("background-color:black;")  # TODO: or white ?

        #self.show()

    def updatePdfPagePixmap(self):
        """
        Render the current PDF page into a pixmap and asign it to a QLabel
        widget.
        """
        if self.pdf_controller is not None:
            page = self.doc.page(self.pdf_controller.current_page_num)

            if page is not None:
                #print self.name, "---"
                #print self.frameSize().width()
                #print self.frameSize().height()
                #print page.pageSize().width()
                #print page.pageSize().height()
                #print "---"

                ratio_x = self.scale_factor * self.screen.width / page.pageSize().width()
                ratio_y = self.scale_factor * self.screen.height / page.pageSize().height()
                ratio = min(ratio_x, ratio_y)

                # See http://people.freedesktop.org/~aacid/docs/qt4/classPoppler_1_1Page.html
                # page.renderToImage(xres=72.0, yres=72.0, x=-1, y=-1, width=-1, height=-1, rotate)
                # 
                # Parameters
                #   x   specifies the left x-coordinate of the box, in pixels.
                #   y   specifies the top y-coordinate of the box, in pixels.
                #   w   specifies the width of the box, in pixels.
                #   h   specifies the height of the box, in pixels.
                #   xres    horizontal resolution of the graphics device, in dots per inch
                #   yres    vertical resolution of the graphics device, in dots per inch
                #   rotate  how to rotate the page
                image = page.renderToImage(72. * ratio, 72. * ratio)
                pixmap = QPixmap.fromImage(image)

                self.label.setPixmap(pixmap)
            else:
                self.label.setPixmap(None)     # TODO: raise an exception: "TypeError: QLabel.setPixmap(QPixmap): argument 1 has unexpected type 'NoneType'"

    def keyPressEvent(self, e):
        """
        Handle keyboard press events.
        """
        if self.pdf_controller is not None:
            self.pdf_controller.update(e)

def main():
    """Main function"""

    # PARSE OPTIONS ###################

    parser = argparse.ArgumentParser(description='PDF Presenter Dual Head.')

    parser.add_argument("--notes", "-n",  help="Notes (PDF files)", metavar="FILE")
    parser.add_argument("fileargs", nargs=1, metavar="FILE", help="Slides (PDF file)")

    args = parser.parse_args()

    # TODO: test arguments
    slides_pdf_file_path = args.fileargs[0]
    notes_pdf_file_path = args.notes

    # POPPLER #########################

    slides_doc = popplerqt5.Poppler.Document.load(slides_pdf_file_path)
    #slides_doc.setRenderBackend(popplerqt5.Poppler.Document.SplashBackend) # ok (default)
    #slides_doc.setRenderBackend(popplerqt5.Poppler.Document.ArthurBackend) # bad
    slides_doc.setRenderHint(popplerqt5.Poppler.Document.Antialiasing)
    slides_doc.setRenderHint(popplerqt5.Poppler.Document.TextAntialiasing)

    notes_doc = popplerqt5.Poppler.Document.load(notes_pdf_file_path)
    #notes_doc.setRenderBackend(popplerqt5.Poppler.Document.SplashBackend) # ok (default)
    #notes_doc.setRenderBackend(popplerqt5.Poppler.Document.ArthurBackend) # bad
    notes_doc.setRenderHint(popplerqt5.Poppler.Document.Antialiasing)
    notes_doc.setRenderHint(popplerqt5.Poppler.Document.TextAntialiasing)

    # QT4 #############################

    app = QApplication(sys.argv)

    # For an application, the screen where the main widget resides is the
    # primary screen. This is stored in the primaryScreen property. All windows
    # opened in the context of the application should be constrained to the
    # boundaries of the primary screen; for example, it would be inconvenient
    # if a dialog box popped up on a different screen, or split over two
    # screens.
    desktop = QDesktopWidget()

    screen0 = Screen(DEFAULT_SCREEN0_ID, desktop.screenGeometry(DEFAULT_SCREEN0_ID))
    screen1 = Screen(DEFAULT_SCREEN1_ID, desktop.screenGeometry(DEFAULT_SCREEN1_ID))

    print(screen0)
    print(screen1)

    # The default constructor has no parent.
    # A widget with no parent is a window.
    window_slides = Window("PDF Presenter (Slides)", slides_doc, screen1)
    window_notes = Window("PDF Presenter (Notes)", notes_doc, screen0)

    window_slides.move(window_slides.screen.left, window_slides.screen.top)
    window_notes.move(window_notes.screen.left, window_notes.screen.top)

    window_slides.showFullScreen()
    window_notes.showFullScreen()

    pdf_controller = PDFController(window_slides, window_notes)
    window_slides.pdf_controller = pdf_controller
    window_notes.pdf_controller = pdf_controller

    # The mainloop of the application. The event handling starts from this point.
    # The exec_() method has an underscore. It is because the exec is a Python
    # keyword. And thus, exec_() was used instead. 
    exit_code = app.exec_()

    # The sys.exit() method ensures a clean exit.
    # The environment will be informed, how the application ended.
    sys.exit(exit_code)

if __name__ == '__main__':
    main()

