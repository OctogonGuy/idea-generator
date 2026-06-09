# Idea Generator

Given some topics, this program generates some sentences using those topics for the purpose of brainstorming ideas. It utilizes Tkinter for the GUI component.

## Setup

Complete the following steps to be able to run this program:

1. Install Python
   - Ubuntu / Debian
       ```
       sudo apt install python3
       ```
   - Fedora / RHEL
       ```
       sudo dnf install python3
       ```
2. Install Tkinter
   - Ubuntu / Debian
       ```
       sudo apt install python3-tk
       ```
   - Fedora / RHEL
       ```
       sudo dnf install python3-tkinter
       ```
3. Create a virtual environment
    ```
    python3 -m venv .venv
    ```

## Usage

To run the program, perform the following commands:

```
source .venv/bin/activate
python3 ./idea_gui.py
deactivate
```

Replace `idea_gui.py` with `idea.py` if you would like to use this program in the command line rather than in a GUI.
