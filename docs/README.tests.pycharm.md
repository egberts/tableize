
This document covers setting up a project under `VirtualEnv` environment for
debugging the PyTest `unittest` unit test cases.

> 📝NOTE: This document is tailored for the Pelican SSG project which used `tests` subdirectory for all their unit test needs.  Other project can benefit from this HOWTO.


Some configuration needs to be made into project-wide settings of PyCharm IDE.

* test directory
* default `pelican` binary, location of
* limiting to 1 process during pytest for debug session
* Run/Debug Configuration setting

Test Directory
==============

Firstly, help the PyCharm IDE properly identify this Pelican Test
directory (more solidly):

* Expand the project tree to 'pelican/pelican[-plugins]/tests' tests in the
  left-side project/file navigation panel,

 * Right-click on this `tests` directory to bring up a pop-up context menu.

 * Select 'Mark directory as' menu option.

  * Select 'Test Sources Root' submenu option.
      This 'tests' folder is now green-colored.


Which Python Binary
===================
PyCharm is defaulted to using `/usr/bin/pelican`.  That may be okay if
not using a Python virtual environment.  Determine if the current
`$SHELL` session, providing this Python binary, is a virtual environment
or not by executing:

    python -c "import sys; print(sys.executable)"
    ls -l <insert-above-result-here>

If it is `/usr/bin/python`, and is NOT a symlink; skip this sub-section
on virtual environment.

You are highly likely using a virtual environment.

Execute this:

```bash
echo ${VIRTUAL_ENV}/bin/python
echo $__VENV_PYTHON
echo $CONDA_PREFIX
echo $PIPENV_PIPFILE
echo $POETRY_VIRTUALENVS_IN_PROJECT
echo $DIRENV_FILE
```

Exactly one Python binary path should appear.  If two or more
lines worth of Python binary appears, you cannot use
different tools of virtual environment together.

From the echo commands performed above, cut and paste the full
path specification that is pointing to the virtual Python binary.

Make that "virtual" Python binary the default inside this project:

* From the Main Menu Bar, select <u>`F`</u>`ile`, then `Settings`
  (or press Ctrl-Alt-S), then the dialog box titled `Settings` appear.

 * In left-side panel of `Settings` dialog, go down to `Project: ...` and
   click on it to expand for more choices.

 * Click on `Python Interpreter` option to see the right-side
   `Project: Pelican > Python Interpreter` panel showing many options.

  * Click on `Add Interpreter` next to the `Python Interpreter:` in
    the `Project: Pelican > Python Interpreter` panel.
    NOTE: This `Project: Pelican > Python Interpreter` is the primary step
          to adding additional virtual environment's worth of Python binary.

 * A drop-down menu box appears, select `Add Local Interpreter ...`.
      A popup dialog box titled `Add Python Interpreter` then appears.

     * The left-side panel of `Add Python Interpreter` dialog box,
       select `VirtualEnv Environment`.

      * Select `Existing` for `Environment`

      * Next to `Location`, at the end of the text box, click
        on the folder icon.

      * Paste in the pelican binary as reported by earlier `echo ...` test.
        (e.g., /home/user/virtualenvs/pelican/bin/python3)

Pytest Debugging
================
When establishing a JetBrain PyCharm session, `pytest` typically spawns
off 6 subprocesses. Let us reduce this to 1 subprocess (like in almost
sequential test):

* Go to "Run" menu option on Main Menu Toolbar, a drop-down menu
option list appears,

 * select "Edit Configurations...", and "Run/Debug Configuration" dialog box appears.

  * In lower left corner, click on "Edit Configuration Templates" hyperlink, and "Run/Debug Configuration Template" dialog box appears.

   * Click on "Python tests" in left panel of "Run/Debug Configuration Template" dialog box to expand more choices for a Python test file.

    * Click on "Pytest" menu option, then more options appear in the right panel.
     * In the 'Additional Arguments' textbox, enter in '-n0' for no multi-process debugging.  This gets passed to the `pytest` now for all pytests you create.


Virtual Environment
===================
If you want to add a virtual environment, TBD.

Debug Session
=============

Next is to set up a debug session using Pytest under PyCharm IDE.

Couple ways to setup the debug session within a Pelican pytest under PyCharm IDE:

1. by a Python test source file
2. from a new Run/Edit Configuration menu item


By a Source File
----------------

Two ways to start a debug session are:

1. With a new Python test source file
2. With an existing Python test source file


<h3>With A New Test Source File</h3>

To establish a first-time debug session in a brand new Python test file:

* In left-side project/file navigation panel, on the 'tests' subdirectory,
  right-click on it and a pop-up context menu appears.

 * Select `New` submenu option.  A new menu slideout appears.

  * Select `Python file` submenu option. A new dialog box that is
    titled `New Python file` appears.

   * Firstly, select the `Python unit test` option
     (if you started to type in the filename firstly, it will get
      harder to select that desired unit test option afterward after
      hitting the ENTER key).

    * Then go back and select that filename's text box
      and firstly type in `test_` then its desired filename.
      NOTE: If testing `b_parse.py`, type in `test_b_parse.py`

      NOTE: This is the only way for PyCharm to pre-fill this
            unit test source file with the good template.

Last step before debugging is to create the Run/Debug configuration.

The easiest way to create the Run/Debug configuration is to just
click on debug.  The many ways to start a debug session are:

* Ctrl-F9 (sometime the desktop's window manager stole that keymap,
  try the next one)
* Alt-Shift-F9
* Debug icon (green bug, next to `Run` green right triangle) on
  the Tool Window Bar (just below Main Menu Bar)
* On Main Menu Bar, `Run` then `Debug`
* Debug icon (Ctrl-5) is in the lower-left `Debug` panel to re-run a debug session
* Green outline triangle in the gutter column next to a source line on the source code panel

WARNING: Using Pythong virtual environment wrecks havoc on PyCharm.  PyCharm defaults
to `/usr/bin/python` which is often not virtualized.  Often times, the virtualized Python
(ie., `~/virtuanenv/pelican/bin/python` or `~/.venv/bin/pelican`) binary are preferred default.

By An Existing Test Source File
===============================
To establish a debug session in an opened source file:

* open a Python test file until the source file appears in the main viewing panel.

 * Locate the the gutter column (line numbers of source file)

  * Identify the line number of a Python code (not a comment nor blank line)
    to start debugging

   * click next to a line number to add a "red-dot" breakpoint

* In left-side project/file navigation panel, choose one of
  the `test_*` file to debug then right-click on it.
  A pop-up context menu appears.

 * On the popped up context menu, select `Debug pytest in test-*` menu
   option to create a new pytest run/debug configuration for
   this `test_*` unittest file.

* On main menu (upper) toolbar, select `Run`.  A menu slideout appears.
 * Select the `Edit Configuration` submenu option.
   A new dialog box that is titled `Edit Run/Debug Configurations` now appears.

  * In the left-side panel, expand the `Pytest` folder into a tree
    of previous run/debug sessions.
    NOTE: If the file is grayed-out, it means "I HAVEN'T BEEN SAVED YET".
          You will lose those when closing this project or exiting PyCharm.

  *
