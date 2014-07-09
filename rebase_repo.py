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

    def __init__(self):
        """
        Initializes all of the current repository information
        """

        # Set some defaults
        self.startingbranch = ''
        self.root = Tk()
        self.remotenames = []
        self.rebaseremote = StringVar()

        self.rebasecurrentbranch = IntVar()
        self.rebasecurrentbranch.set(0)

        self.pushtoorigin = IntVar()
        self.pushtoorigin.set(1)

        # Gather required information
        self.getcurrentbranchname()
        self.getremotenames()

    def getcurrentbranchname(self):
        """
        Get the current branch name
        """

        branchname = re.compile(r"^On branch (?P<branchname>.*?)\n")
        try:
            # Run the git status command
            p = Popen(['git', 'status'], stdout=PIPE)
            output = p.communicate()[0]
            self.startingbranch = branchname\
                .search(output.decode('utf-8')).group('branchname')
        except CalledProcessError:
            sys.stderr.write("Unable to get current branch name\n")
            sys.exit(1)

    def quit(self, exitcode=0):
        """
        Quits the current application
        """
        sys.exit(exitcode)

    def rebase(self):
        """
        Rebases the using the given options
        """

        # Debugging - Print out the known variables
        print('Starting Branch', self.startingbranch)
        print('Known remotes: ', ", ".join(self.remotenames))
        print('Rebase to the following remote: ', self.rebaseremote.get())
        print('Rebase my current branch as well?: ',
              self.rebasecurrentbranch.get())
        print('Push to my origin repo?: ', self.pushtoorigin.get())

        self.quit()

    def getremotenames(self):
        """
        Glean the git remote repos from the system
        """

        try:
            # Run the git status command
            p = Popen(['git', 'remote'], stdout=PIPE)
            output = p.communicate()[0]
            self.remotenames = output.decode('utf-8').split()
        except CalledProcessError:
            sys.stderr.write("Unable to get remote repo names\n")
            sys.exit(1)

    def creategui(self):
        """
        Run the GUI
        """

        # Set up the root window
        self.root.title(self.startingbranch)

        mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        # Notify of the current branch
        ttk.Label(mainframe, text='Current Branch:').grid(
            column=1,
            row=1,
            sticky=(W, E)
        )
        ttk.Label(
            mainframe,
            text=self.startingbranch,
            foreground='red').grid(
                column=2,
                row=1,
                sticky=(W, E))

        # Remote to rebase against
        ttk.Label(mainframe,
                  text='Rebase Against:')\
            .grid(column=1, row=2, sticky=(W, E))

        cb1 = ttk.Combobox(mainframe,
                           textvariable=self.rebaseremote,
                           values=self.remotenames,
                           state='readonly')
        cb1.grid(column=2,
                 row=2,
                 sticky=(W, E))

        # If upstream exists, set it to the default
        if 'upstream' in self.remotenames:
            cb1.set('upstream')
        else:
            cb1.current(0)

        # If we are not on master, see if user wants to
        # rebase the current branch as well
        ttk.Label(mainframe,
                  text='Rebase Current Branch?')\
                  .grid(column=1,
                        row=3,
                        sticky=W)
        cb2 = ttk.Checkbutton(mainframe,
                              variable=self.rebasecurrentbranch)
        cb2.grid(column=2, row=3, sticky=E)

        # If the default branch is master, set it to 1, and
        # make it readonly
        if self.startingbranch == 'master':
            self.rebasecurrentbranch.set(1)
            cb2.configure(state='disabled')

        # Push to our origin after rebase?
        ttk.Label(mainframe,
                  text='Push to Origin?')\
                  .grid(column=1, row=4, sticky=W)
        cb3 = ttk.Checkbutton(mainframe,
                              variable=self.pushtoorigin)
        cb3.grid(column=2,
                 row=4,
                 sticky=E)

        # Add buttons at the bottom
        ttk.Button(mainframe,
                   text='Quit',
                   command=self.quit)\
            .grid(column=1, row=5, sticky=W)

        ttk.Button(mainframe,
                   text='Rebase',
                   command=self.rebase)\
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

        self.root.mainloop()

if __name__ == '__main__':

    app = App()
    app.creategui()

