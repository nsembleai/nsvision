import sys
from tkinter import Tk, ttk, filedialog, Label, Entry, messagebox, StringVar, BooleanVar
from threading import Thread
from nsvision.classifier import split_image_data
from pathlib import Path

class SplitDataGui(Tk):
    def __init__(self):
        super(SplitDataGui,self).__init__() #Initialize Tk constructor
        self.title("Split Data GUI") #set gui title
        self.minsize(900, 450) #set minimum size
        vcmd = (self.register(self.validate))
        
        #variable for setting and getting input from textbox 
        self.trainvar = StringVar()
        self.testvar = StringVar()
        self.valvar = StringVar()
        self.qavar = StringVar()
        self.error_message = StringVar()
        self.process_status = BooleanVar()
        
        #variable for storing source folder path, train, val, test and QA ration value
        self.qa = None
        self.val = None
        self.test = None
        self.train = None
        self.source_browse_path = None
        

        #defining source and destination containers along with processing container
        #for displaying browse button along with path after clicking on it
        self.selectorLabelFrame = ttk.LabelFrame(self, text = "Selector label frame").grid(column = 0, row = 0)
        
        self.sourceLabelFrame = ttk.LabelFrame(self , text = "Select Source Folder and set ratio")
        self.sourceLabelFrame.grid(column = 0, row = 0, padx = 10, pady = 50)
        
        self.ratioFrame = ttk.LabelFrame(self.sourceLabelFrame , text = "Select Ratio")
        self.ratioFrame.grid(column = 1, row = 0, padx = 1, pady = 50)
        
        self.progressLabelFrame = ttk.LabelFrame(self, text = "Main")
        self.progressLabelFrame.grid(column = 0 ,row = 1, padx = 30 , pady = 50)
        
        #Add a progress bar for displaying status
        self.progress_bar = ttk.Progressbar(self.progressLabelFrame, orient = 'horizontal', length = 600, mode = 'indeterminate')
        self.progress_bar.grid(column = 0 ,row = 0 , padx = 50 , pady = 50)

        #Adding buttons for browsing source ,destination and path reset
        self.source_button = ttk.Button(self.sourceLabelFrame, text = "Browse", command = self.source_browse)
        self.source_button.grid(column = 0 ,row = 0 , padx = 10, pady = 10)
        
        self.set_ratio_button = ttk.Button(self.sourceLabelFrame, text = "Set Ratio", command = self.set_ratio).grid(column=1,row = 1, pady=10)
        
        
        self.train_label = Label(self.ratioFrame, text = 'train').grid(column = 0, row = 0)
        self.val_label = Label(self.ratioFrame, text = 'val').grid(column = 2, row = 0)
        self.test_label = Label(self.ratioFrame, text = 'test').grid(column = 0, row = 1)
        self.qa_label = Label(self.ratioFrame, text = 'QA').grid(column = 2, row = 1)
        
        
        self.train_input_box = Entry(self.ratioFrame, state = 'normal', textvariable=self.trainvar, validate = 'all', validatecommand = (vcmd,'%P'))
        self.train_input_box.grid(column = 1, row = 0)
        
        self.val_input_box = Entry(self.ratioFrame, state = 'normal', textvariable=self.valvar, validate = 'all', validatecommand = (vcmd,'%P'))
        self.val_input_box.grid(column = 3, row = 0)
        
        self.test_input_box = Entry(self.ratioFrame, state = 'normal', textvariable=self.testvar, validate = 'all', validatecommand = (vcmd,'%P'))
        self.test_input_box.grid(column = 1, row = 1)
        
        self.qa_input_box = Entry(self.ratioFrame, state = 'normal',textvariable=self.qavar, validate = 'all', validatecommand = (vcmd,'%P'))
        self.qa_input_box.grid(column = 3, row = 1)
        
        self.reset_button = ttk.Button(self,text="Reset",command = self.reset)
        self.reset_button.grid(column = 1 , row = 0 , padx = 2, pady = 50)
        
        self.progress_button = ttk.Button(self,text = "Split Data", command = self.process)
        self.progress_button.grid(column = 1 , row = 1 , padx = 2, pady = 50)
        
        #label for displaying browse path for both source and destination
        self.source_path_label = Label(self.sourceLabelFrame, wraplength=150)
        self.source_path_label.grid(column = 0,row = 1)
                

    def source_browse(self):
        self.source_browse_path = Path(filedialog.askdirectory()) #using Path() to get absolute path for linux as well as windows    
        self.source_path_label.config(text = self.source_browse_path)


    def update_input_state(self,state = "normal"):
        self.train_input_box.config(state=state)
        self.test_input_box.config(state=state)
        self.val_input_box.config(state=state)
        self.qa_input_box.config(state=state)
        
        
    def set_ratio(self):
        self.train = int(self.trainvar.get()) if self.trainvar.get() else 0
        self.test = int(self.testvar.get()) if self.testvar.get() else 0
        self.val = int(self.valvar.get()) if self.valvar.get() else 0
        self.qa = int(self.qavar.get()) if self.qavar.get() else 0
        total = self.train + self.test + self.val + self.qa
        if total != 100:
            messagebox.showwarning("Please check your ratio", f"Total ratio must be 100 but your total ratio is {total}")
        else:
            self.update_input_state(state="readonly")        
        
    
    def clear_text(self):
        self.train_input_box.delete(0,"end")
        self.val_input_box.delete(0,"end")
        self.test_input_box.delete(0,"end")
        self.qa_input_box.delete(0,"end")
        
        
    def reset_string_var(self):
        self.trainvar.set('')
        self.testvar.set('')
        self.valvar.set('')
        self.qavar.set('')
        self.error_message.set('')
        
    
    def reset(self):
        self.source_browse_path = None
        self.process_status.set(False)
        self.source_path_label.config(text = '')
        self.progress_bar.config(value = 0)
        self.reset_string_var()
        self.update_input_state()
        self.clear_text()
        
    
    def validate(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False
        
    
    def split_data(self):
        try:
            split_image_data(self.source_browse_path,ratio=(self.train , self.val , self.test, self.qa))
            self.process_status.set(True)
        except Exception as e:
            self.error_message.set(str(e))
            self.process_status.set(False)
            
    
    def check_thread(self):
        if self.split_data_thread.is_alive():
            self.after(50, self.check_thread)
        else:
            self.progress_bar.stop()
            if self.process_status.get():
                messagebox.showinfo('Success',f'Split data completed successfully\nData is stored at {self.source_browse_path}_classified')
            else:
                messagebox.showerror('Fail',f'{self.error_message.get()}')

        
    def process(self):
        if self.source_browse_path is None or self.train_input_box['state'] == 'normal':
            messagebox.showwarning("Warning", "Please set input path and ratio before pressing 'Split Data'")
        else:
            self.progress_bar.start()
            self.split_data_thread = Thread(target = self.split_data)
            self.split_data_thread.start()
            self.after(50, self.check_thread)
                    
def main():
    split_data_gui = SplitDataGui()
    split_data_gui.mainloop()

if __name__ == '__main__':
    sys.exit(main())