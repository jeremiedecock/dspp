# TODO

## Version 0.2

- [ ] Write a GTK+3 version ? (separate the backend and frontend to keep the Qt version in a separate file in addition to the GTK version).
      Motivation: Pypoppler is a bit outdated now (2014) as it only works with
      Python 2.x and Qt4 (see
      http://stackoverflow.com/questions/9682297/displaying-pdf-files-with-python3
      for alternatives...)

## Version 0.3

- [ ] New feature: move left/right, up/down the displayed PDF to make the zooming in/out feature more useful
- [ ] Fix the bug occurring when zooming in and then zooming out (vertically
      recenter the label) -> Alignment H et V => il faut forcer à redimensionner le
      label et la vbox (probablement un problème avec le Layout -> le supprimer ?)

## Version 0.4

- [ ] Add a clock on the note screen (and update it every seconds) -> cf. QTimer
- [ ] Check command options, check available screens, ...

## Version 0.5

- [ ] Handle the "only one screen" case
- [ ] Handle the "three or more screens" case: let choose the screen numbers to use in options

## Version 0.6

- [ ] Add an optional graphical user interface (dspp-gui.py) to choose the 2 PDF files and setup screens, timer, remote control keymap, alarms, ...

## Version 0.7

- [ ] Update the README file, write a more detailed description, add a
      tutorial to explain how to use it with LaTeX/Beamer (how to use notes in
      Beamer to generate 2 PDF), add a video demo, ...

## Version 1.0

- [ ] Add a setup.py file
- [ ] Create a Debian package
- [ ] Let it work on Windows platforms + add installation instructions for windows in the README file

## Misc

- Cf
    - http://blog.dorian-depriester.fr/linux/beamer-voir-ses-notes-sans-les-montrer-a-lassistance/
    - http://tex.stackexchange.com/questions/10197/in-beamer-slide-view-notes-on-computer-only-while-presenting-with-a-projector
