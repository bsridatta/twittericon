import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib import style
import Tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt


LARGE_FONT = ("Verdana", 12)
style.use("ggplot")
# f = Figure(figsize=(5, 5), dpi=100)
# a = f.add_subplot(111)


fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

def animate(i):
    pullData = open("twitter-out.txt", "r").read()
    lines = pullData.split('\n')

    xar = []
    yar = []

    x = 0
    y = 0

    for l in lines[-200:]:
        x += 1
        if "pos" in l:
            y += 10
        elif "neg" in l:
            y -= 1

        xar.append(x)
        yar.append(y)

    ax1.clear()
    ax1.plot(xar, yar)

class senti(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Twitter'e'con")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        self.controller = controller

        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="The Senti Tool", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        self.emp = tk.Entry(self, bd=5, font=("Times New Roman", 14), width=25)
        self.emp.pack(side=tk.TOP)

        button3 = ttk.Button(self, text=" Get sentiment ",
                             command=lambda: self.go_to_page_one())
        button3.pack()


    def go_to_page_one(self):
        self.controller.inputString = self.emp.get()  # save text from entry to some var
        self.controller.frames[PageOne].correct_label()  # call correct_label function
        self.controller.frames[PageOne].streamLive()
        self.controller.frames[PageOne].plotLive()
        self.controller.show_frame(PageOne)  # show page one

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.label = tk.Label(self, text="plot", font=LARGE_FONT)
        self.label.pack(side=tk.TOP)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack(side=tk.TOP)

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


    #call twitterLive and pass streaminf input

    def correct_label(self):
        self.label.config(text=self.controller.inputString)  # correct the label

    def streamLive (self):
        twitterLive.stream(self.controller.inputString)

    def plotLive(self):
        import graphingMATLAB as grapher
        print "plotting"
        grapher.plotMe()


app = senti()
app.mainloop()
