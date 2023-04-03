import customtkinter as ctk
import grades

class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        # window configuration
        self.title('GoodGrades')
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('dark-blue')
        
        # dimensions
        self.x = 360
        self.y = 360
        self.geometry(f'{self.x}x{self.y}')

        # widgets
        self.frame = ctk.CTkFrame(self, fg_color='transparent')
        self.menuSection = ctk.CTkFrame(self.frame, fg_color='transparent')
        self.inoutSection = ctk.CTkFrame(self.frame, fg_color='transparent')
        self.inoutFields = ctk.CTkFrame(self.inoutSection, fg_color='transparent')
        self.confirmFields = ctk.CTkFrame(self.inoutSection, fg_color='transparent')
        self.printSection = ctk.CTkFrame(self.frame, fg_color='transparent')

        self.newButton = ctk.CTkButton(self.menuSection, text='New', width=self.x/(1/0.3))
        self.modButton = ctk.CTkButton(self.menuSection, text='Modify', width=self.x/(1/0.3))
        self.delButton = ctk.CTkButton(self.menuSection, text='Delete', width=self.x/(1/0.3))

        self.moduleCombo = ctk.CTkComboBox(self.inoutFields, width=self.y/1.1, values=[row[0] for row in grades.select()], command=self.setOutputs)
        self.grade = ctk.StringVar()
        self.gradeEntry = ctk.CTkEntry(self.inoutFields, width=self.y/2.2, placeholder_text='Grade', textvariable=self.grade)
        self.cp = ctk.StringVar()
        self.cpEntry = ctk.CTkEntry(self.inoutFields, width=self.y/2.2, placeholder_text='CP', textvariable=self.cp)
        self.cancelButton= ctk.CTkButton(self.confirmFields, width=self.y/2.2, text='Cancel')
        self.okButton = ctk.CTkButton(self.confirmFields, width=self.y/2.2, text='OK')# 
        self.avg = ctk.StringVar(value='⌀ ' + str(round(grades.avg(), 2)))
        self.avgLabel = ctk.CTkLabel(self.inoutSection, font=('TkCaptionFont', 20), textvariable=self.avg)

        self.printButton = ctk.CTkButton(self.printSection, text='Print')

        # packing
        self.frame.pack(expand='True')
        self.menuSection.pack()
        self.inoutSection.pack(pady=self.y/8)
        self.inoutFields.pack()
        self.confirmFields.pack()
        self.printSection.pack()

        self.newButton.pack(side=ctk.LEFT, padx=self.x/400)
        self.modButton.pack(side=ctk.LEFT, padx=self.x/400)
        self.delButton.pack(side=ctk.LEFT, padx=self.x/400)

        self.moduleCombo.pack(pady=self.y/100)
        self.gradeEntry.pack(side=ctk.LEFT, padx=self.x/300)
        self.cpEntry.pack(side=ctk.LEFT, padx=self.x/300)
        self.cancelButton.pack(side=ctk.LEFT, padx=self.x/300, pady=self.y/100)
        self.okButton.pack(side=ctk.LEFT, padx=self.x/300, pady=self.y/100)
        self.avgLabel.pack(pady=self.y/20)

        self.printButton.pack()

        # initialize
        self.modButton.configure(state='disabled')
        self.delButton.configure(state='disabled')
        self.grade.set('Grade')
        self.cp.set('CP')
        self.moduleCombo.set('Module')
        self.entryState(False)
        self.cancelButton.configure(state='disabled')
        self.okButton.configure(state='disabled')

    def entryState(self, enable: bool):
        self.moduleCombo.configure(state='normal' if enable else 'readonly')
        self.gradeEntry.configure(state='normal' if enable else 'disabled')
        self.cpEntry.configure(state='normal' if enable else 'disabled')

    def setOutputs(self, module):
        row = grades.select(module)
        self.grade.set(row[1])
        self.cp.set(row[2])
