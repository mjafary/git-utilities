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
        self.localbranches = []
        self.root = Tk()
        self.remotenames = []
        self.currentstatus = StringVar()
        self.rebaseremote = StringVar()
        self.rebase_button = ''
        self.quit_button = ''

        self.rebasecurrentbranch = IntVar()
        self.rebasecurrentbranch.set(0)

        self.pushtoorigin = IntVar()
        self.pushtoorigin.set(1)

        # Gather required information
        self.getcurrentbranchname()
        self.getremotenames()
        self.getlocalbranches()

    def getcurrentbranchname(self):
        """
        Get the current branch name
        """

        self.update_status('Getting current branch name')
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

    def getlocalbranches(self):
        """
        Get a list of current branches.
        """

        self.update_status('Getting list of local branches')
        try:
            # Run the git status command
            p1 = Popen(['git', 'branch'], stdout=PIPE)
            output = p1.communicate()[0]
            self.localbranches = output.decode('utf-8').replace('*', '').split()
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

        # Disable buttons
        self.quit_button['state'] = 'disabled'
        self.rebase_button['state'] = 'disabled'
        self.update_status('Checking out master branch')

        # Go to our master branch if we are not already there
        if self.startingbranch != 'master':
            self.checkout('master')

        # Fetch the other remote repositories
        self.fetchremote('upstream')
        self.fetchremote('origin')

        try:
            # Run the master rebase
            p1 = Popen(
                [
                    'git',
                    'rebase',
                    self.rebaseremote.get() + '/master'
                ],
                stdout=PIPE
            )
            output = p1.communicate()[0]

        except CalledProcessError:
            sys.stderr.write(
                "Unable to rebase to "\
                + self.rebaseremote.get()\
                + "/master\n")
            sys.exit(1)

        # Push master back to origin
        if self.pushtoorigin.get() == 1:
            self.update_status('Pushing master to origin repo')
            self.push_branch()

        # Go back to our initial branch
        if self.startingbranch != 'master':
            self.checkout(self.startingbranch)

            if self.rebasecurrentbranch.get() == 1:
                try:
                    # Run the master rebase
                    p1 = Popen(
                        [
                            'git',
                            'rebase',
                            'master'
                        ],
                        stdout=PIPE
                    )
                    output = p1.communicate()[0]
                    self.remotenames = output.decode('utf-8').split()
                except CalledProcessError:
                    sys.stderr.write(
                        "Unable to rebase to "\
                        + "master\n"
                    )
                    sys.exit(1)

        self.update_status('Complete')

        # Enable buttons
        self.quit_button['state'] = 'enabled'
        self.rebase_button['state'] = 'enabled'

        # self.quit()

    def update_status(self, statusmessage):
        """
        Forces an update of the UI status bar
        """

        self.currentstatus.set(statusmessage)
        self.root.update()

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

    def fetchremote(self, remotename):
        """
        Fetch the latest DB from the given remote
        """

        self.update_status('Updating database from ' + remotename)
        if remotename in self.remotenames:
            try:
                # Run the git status command
                p1 = Popen(['git', 'fetch', '--prune', remotename])
                output = p1.communicate()[0]
                if p1.returncode != 0:
                    sys.stderr.write("Unable to update " + remotename + "\n")
                    self.quit(1)
            except CalledProcessError:
                sys.stderr.write("Unable to update " + remotename + "\n")
                self.quit(1)

    def checkout(self, branchname):
        """
        Changes the current repo into the nominated branch
        """

        # First check that the branch exists
        if branchname in self.localbranches:
            self.update_status('Checking out ' + branchname)
            try:
                # Run the git status command
                p1 = Popen(['git', 'checkout', branchname])
                output = p1.communicate()[0]
                if p1.returncode != 0:
                    sys.stderr.write("Unable to checkout " + branchname + "\n")
                    self.quit(1)
            except CalledProcessError:
                sys.stderr.write("Unable to checkout " + branchname + "\n")
                self.quit(1)

    def push_branch(self):
        """
        Pushes the currently checked out branch up to the origin
        """

        # First check that the branch exists
        self.update_status('Pushing branch to origin')
        try:
            # Run the git status command
            p1 = Popen(['git', 'push'])
            output = p1.communicate()[0]
            if p1.returncode != 0:
                sys.stderr.write("Unable to push branch\n")
                self.quit(1)
        except CalledProcessError:
            sys.stderr.write("Unable to push branch\n")
            self.quit(1)

    def run(self):
        """
        Run the program
        """

        # Set up the root window
        self.root.title(self.startingbranch)
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        mainframe = ttk.Frame(
            self.root,
            padding="3 3 3 3"
        )
        mainframe.rowconfigure(0, weight=1)
        mainframe.columnconfigure(0, weight=1)
        mainframe.grid(
            column=0,
            row=0,
            sticky=(N, W, E, S)
        )

        # Notify of the current branch
        ttk.Label(mainframe, text='Current Branch:').grid(
            column=1,
            row=1,
            sticky=W
        )
        ttk.Label(
            mainframe,
            text=self.startingbranch,
            foreground='red').grid(
                column=2,
                row=1,
                sticky=W)

        # Remote to rebase against
        ttk.Label(mainframe,
                  text='Rebase Against:')\
            .grid(column=1, row=2, sticky=W)

        cb1 = ttk.Combobox(mainframe,
                           textvariable=self.rebaseremote,
                           values=self.remotenames,
                           state='readonly')
        cb1.grid(column=2,
                 row=2,
                 sticky=W)

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

        # Separator
        ttk.Separator(mainframe).grid(
            column=1,
            row=5,
            sticky=(W, E),
            columnspan=2
        )

        # Status bar
        ttk.Label(mainframe,
                  textvariable=self.currentstatus)\
                  .grid(
                      column=1,
                      row=6,
                      sticky=W,
                      columnspan=2
                  )

        # Separator
        ttk.Separator(mainframe).grid(
            column=1,
            row=7,
            sticky=(W, E),
            columnspan=2
        )

        # Add buttons at the bottom
        self.quit_button = ttk.Button(
            mainframe,
            text='Quit',
            command=self.quit
        )
        self.quit_button.grid(column=1, row=8, sticky=W)

        self.rebase_button = ttk.Button(
            mainframe,
            text='Rebase',
            command=self.rebase
        )
        self.rebase_button.grid(column=2, row=8, sticky=E)

        for x in range(2):
            mainframe.columnconfigure(x, weight=1)
        for y in range(8):
            mainframe.rowconfigure(y, weight=1)

        self.root.mainloop()

if __name__ == '__main__':

    app = App()
    app.run()

