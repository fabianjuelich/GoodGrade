import customtkinter as ctk
import tkinter as tk
import db
from enum import Enum, auto
import time
import threading
import pdf
from tktooltip import ToolTip

class App(ctk.CTk):

    # state
    def entryState(self, course, grade, factor: bool):
        self.courseCombo.configure(state='normal' if course else 'readonly')
        self.gradeEntry.configure(state='normal' if grade else 'disabled')
        self.factorEntry.configure(state='normal' if factor else 'disabled')

    def confirmState(self, cancel: bool, ok: bool):
        self.cancelButton.configure(state='normal' if cancel else 'disabled')
        self.okButton.configure(state='normal' if ok else 'disabled')

    def entryValid(self):
        grade = self.grade.get()
        factor = self.factor.get()
        valid = False
        try:
            grade = float(grade)
            if factor:
                factor = float(factor)
            valid = True
        except:
            pass
        if self.mode == self.Mode.ADD:
            return bool(self.mode), self.course.get() and valid
        elif self.mode == self.Mode.MOD:
            return bool(self.mode), self.course.get() and valid and (grade != self.tmpGrade or factor != self.tmpFactor)
        elif self.mode == self.Mode.DEL:
            return True, True
        else:
            return False, False

    def validateEntries(self, *_):
        self.confirmState(*self.entryValid())

    def menuState(self, add, modify, delete):
        self.addButton.configure(state='normal' if add else 'disabled')
        self.modButton.configure(state='normal' if modify else 'disabled')
        self.delButton.configure(state='normal' if delete else 'disabled')

    # menu
    class Mode(Enum):
        ADD = auto(),
        MOD = auto(),
        DEL = auto()

    def add(self):
        self.mode = self.Mode.ADD
        self.menuState(False, False, False)
        self.clearEntry()
        self.entryState(True, True, True)
        self.courseCombo.focus_set()
        self.cancelButton.configure(state='normal')
        self.feedback.set(self.emojis[self.Mode.ADD])

    tmpGrade = None
    tmpFactor = None
    def modify(self):
        self.mode = self.Mode.MOD
        self.tmpGrade = float(self.grade.get())
        self.tmpFactor = float(self.factor.get())
        self.menuState(False, False, False)
        self.entryState(False, True, True)
        self.courseCombo.configure(state='disabled')
        self.gradeEntry.focus_set()
        self.cancelButton.configure(state='normal')
        self.feedback.set(self.emojis[self.Mode.MOD])

    def delete(self):
        self.mode = self.Mode.DEL
        self.menuState(False, False, False)
        self.feedback.set(self.emojis[self.Mode.DEL])
        self.entryState(False, False, False)
        self.courseCombo.configure(state='disabled')
        self.confirmState(True, True)

    # output
    emojis = {None: '', Mode.ADD: u'\uFF0B', Mode.MOD: u'\u25B2', Mode.DEL: u'\uFF0D', 'avg': u'\u2300', 'chkmark': u'\u2713', 'err': u'\u2715', 'printer': u'\u2399'}

    def clearEntry(self):
        self.course.set('')
        self.grade.set('')
        self.factor.set('')

    def showGrade(self, course):
        row = db.select(course)
        self.grade.set(row[1])
        self.factor.set(row[2])
        if self.mode == None:
            self.menuState(True, True, True)

    def refreshList(self):
        self.courseCombo.configure(values=[row[0] for row in db.select()])

    def refreshAvg(self):
        try:
            avg = db.avg()
        except:
            pass
        self.avg.set(self.emojis['avg'] + (f' {str(round(avg, 2))}' if avg else ''))

    def refresh(self):
        self.refreshList()
        self.refreshAvg()

    def pdf(self):
        pdf.print2pdf()
        self.setFeedback(self.emojis['printer'], 1)

    # resetting
    def rstFeedback(self):
        self.feedback.set('')

    def disableEntry(self):
        self.entryState(False, False, False)
        self.confirmState(False, False)

    def rstAll(self):
        self.menuState(True, False, False)
        self.disableEntry()

    # confirmation
    def cancel(self, *_):
        if self.mode:
            self.mode = None
            self.rstFeedback()
            self.rstAll()
            self.clearEntry()

    def setFeedbackBg(self, feedback, t, afterwards):
        self.feedback.set(feedback)
        if t:
            time.sleep(t)
            self.feedback.set(afterwards if afterwards else '')

    def setFeedback(self, feedback, t=0, afterwards=None):
        errorThread = threading.Thread(target=self.setFeedbackBg, args=[feedback, t, afterwards])
        errorThread.start()

    def ok(self, *_):
        # valid = self.entryValid()
        if not all(self.entryValid()):# valid[0] and not valid[1]:
            return
        match(self.mode):
            case self.Mode.ADD:
                try:
                    db.insert(self.course.get(), self.grade.get(), self.factor.get() if self.factor.get() else 1)
                    self.clearEntry()
                    self.courseCombo.focus_set()
                    self.refresh()
                    self.setFeedback(self.emojis['chkmark'], 1, self.emojis[self.mode])
                except:
                    self.setFeedback(self.emojis['err'], 1, self.emojis[self.mode])
                    return
            case self.Mode.MOD:
                try:
                    db.modify(self.grade.get(), self.factor.get(), self.course.get())
                    self.disableEntry()
                    self.menuState(True, True, True)
                    self.refresh()
                    self.mode = None
                    self.setFeedback(self.emojis['chkmark'], 1)
                except:
                    self.setFeedback(self.emojis['err'], 1, self.emojis[self.mode])
                    return
            case self.Mode.DEL:
                try:
                    db.delete(self.course.get())
                    self.clearEntry()
                    self.refresh()
                    self.mode = None
                    self.rstAll()
                    self.setFeedback(self.emojis['chkmark'], 1)
                except:
                    self.setFeedback(self.emojis['err'], 1, self.emojis[self.mode])
                    return
            case _:
                pass

    # initialization
    def __init__(self):
        super().__init__()

        # window configuration
        self.title('GoodGrade')
        self.icon = tk.PhotoImage(file = "Assets/icons8-grades-100.png")
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
        self.gradeSection = ctk.CTkFrame(self.inoutFields, width=self.x/2)
        self.factorSection = ctk.CTkFrame(self.inoutFields, width=self.x/2)
        self.confirmFields = ctk.CTkFrame(self.inoutSection, fg_color='transparent')
        self.printSection = ctk.CTkFrame(self.frame, fg_color='transparent')

        self.addButton = ctk.CTkButton(self.menuSection, text='Add', width=self.x/3.4, command=self.add)
        self.modButton = ctk.CTkButton(self.menuSection, text='Modify', width=self.x/3.4, command=self.modify)
        self.delButton = ctk.CTkButton(self.menuSection, text='Delete', width=self.x/3.4, command=self.delete)

        self.feedback = ctk.StringVar(value='')
        self.feedbackLabel = ctk.CTkLabel(self.inoutFields, font=('TkCaptionFont', 20), textvariable=self.feedback)
        self.course = ctk.StringVar()
        self.courseCombo = ctk.CTkComboBox(self.inoutFields, width=self.x/1.1, values=[row[0] for row in db.select()], variable=self.course, command=self.showGrade)
        self.grade = ctk.StringVar()
        self.gradeEntry = ctk.CTkEntry(self.gradeSection, width=self.x/2.2, justify=ctk.RIGHT, placeholder_text='Grade', textvariable=self.grade)
        self.factor = ctk.StringVar()
        self.factorEntry = ctk.CTkEntry(self.factorSection, width=self.x/2.2, justify=ctk.RIGHT, placeholder_text='factor', textvariable=self.factor)
        self.inclFactor = ctk.StringVar(value='yes')
        self.factorCheck = ctk.CTkCheckBox(self.factorSection, width=self.x/20, height=self.x/20, variable=self.inclFactor, onvalue="yes", offvalue='no', text=None)
        self.cancelButton= ctk.CTkButton(self.confirmFields, width=self.x/2.2, text='Cancel', command=self.cancel)
        self.okButton = ctk.CTkButton(self.confirmFields, width=self.x/2.2, text='OK', command=self.ok)
        self.avg = ctk.StringVar(value='⌀')
        self.avgLabel = ctk.CTkLabel(self.inoutSection, font=('TkCaptionFont', 20), textvariable=self.avg)

        self.printButton = ctk.CTkButton(self.printSection, width=self.x/4, text='Print', command=self.pdf)

        # packing
        self.frame.pack(expand='True')
        self.menuSection.pack()
        self.inoutSection.pack(pady=self.y/10)
        self.inoutFields.pack()
        self.confirmFields.pack()
        self.printSection.pack()

        self.addButton.pack(side=ctk.LEFT, padx=self.x/200)
        self.modButton.pack(side=ctk.LEFT, padx=self.x/200)
        self.delButton.pack(side=ctk.LEFT, padx=self.x/200)

        self.feedbackLabel.pack()
        self.courseCombo.pack(pady=self.y/100)
        self.gradeSection.pack(side=ctk.LEFT, expand=False, fill=None)
        self.gradeEntry.pack(padx=self.x/300)
        self.factorSection.pack(side=ctk.RIGHT, expand=False, fill=None)
        #self.factorCheck.pack(side=ctk.RIGHT, padx=self.x/300)
        self.factorEntry.pack(side=ctk.RIGHT, padx=self.x/300)
        self.cancelButton.pack(side=ctk.LEFT, padx=self.x/300, pady=self.y/100)
        self.okButton.pack(side=ctk.LEFT, padx=self.x/300, pady=self.y/100)
        self.avgLabel.pack(pady=self.y/20)

        self.printButton.pack()

        # initialize
        self.rstAll()
        self.refreshAvg()
        # current mode
        self.mode = None

        # tracing events
        self.course.trace('w', self.validateEntries)
        self.grade.trace('w', self.validateEntries)
        self.factor.trace('w', self.validateEntries)

        # key listener
        self.bind('<Escape>', self.cancel)
        self.bind('<Return>', self.ok)

        # tooltips
        ToolTip(self.courseCombo, msg='Course/Module/Lecture/Seminar', delay=0.5, bg='#1c1c1c', fg='#ffffff', )
        ToolTip(self.gradeEntry, msg='Grade', delay=0.5, bg='#1c1c1c', fg='#ffffff')
        ToolTip(self.factorEntry, msg='Factor (ECTS/CreditUnits)', delay=0.5, bg='#1c1c1c', fg='#ffffff')
