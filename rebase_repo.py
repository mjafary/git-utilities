#!/usr/bin/env python3

"""
Graphical interface for rebasing your repository

Requires: python-git, python-tk
"""
from tkinter import *
from tkinter import ttk
import re
import os
from subprocess import *

class App:
    """
    Gathers information on the current repositories,
    and allows rebasing for the upstream
    """

    startingbranch = ''

    def __init__(self):
        """
        Initializes all of the current repository information
        and runs the gui
        """

        self.getcurrentbranchname()
        self.creategui()

    def getcurrentbranchname(self):
        """
        Get the current branch name
        """

        branchname = re.compile(r"^On branch (?P<branchname>.*?)\n")
        try:
            # Run the git status command
            p1 = Popen(['git', 'status'], stdout=PIPE)
            output = p1.communicate()[0]
            self.startingbranch = branchname\
                .search(output.decode('utf-8')).group('branchname')
        except CalledProcessError:
            sys.stderr.write("Unable to get current branch name\n")
            sys.exit(1)

    def printoptions(self, mystring):
        """
        Debugging to check selection is correct
        """
        print(mystring)
    
    def quit(self):
        """
        Quits the current application
        """
        sys.exit(0)
    
    def rebase(self):
        """
        Rebases the using the given options
        """
        sys.exit(0)

    def creategui(self):
        """
        Run the GUI
        """

        # Set up the root window
        root = Tk()
        root.title(self.startingbranch)

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        # Notify of the current branch
        ttk.Label(mainframe, text='Current Branch:').grid(
        column=1, row=1, sticky=(W, E))
        ttk.Label(mainframe, text=self.startingbranch, foreground='red').grid(
        column=2, row=1, sticky=(W, E))

        # Remote to rebase against
        rebaseremote = StringVar()
        ttk.Label(mainframe,
                  text='Rebase Against:')\
            .grid(column=1, row=2, sticky=(W, E))

        cb1 = ttk.Combobox(mainframe,
                           textvariable=rebaseremote,
                           values=['upstream', 'origin'],
                           state='readonly')
        cb1.current(0)
        cb1.grid(column=2,
                 row=2,
                 sticky=(W, E))

        # If we are not on master, see if user wants to 
        # rebase the current branch as well
        rebasecurrentbranch = IntVar()
        ttk.Label(mainframe,
                  text='Rebase Current Branch?')\
                  .grid(column=1,
                        row=3,
                        sticky=W)
        cb2 = ttk.Checkbutton(mainframe,
                              variable=rebasecurrentbranch)
        cb2.grid(column=2, row=3, sticky=E)

        # If the default branch is master, set it to 1, and
        # make it readonly
        if self.startingbranch == 'master':
            rebasecurrentbranch.set(1)
            cb2.configure(state='disabled')
            
        # Push to our origin after rebase?
        pushtoorigin = IntVar()
        pushtoorigin.set(1)
        ttk.Label(mainframe,
                  text='Push to Origin?')\
                  .grid(column=1, row=4, sticky=W)
        cb3 = ttk.Checkbutton(mainframe,
                              variable=pushtoorigin)
        cb3.grid(column=2,
                 row=4,
                 sticky=E)

        # Add buttons at the bottom
        ttk.Button(mainframe, text='Quit', command=quit)\
            .grid(column=1, row=5, sticky=W)

        ttk.Button(mainframe, text='Rebase', command=quit)\
            .grid(column=2, row=5, sticky=E)

        # feet = StringVar()
        # meters = StringVar()

        # feet_entry = ttk.Entry(mainframe,
        #                        width=7,
        #                        textvariable=feet)
        # feet_entry.grid(column=2, row=1, sticky=(W, E))

        # ttk.Label(mainframe, textvariable=meters).grid(
        # column=2, row=2, sticky=(W, E))
        # ttk.Button(
        # mainframe, text="Calculate", command=calculate).grid(
        # column=3, row=3, sticky=W)

        # ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
        # ttk.Label(mainframe,
        #           text="is equivalent to")\
        #          .grid(column=1, row=2, sticky=E)
        # ttk.Label(mainframe, text="meters")\
        #          .grid(column=3, row=2, sticky=W)

        # for child in mainframe.winfo_children():
        #     child.grid_configure(padx=5, pady=5)

        # feet_entry.focus()
        # root.bind('<Return>', calculate)


        root.mainloop()

if __name__ == '__main__':

    app = App()

