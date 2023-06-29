
from main import *
from graphs import * 
from tkinter.messagebox import askyesno
from babel import numbers
from tkcalendar import Calendar
from datetime import datetime
  
#on pressing 'add expense Button':
def addExpense(userid):
    def add_database():
        # convert to sql date format
        date = datetime.strptime(cal.get_date(), "%m/%d/%y").strftime("%Y-%m-%d")
        amt= amt_entry.get()
        cat = cat_text.get()
        mop = mop_text.get()
        note = note_entry.get()
        
        current_month = datetime.now().month
        if(current_month < 10): #save jan as 01 not 1 (for ex.)
            current_month = '0' + str(current_month)
        
        
        #retrieve data for the current month
        cur.execute("SELECT SUM(AMOUNT) FROM expenses WHERE strftime('%m', DATE) = ? and userid = ? and CATEGORY = ?", (current_month,userid,cat))
        try:
            sum_ = float(cur.fetchone()[0])
        except:
            sum_ = 0.0
        cur.execute("SELECT AMOUNT FROM budget WHERE CATEGORY = ? and userid = ?", (cat,userid))
        temp = cur.fetchone()
        print("test")
        if(temp):    
            print("test")

            budget = float(temp[0])
            print("budget",budget)
            print("sum", sum_)
            print("amt",amt)
            #print(budget, sum_)
            if(sum_ + float(amt) > budget):
                answer = askyesno(title='Alert', message='You are exceeding your budget. Are you sure that you want to proceed?')
                if answer == False:
                    #addexp_window.destroy()
                    return
                #messagebox.showwarning("Alert", "You are exceeding your budget!")
        
        exp_query = '''INSERT INTO expenses(USERID, DATE, AMOUNT, CATEGORY, MOP, NOTE)
        VALUES(?,?,?,?,?,?)'''
        exp_tuple = (userid, date, amt, cat, mop, note)
        cur.execute(exp_query, exp_tuple)          
        conn.commit()

        row = cur.fetchone()      

        if(row!=[] and cat and mop and str(amt_entry.get()).isdigit()):
            l5 = Label(addexp_window, text="Added Successfully",bg = label_colour,font = (myfont, 12))
            l5.pack(pady = 10)
            addexp_window.after(1500, addexp_window.destroy)
        else:
            messagebox.showwarning("Error", "Please enter all values!")
        
        
    addexp_window = Tk()
    addexp_window.title('Add Expense')
    addexp_window.geometry("%dx%d" % (width, height))
    addexp_window.configure(bg=label_colour)

    cat_text = StringVar()
    cat_list = ["Savings", "Utilities", "Rent", "Insurance", "Transport", "Food", "Medical", "Entertainment", "Miscellaneous"]
    cat_list.sort()
    cat_menu = OptionMenu(addexp_window,cat_text, *cat_list)
    cat_menu.configure(bg=button_colour)
    cat_text.set("")

    mop_text = StringVar()
    mop_list = ["Cash", "Card", "UPI"]
    mop_menu = OptionMenu(addexp_window,mop_text, *mop_list)
    mop_menu.configure(bg=button_colour)
    mop_text.set("")

    date_label = Label(addexp_window, text="Date", bg = label_colour, font = (myfont, 12))
    cal = Calendar(addexp_window, selectmode = 'day')

    amt_label = Label(addexp_window, text="Amount",bg = label_colour,font = (myfont, 12))
    amt_entry = Entry(addexp_window, font = (myfont, 12))
    note_entry = Entry(addexp_window, font = (myfont, 12))
    cat_label = Label(addexp_window, text="Category", bg=label_colour, font = (myfont, 12))
    mop_label = Label(addexp_window, text="Mode of Payment", bg=label_colour, font = (myfont, 12))
    note_label = Label(addexp_window, text="Note",bg = label_colour,font = (myfont, 12))
    b = Button(addexp_window,text="Add", command=add_database, font = (myfont, 12),bg = button_colour)

    date_label.pack(pady = 10)
    cal.pack()
    amt_label.pack(pady = 10)
    amt_entry.pack()
    cat_label.pack(pady = 10)
    cat_menu.pack()
    mop_label.pack(pady = 10)
    mop_menu.pack()
    note_label.pack(pady = 10)
    note_entry.pack()
    b.pack(pady = 10)

#on pressing 'set budget' Button
def setBudget(userid):
    budget_window = Tk()
    budget_window.title('Budget set')
    budget_window.geometry("300x300")
    budget_window.configure(bg=label_colour) 
    
    def setDatabase():
        budget = budget_entry.get()
        cat = cat_text.get()
        
        if(budget.isdigit() and cat):
            #userid amount category
            cur.execute("SELECT * FROM budget WHERE CATEGORY = ?", (cat,))
            result = cur.fetchall()
            if(result == []):
                exp_query = '''INSERT INTO budget(USERID, AMOUNT, CATEGORY)
                    VALUES(?,?,?)'''
                exp_tuple = (userid, budget, cat)
                cur.execute(exp_query, exp_tuple)
            else:
                cur.execute("UPDATE budget SET amount = ? WHERE category = ? and userid = ?", (budget, cat, userid))

            l1 = Label(budget_window,text = "Budget set successfully!" ,bg = label_colour)
            l1.pack()
        else:
            messagebox.showwarning("Error", "Invalid entry! Please try again")

        conn.commit()

    cat_text = StringVar()
    cat_list = ["Savings", "Insurance", "Travel", "Utilities", "Transport", "Food", "Medical", "Entertainment", "Miscellaneous"]
    cat_list.sort()
    cat_menu = OptionMenu(budget_window,cat_text, *cat_list)
    cat_menu.configure(bg=button_colour)
    cat_text.set("")
    budget_entry = Entry(budget_window, bg = button_colour, font = (myfont, 12))

    budget_button = Button(budget_window, text = "Set", command=setDatabase, bg = button_colour, font = (myfont, 12))
    cat_label = Label(budget_window, text="Select category", bg=label_colour, font = (myfont, 12))
    cat_label.pack(pady = 10)
    
    cat_label.pack()
    cat_menu.pack()
    budget_entry.pack(pady = 10)
    budget_button.pack(pady = 10) 
    budget_window.mainloop()


def home(user):
    #window creation
    home_window = Tk()
    home_window.title('Home')
    home_window.geometry("%dx%d" % (width, height))
    home_window.configure(bg=label_colour)

    cur.execute("SELECT ID FROM USER WHERE UNAME = ?", (user,))
    userid = cur.fetchone()[0]

    button1 = Button(home_window,text="Add Expenses",width=20, command=lambda: addExpense(userid), bg = button_colour, font = (myfont, 12))
    button1.pack(pady=30)

    button2 = Button(home_window,text="Analytics",width=20, command = lambda: viewGraph(userid), bg = button_colour, font = (myfont, 12))
    button2.pack(pady=30)

    button3 =  Button(home_window, text="Set budget",width=20, command= lambda: setBudget(userid), bg = button_colour, font = (myfont, 12))
    button3.pack(pady = 30)

    button4 =  Button(home_window, text="Expense History",width=20, command= lambda: viewTable(userid), bg = button_colour, font = (myfont, 12))
    button4.pack(pady = 30)
    
    today = datetime.now()
    current_month = today.strftime("%m")

    cur.execute("SELECT SUM(AMOUNT) FROM expenses WHERE strftime('%m', DATE) = ? and userid = ? and CATEGORY = 'Food'", (current_month,userid))
    res = cur.fetchall()
    try:
        sum_ = float(cur.fetchone()[0])
    except:
        sum_ = 0.0

    label1 = Label(home_window, text = str(sum), bg = label_colour, font = (myfont, 12))
    #label1.pack(pady = 50)
    home_window.mainloop()