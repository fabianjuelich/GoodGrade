import customtkinter as ctk
import tkinter as tk
import db
from enum import Enum, auto
import time
import threading

class App(ctk.CTk):

    # state
    def entryState(self, module, grade, cp: bool):
        self.moduleCombo.configure(state='normal' if module else 'readonly')
        self.gradeEntry.configure(state='normal' if grade else 'disabled')
        self.cpEntry.configure(state='normal' if cp else 'disabled')

    def confirmState(self, cancel: bool, ok: bool):
        self.cancelButton.configure(state='normal' if cancel else 'disabled')
        self.okButton.configure(state='normal' if ok else 'disabled')

    def entriesValid(self):
        return True if self.mode else False, self.mode and self.module.get() and self.grade.get() and self.cp.get()

    def validateEntries(self, *_):
        self.confirmState(*self.entriesValid())

    def menuState(self, new, modify, delete):
        self.newButton.configure(state='normal' if new else 'disabled')
        self.modButton.configure(state='normal' if modify else 'disabled')
        self.delButton.configure(state='normal' if delete else 'disabled')

    # menu
    class Mode(Enum):
        NEW = auto(),
        MOD = auto(),
        DEL = auto()

    def new(self):
        self.mode = self.Mode.NEW
        self.menuState(False, False, False)
        self.clearEntry()
        self.entryState(True, True, True)
        self.moduleCombo.focus_set()
        self.cancelButton.configure(state='normal')
        self.feedback.set(self.emojis[self.Mode.NEW])

    def modify(self):
        self.mode = self.Mode.MOD
        self.menuState(False, False, False)
        self.entryState(False, True, True)
        self.moduleCombo.configure(state='disabled')
        self.gradeEntry.focus_set()
        self.cancelButton.configure(state='normal')
        self.feedback.set(self.emojis[self.Mode.MOD])

    def delete(self):
        self.mode = self.Mode.DEL
        self.menuState(False, False, False)
        self.feedback.set(self.emojis[self.Mode.DEL])
        self.entryState(False, False, False)
        self.moduleCombo.configure(state='disabled')
        self.confirmState(True, True)

    # output
    emojis = {None: '', Mode.NEW: u'\uFF0B', Mode.MOD: u'\u25B2', Mode.DEL: u'\uFF0D', 'avg': u'\u2300', 'chkmark': u'\u2713', 'err': u'\u2715'}

    def clearEntry(self):
        self.module.set('')
        self.grade.set('')
        self.cp.set('')

    def showGrade(self, module):
        row = db.select(module)
        self.grade.set(row[1])
        self.cp.set(row[2])
        if self.mode == None:
            self.menuState(True, True, True)

    def refreshList(self):
        self.moduleCombo.configure(values=[row[0] for row in db.select()])

    def refreshAvg(self):
        try:
            avg = db.avg()
        except:
            pass
        self.avg.set(self.emojis['avg'] + (f' {str(round(avg, 2))}' if avg else ''))

    def refresh(self):
        self.refreshList()
        self.refreshAvg()

    # resetting
    def rstFeedback(self):
        self.feedback.set('')

    def prompts(self):
        self.grade.set('Grade')
        self.cp.set('CP')
        self.moduleCombo.set('Module')

    def disableEntry(self):
        self.entryState(False, False, False)
        self.confirmState(False, False)

    def rstAll(self):
        self.menuState(True, False, False)
        self.disableEntry()

    # confirmation
    def cancel(self):
        self.mode = None
        self.rstFeedback()
        self.rstAll()
        self.clearEntry()

    def setFeedbackBg(self, feedback, afterwards):
        self.feedback.set(feedback)
        time.sleep(1)
        self.feedback.set(afterwards if afterwards else '')

    def setFeedback(self, feedback, afterwards=None):
        errorThread = threading.Thread(target=self.setFeedbackBg, args=[feedback, afterwards])
        errorThread.start()

    def ok(self, *_):
        valid = self.entriesValid()
        if valid[0] and not valid[1]:
            self.setFeedback(self.emojis['err'], self.emojis[self.mode])
            return
        match(self.mode):
            case self.Mode.NEW:
                try:
                    db.insert(self.module.get(), self.grade.get(), self.cp.get())
                    self.clearEntry()
                    self.moduleCombo.focus_set()
                    self.refresh()
                    self.setFeedback(self.emojis['chkmark'], self.emojis[self.mode])
                except:
                    self.setFeedback(self.emojis['err'], self.emojis[self.mode])
                    return
            case self.Mode.MOD:
                try:
                    db.modify(self.grade.get(), self.cp.get(), self.module.get())
                    self.disableEntry()
                    self.menuState(True, True, True)
                    self.refresh()
                    self.mode = None
                    self.setFeedback(self.emojis['chkmark'])
                except:
                    self.setFeedback(self.emojis['err'], self.emojis[self.mode])
                    return
            case self.Mode.DEL:
                try:
                    db.delete(self.module.get())
                    self.clearEntry()
                    self.refresh()
                    self.mode = None
                    self.rstAll()
                    self.setFeedback(self.emojis['chkmark'])
                except:
                    self.setFeedback(self.emojis['err'], self.emojis[self.mode])
                    return
            case _:
                pass

    # initialization
    def __init__(self):
        super().__init__()

        # window configuration
        self.title('GoodGrade')
        self.icon = tk.PhotoImage(file = "icons8-grades-100.png")
        self.iconphoto(False, self.icon)
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
        self.delButton = ctk.CTkButton(self.menuSection, text='Delete', width=self.x/(1/0.3), command=self.delete)

        self.feedback = ctk.StringVar(value='')
        self.feedbackLabel = ctk.CTkLabel(self.inoutFields, font=('TkCaptionFont', 20), textvariable=self.feedback)
        self.module = ctk.StringVar()
        self.moduleCombo = ctk.CTkComboBox(self.inoutFields, width=self.y/1.1, values=[row[0] for row in db.select()], variable=self.module, command=self.showGrade)
        self.grade = ctk.StringVar()
        self.gradeEntry = ctk.CTkEntry(self.inoutFields, width=self.y/2.2, justify=ctk.RIGHT, placeholder_text='Grade', textvariable=self.grade)
        self.cp = ctk.StringVar()
        self.cpEntry = ctk.CTkEntry(self.inoutFields, width=self.y/2.2, justify=ctk.RIGHT, placeholder_text='CP', textvariable=self.cp)
        self.cancelButton= ctk.CTkButton(self.confirmFields, width=self.y/2.2, text='Cancel', command=self.cancel)
        self.okButton = ctk.CTkButton(self.confirmFields, width=self.y/2.2, text='OK', command=self.ok)
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

        # initialize
        self.rstAll()
        self.prompts()
        self.refreshAvg()
        # current mode
        self.mode = None

        # tracing events
        self.module.trace('w', self.validateEntries)
        self.grade.trace('w', self.validateEntries)
        self.cp.trace('w', self.validateEntries)

        # key listener
        self.bind('<Return>', self.ok)
