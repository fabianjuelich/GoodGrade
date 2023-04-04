import customtkinter as ctk
import db
from enum import Enum, auto

class App(ctk.CTk):

    # menu
    class Mode(Enum):
        NEW = auto(),
        MOD = auto(),
        DEL = auto()

    def new(self):
        self.mode = self.Mode.NEW
        self.feedback.set('')
        self.moduleCombo.set('')
        self.moduleCombo.configure(state='normal')
        self.grade.set('')
        self.cp.set('')
        self.gradeEntry.configure(state='normal')
        self.cpEntry.configure(state='normal')
        self.cancelButton.configure(state='normal')
    
    def modify(self):
        self.mode = self.Mode.MOD
        self.okayBtnState(True)

    def delete(self):
        pass

    # enabling
    def entryState(self, enable: bool):
        self.moduleCombo.configure(state='normal' if enable else 'readonly')
        self.gradeEntry.configure(state='normal' if enable else 'disabled')
        self.cpEntry.configure(state='normal' if enable else 'disabled')

    def okayBtnState(self, enable: bool):
        self.okButton.configure(state='normal' if enable else 'disabled')

    def validateEntries(self, *args):
        if self.mode and self.module.get() and self.grade.get() and self.cp.get():
            self.okayBtnState(True)

    # output
    def clear(self):
        pass

    def showData(self, module):
        self.feedback.set('')
        row = db.select(module)
        self.grade.set(row[1])
        self.cp.set(row[2])

    def refreshList(self):
        self.moduleCombo.configure(values=[row[0] for row in db.select()])

    def refreshAvg(self):
        self.avg.set('⌀ ' + str(round(db.avg(), 2)))

    # confirmation
    def cancel(self):
        self.mode = None
        self.resetAll()

    def okay(self):
        match(self.mode):
            case self.Mode.NEW:
                try:
                    db.insert(self.module.get(), self.grade.get(), self.cp.get())
                    self.feedback.set(u'\uFF0B')
                except:
                    print('db: Inserting failed')
            case self.Mode.MOD:
                try:
                    self.feedback.set(u'\u25B2')
                except:
                    print('db: Updating failed')
            case self.Mode.DEL:
                try:
                    self.feedback.set(u'\uFF0D')
                except:
                    print('db: Deleting failed')
            case _:
                raise Exception()
        self.mode = None
        self.disableEntries()
        self.disableMenu()
        self.refreshList()
        self.refreshAvg()

    # reseting
    def prompts(self):
        self.grade.set('Grade')
        self.cp.set('CP')
        self.moduleCombo.set('Choose module')

    def disableEntries(self):
        self.entryState(False)
        self.cancelButton.configure(state='disabled')
        self.okButton.configure(state='disabled')

    def disableMenu(self):
        self.modButton.configure(state='disabled')
        self.delButton.configure(state='disabled')

    def resetAll(self):
        self.prompts()
        self.disableEntries()
        self.disableMenu()

    # initialization
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

        self.newButton = ctk.CTkButton(self.menuSection, text='New', width=self.x/(1/0.3), command=self.new)
        self.modButton = ctk.CTkButton(self.menuSection, text='Modify', width=self.x/(1/0.3), command=self.modify)
        self.delButton = ctk.CTkButton(self.menuSection, text='Delete', width=self.x/(1/0.3))

        self.feedback = ctk.StringVar(value='')
        self.feedbackLabel = ctk.CTkLabel(self.inoutFields, textvariable=self.feedback)
        self.module = ctk.StringVar()
        self.moduleCombo = ctk.CTkComboBox(self.inoutFields, width=self.y/1.1, values=[row[0] for row in db.select()], variable=self.module, command=self.showData)
        self.grade = ctk.StringVar()
        self.gradeEntry = ctk.CTkEntry(self.inoutFields, width=self.y/2.2, justify=ctk.RIGHT, placeholder_text='Grade', textvariable=self.grade)
        self.cp = ctk.StringVar()
        self.cpEntry = ctk.CTkEntry(self.inoutFields, width=self.y/2.2, justify=ctk.RIGHT, placeholder_text='CP', textvariable=self.cp)
        self.cancelButton= ctk.CTkButton(self.confirmFields, width=self.y/2.2, text='Cancel', command=self.cancel)
        self.okButton = ctk.CTkButton(self.confirmFields, width=self.y/2.2, text='OK', command=self.okay)
        self.avg = ctk.StringVar(value='⌀')
        self.avgLabel = ctk.CTkLabel(self.inoutSection, font=('TkCaptionFont', 20), textvariable=self.avg)

        self.printButton = ctk.CTkButton(self.printSection, text='Print')

        # packing
        self.frame.pack(expand='True')
        self.menuSection.pack()
        self.inoutSection.pack(pady=self.y/10)
        self.inoutFields.pack()
        self.confirmFields.pack()
        self.printSection.pack()

        self.newButton.pack(side=ctk.LEFT, padx=self.x/400)
        self.modButton.pack(side=ctk.LEFT, padx=self.x/400)
        self.delButton.pack(side=ctk.LEFT, padx=self.x/400)

        self.feedbackLabel.pack()
        self.moduleCombo.pack(pady=self.y/100)
        self.gradeEntry.pack(side=ctk.LEFT, padx=self.x/300)
        self.cpEntry.pack(side=ctk.LEFT, padx=self.x/300)
        self.cancelButton.pack(side=ctk.LEFT, padx=self.x/300, pady=self.y/100)
        self.okButton.pack(side=ctk.LEFT, padx=self.x/300, pady=self.y/100)
        self.avgLabel.pack(pady=self.y/20)

        self.printButton.pack()

        # current mode
        self.mode = None

        # initialize
        self.resetAll()
        try:
            self.refreshAvg()
        except:
            pass

        # tracing events
        self.module.trace('w', self.validateEntries)
        self.grade.trace('w', self.validateEntries)
        self.cp.trace('w', self.validateEntries)