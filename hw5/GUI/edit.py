from Tkinter import *
from tkFileDialog import askopenfilename
import tkMessageBox

class Application(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        self.grid()
        self.create_widgets()
        self.memo2 = {}
        self.trace = {}
        self.all_result = ""

    def edit_Dist(self,x,y,memo=None):
        if memo is None: memo = {}
        if len(x) == 0: return len(y)
        if len(y) == 0: return len(x)
        if (len(x), len(y)) in memo:
            return memo[(len(x), len(y))]
        delt = int(self.csub.get()) if x[-1] != y[-1] else 0
        diag = self.edit_Dist(x[:-1], y[:-1], memo) + delt
        vert = self.edit_Dist(x[:-1], y, memo) + int(self.cdel.get())
        horz = self.edit_Dist(x, y[:-1], memo) + int(self.cins.get())
        ans = min(diag, vert, horz)
        memo[(len(x), len(y))] = ans
        self.memo2[(len(x), len(y))] = ans
        if ans == diag:
            self.trace[(len(x), len(y))] = '\\'
        elif ans == vert:
            self.trace[(len(x), len(y))] = '|'
        elif ans == horz:
            self.trace[(len(x), len(y))] = '-'

        return ans

    def compare(self):
        s = str(self.string_s.get())
        t = str(self.string_t.get())

        #check the inpur strings
        if s == "" or t == "" :
            tkMessageBox.showerror("error:","input error !")
            exit()

        d = self.edit_Dist(s,t)
        self.dist.set(d)

        #initialize trace matrix
        self.trace[(0,0)] = 0
        self.trace[(-1,-1)] = ' '
        self.trace[(-1,0)] = ' '
        self.trace[(0,-1)] = ' '
        for i in range(1,len(t) + 1):
            self.trace[(0,i)] = '-'
            self.trace[(-1,i)]= t[i-1]

        for i in range(1,len(s) + 1):
            self.trace[(i,0)] = '|'
            self.trace[(i,-1)] = s[i-1]

        #initialize edit distance matrix
        self.memo2[(0,0)] = 0
        self.memo2[(-1,-1)] = ' '
        self.memo2[(-1,0)] = ' '
        self.memo2[(0,-1)] = ' '
        for i in range(1,len(t) + 1):
            self.memo2[(0,i)] = i
            self.memo2[(-1,i)] = t[i-1]
        for i in range(1,len(s) + 1):
            self.memo2[(i,0)] = i
            self.memo2[(i,-1)] = s[i-1]

        #get the alignment
        i = len(s)
        j = len(t)
        ss = ""
        tt = ""
        symbol = ""
        while self.trace[(i,j)] != 0:
            if self.trace[(i,j)] == '\\':
                if s[i-1] == t[j-1]:
                    symbol += "|"
                    ss += s[i-1]
                    tt += t[j-1]
                else:
                    symbol += " "
                    ss += s[i-1]
                    tt += t[j-1]
                i -= 1
                j -= 1

            elif self.trace[(i,j)] == '|':
                symbol += " "
                ss += s[i-1]
                tt += "-"
                i -= 1

            elif self.trace[(i,j)] == '-':
                symbol += " "
                ss += "-"
                tt += t[j-1]
                j -= 1

        ss = ss[::-1]
        tt = tt[::-1]
        symbol = symbol[::-1]

        r1 = ""
        r2 = ""
        r3 = ""
        for i in range(0,len(ss) ):
            r1 += ss[i] + '\t'
            r2 += symbol[i] + '\t'
            r3+= tt[i] + '\t'


        #print results
        if self.is_edit.get():
            self.all_result += "full distance matrix :\n"
            for i in range(-1,len(s)+1):
                for j in range(-1,len(t)+1):
                    if ((i,j))in self.memo2:
                      self.all_result += str(self.memo2[(i,j)]) + "\t"
                self.all_result += "\n"

            self.all_result += "\n"

        if self.is_back.get():
            self.all_result += "backtrack matrix: \n"

            for i in range(-1,len(s)+1):
                for j in range(-1,len(t)+1):
                    self.all_result +=  str(self.trace[(i,j)]) + "\t"
                self.all_result +=  "\n"

            self.all_result += "\n"

        if self.is_alignment.get():
            self.all_result += "alignment: \n"
            self.all_result += r1 + "\n" + r2 + "\n" + r3 + "\n"

        self.all_result += "end-------------------------------------------------------\n"
        self.dist_matrix.delete(0.0, END)
        self.dist_matrix.insert(0.0, self.all_result)


    #read the strings from the files
    def load_file_s(self):
            fname = askopenfilename()
            file = open(fname)
            s_s = file.readline()
            s_s = s_s[:-1]
            file.close()
            self.string_s.delete(0,END)
            self.string_s.insert(0,s_s)

    def load_file_t(self):
            fname = askopenfilename()
            file = open(fname)
            s_t = file.readline()
            s_t = s_t[:-1]
            file.close()
            self.string_t.delete(0,END)
            self.string_t.insert(0,s_t)

    def create_widgets(self):
        #input string S
        Label(self,
              text="string from:"
              ).grid(row = 0,column = 0, sticky = W)

        self.string_s = Entry(self)
        self.string_s.grid(row = 0, column = 1, sticky = W)

        #input string T
        Label(self,
              text="string to:"
              ).grid(row = 1,column = 0, sticky = W)

        self.string_t = Entry(self)
        self.string_t.grid(row = 1, column = 1, sticky = W)


        #choose from file
        Button(self,
               text = "select from file:",
               command = self.load_file_s
               ).grid(row = 0, column = 2,sticky = W)

        Button(self,
               text = "select from file:",
               command = self.load_file_t
               ).grid(row = 1, column = 2,sticky = W)

        #result
        self.result = Label(self,
              text = "edit distance:"
        ).grid(row = 2, column = 0, sticky = W)

        self.dist = IntVar()
        self.distance = Label(self,
              textvariable = self.dist
        ).grid(row = 2, column = 1, sticky = W)
        self.dist.set(0)


        #input cdel
        Label(self,
              text="cdel (cost of deletion):"
              ).grid(row = 3,column = 0,columnspan = 1, sticky = W)
        self.cdel = Scale(self,
                          from_= 1,
                          to = 10,
                          orient = HORIZONTAL
                          )
        self.cdel.grid(row = 3, column = 1,columnspan = 1, sticky = W)


        #input cins
        Label(self,
              text="cins (cost for insertion):"
              ).grid(row = 4,column = 0,columnspan = 1, sticky = W)
        self.cins = Scale(self,
                          from_= 1,
                          to = 10,
                          orient = HORIZONTAL
                          )
        self.cins.grid(row = 4, column = 1,columnspan = 1,  sticky = W)

        #input csub
        Label(self,
              text="csub (cost for substitution):"
              ).grid(row = 5,column = 0,columnspan = 1, sticky = W)
        self.csub = Scale(self,
                          from_= 1,
                          to = 10,
                          orient = HORIZONTAL
                          )
        self.csub.grid(row = 5, column = 1,columnspan = 1, sticky = W)


        #preference choice-----------------------------------------------------------------------
        Label(self,
              text = "preference:"
              ).grid(row =8, column = 0, sticky = W)

        #create edit distance matrix check button
        self.is_edit = BooleanVar()
        Checkbutton(self,
                    text = "edit distance matrix",
                    variable = self.is_edit
                    ).grid(row = 8,column = 1,sticky = W)

        #create backtrace matrix check button
        self.is_back = BooleanVar()
        Checkbutton(self,
                    text = "backtrace matrix",
                    variable = self.is_back
                    ).grid(row = 8,column = 2,sticky = W)

        #create alignment check button
        self.is_alignment = BooleanVar()
        Checkbutton(self,
                    text = "alignment",
                    variable = self.is_alignment
                    ).grid(row = 8,column = 3,sticky = W)

        #compare button: begin to compute the edit distance
        Button(self,
               text = "compare",
               command = self.compare
               ).grid(row = 9, column = 0,sticky = W)

        #result summarization---------------------------------------------------------------
        scrollbar = Scrollbar(self)
        scrollbar2 = Scrollbar(self)
        Label(self,
              text="Results:"
              ).grid(row = 10,column = 0, sticky = W)
        self.dist_matrix = Text(self, width = 90, height = 20,yscrollcommand=scrollbar.set,xscrollcommand = scrollbar2.set)
        self.dist_matrix.grid(row = 11, column = 0, columnspan = 8)

        scrollbar.config(command=self.dist_matrix.yview)
        scrollbar.grid(row=11, column=8, sticky='ns')

        scrollbar2.config(command=self.dist_matrix.xview,orient = HORIZONTAL)
        scrollbar2.grid(row=14, column=0,columnspan = 8, sticky='we')


#main
root = Tk()
root.title("Edit Distance")
app = Application(root)
root.mainloop()