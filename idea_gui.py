"""
Program: idea_gui.py
Author: Alex Gill
Displays a graphical user interface for the idea generator program.
"""
from tkinter import *
from tkinter import messagebox
import idea


WIDTH = 600     # Width of the window
HEIGHT = 400    # Height of the window
BG = '#cbdbf5'  # Background color
PADX = 20       # Horizontal padding around the idea view
PADY = 10       # Vertical padding around the idea view
icon_path = "resources\\images\\icon.png"
octogon_image_path = "resources\\images\\octogon.png"


def main():
    # Create the window
    app = app_window()

    # Display the window
    app.mainloop()


class app_window(Tk):
    """Class for the root or app window"""

    def __init__(self):
        # Create the window
        Tk.__init__(self)
        self.title("Idea Generator")
        self.geometry(str(WIDTH) + "x" + str(HEIGHT))
        self.config(background='#cbdbf5')

        # Create an icon for the window
        icon = PhotoImage(file=icon_path)
        self.iconphoto(True, icon)

        # Set the prompt view
        self.frame = prompt_view(self)
        self.frame.pack(expand=True, fill=BOTH)


    def switch_frame(self, frame_class, *args):
        """Switches to the given frame."""
        self.frame.pack_forget()
        self.frame = frame_class(self, *args)
        self.frame.pack(expand=True, fill=BOTH)



class prompt_view(Frame):
    """Class for the prompt page"""

    def __init__(self, window):
        # Create the frame
        Frame.__init__(self, window, background=BG)

        # Create an image for decoration
        self.photo = PhotoImage(file=octogon_image_path, )    # global so not garbage collected
        image_label = Label(self,
                            image=self.photo,
                            background=BG)
        image_label.grid(row=0, column=0)

        # Create a prompt for entering subject
        prompt_label = Label(self,
                             text="What topic(s) would you like to generate ideas for?",
                             font=('Calibri', 13),
                             background=BG)
        prompt_label.grid(row=1, column=0)

        # Create an entry to enter subject
        self.subject_entry = Entry(self,
                              font = ('Calibri', 13),
                              width=39)
        self.subject_entry.grid(row=2, column=0)
        # Create prompt text that disappears when focused
        self.entry_text = "Enter one or more subjects separate by commas"
        self.subject_entry.insert(0, self.entry_text)
        self.subject_entry['foreground'] = 'gray'
        self.subject_entry.bind("<FocusIn>", self.on_focusin)
        self.subject_entry.bind("<FocusOut>", self.on_focusout)
        # Allow the user to press enter button to submit
        self.subject_entry.bind('<Return>', lambda e:self.submit(self.subject_entry.get()))

        # Create submit button
        submit_button = Button(self,
                               text="Submit",
                               font=('Algerian', 15),
                               foreground='white',
                               background='indigo',
                               activeforeground='white',
                               activebackground='indigo',
                               borderwidth=5,
                               command=lambda:self.submit(self.subject_entry.get()))
        submit_button.grid(row=3, column=0)

        # Configure grid properties
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=16)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=4)


    def submit(self, subjects_text):
        """Accepts the subjects and proceeds to the idea titles screen."""
        # Make sure the text box has some text
        if subjects_text.strip() == '' or subjects_text == self.entry_text:
            messagebox.showwarning(title='Warning', message='Please enter at least one subject.')
            return
        
        # Create the set of subjects
        subjects = idea.setOfSubjects(subjects_text)

        # Proceed to the idea screen
        self.master.switch_frame(idea_view, subjects)

    
    def on_focusin(self, event):
        """Occurs when the entry is focused in on"""
        if self.subject_entry.get() == self.entry_text:
            self.subject_entry.delete(0, END)
            self.subject_entry['foreground'] = 'black'


    def on_focusout(self, event):
        """Occurse when the entry is focused out"""
        if self.subject_entry.get() == '':
            self.subject_entry['foreground'] = 'gray'
            self.subject_entry.insert(0, self.entry_text)



class idea_view(Frame):
    """Class for the ideas page"""

    def __init__(self, window, subjects):
        # Initialize some member variables
        self.subjects = subjects
        self.ideas = [idea.generateTitle(subjects)]
        self.cur_page = 1
        self.far_page = 0

        # Create the frame
        Frame.__init__(self,
                       background=BG,
                       padx=PADX,
                       pady=PADY)
        self.bind('<Configure>', self.resize)

        # Create a button to go back to the prompt screen
        self.back_button = Button(self,
                                  text="Back",
                                  font=('Latin', 14),
                                  background='#ffff66',
                                  activebackground='#ffff66',
                                  command=self.back)
        self.back_button.grid(row=0, column=0, sticky=NW)

        # Create a label fore the idea
        self.idea_label = Label(self,
                                text=self.ideas[0],
                                font=('Georgia Bold', 13),
                                wraplength=WIDTH,
                                background=BG)
        self.idea_label.grid(row=1, column=0, columnspan=3)
        
        # Create the previous button
        self.prev_button = Button(self,
                                  text="Previous",
                                  font=('Latin', 14),
                                  background='#66ccff',
                                  activebackground='#66ccff',
                                  disabledforeground='#0077b3',
                                  state=DISABLED,
                                  command=self.prev)
        self.prev_button.grid(row=2, column=0, sticky=SW)

        # Create the page number label
        self.page_num_label = Label(self,
                                    text=self.cur_page,
                                    font=('Georgia Bold', 13),
                                    background=BG)
        self.page_num_label.grid(row=2, column=1)

        # Create the next button
        self.next_button = Button(self,
                                  text="Next",
                                  font=('Latin', 14),
                                  background='#ff6666',
                                  activebackground='#ff6666',
                                  command=self.next)
        self.next_button.grid(row=2, column=2, sticky=SE)

        # Configure grid properties
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        
    def next(self):
        """Moves to the next page"""
        if self.cur_page == 1:
            self.prev_button['state'] = ACTIVE
        self.cur_page += 1
        if self.cur_page > self.far_page:
            self.far_page = self.cur_page
            self.ideas.append(idea.generateTitle(self.subjects))
        self.idea_label['text'] = self.ideas[self.cur_page-1]
        self.page_num_label['text'] = self.cur_page

    
    def prev(self):
        """Moves to the previous page"""
        if self.cur_page > 1:
            self.cur_page -= 1
            self.idea_label['text'] = self.ideas[self.cur_page-1]
            self.page_num_label['text'] = self.cur_page
            if self.cur_page == 1:
                self.prev_button['state'] = DISABLED

    
    def back(self):
        """Goes back to the prompt view"""
        self.master.switch_frame(prompt_view)


    def resize(self, event):
        """Defines what happens when the window is resized"""
        self.idea_label['wraplength'] = event.width - PADX * 2



if __name__ == '__main__':
    main()