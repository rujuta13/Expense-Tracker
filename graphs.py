from main import *
#from excel import *

def viewGraph(userid):

    def view_pie():
        month = month_text.get()
        if(month == 'Jan'):
            month_selected = '01'
        elif(month == 'Feb'):
            month_selected = '02'
        elif(month == 'Mar'):
            month_selected = '03'
        elif(month == 'Apr'):
            month_selected = '04'
        elif(month == 'May'):
            month_selected = '05'
        elif(month == 'Jun'):
            month_selected = '06'
        elif(month == 'Jul'):
            month_selected = '07'
        elif(month == 'Aug'):
            month_selected = '08'
        elif(month == 'Sept'):
            month_selected = '09'
        elif(month == 'Oct'):
            month_selected = '10'
        elif(month == 'Nov'):
            month_selected = '11'
        elif(month == 'Dec'):
            month_selected = '12'
        
        pie_query = '''SELECT category, ROUND(SUM(amount),2) 
            FROM expenses 
            WHERE strftime('%m', date)= ?  AND userid = ?
            GROUP BY category'''
        cur.execute(pie_query, (month_selected, userid))
        Amounts = []
        Categories = []

        result = cur.fetchall()
        for i in result:
            Amounts.append(i[1])
            Categories.append(i[0])

        # Visualize Data
        y = np.array(Amounts)
        fig1, ax1 = plt.subplots()
        ax1.pie(y, labels=Categories, autopct='%1.1f%%', startangle=90, pctdistance=0.85)
        #draw circle
        centre_circle = plt.Circle((0,0),0.70,fc='white')
        fig1 = plt.gcf()
        fig1.gca().add_artist(centre_circle)
        ax1.axis('equal')  
        plt.tight_layout()
        plt.show()

    def view_bar():
        def addlabels(x,y):
            for i in range(len(x)):
                plt.text(i, y[i], y[i], ha = 'center')

        month = month_text.get()
        if(month == 'Jan'):
            month_selected = '01'
        elif(month == 'Feb'):
            month_selected = '02'
        elif(month == 'Mar'):
            month_selected = '03'
        elif(month == 'Apr'):
            month_selected = '04'
        elif(month == 'May'):
            month_selected = '05'
        elif(month == 'Jun'):
            month_selected = '06'
        elif(month == 'Jul'):
            month_selected = '07'
        elif(month == 'Aug'):
            month_selected = '08'
        elif(month == 'Sept'):
            month_selected = '09'
        elif(month == 'Oct'):
            month_selected = '10'
        elif(month == 'Nov'):
            month_selected = '11'
        elif(month == 'Dec'):
            month_selected = '12'
        
        bar_query = '''SELECT category, ROUND(SUM(amount),2) 
            FROM expenses 
            WHERE strftime('%m', date)= ? AND userid = ?
            GROUP BY category'''
        cur.execute(bar_query,(month_selected, userid))

        result = cur.fetchall()
        Amounts = []
        Categories = []
        for i in result:
            Amounts.append(i[1])
            Categories.append(i[0])

        # Visualize Data
        plt.figure(figsize = (10, 5))
        plt.bar(Categories, Amounts)
        plt.xlabel("Categories")
        plt.ylabel("Amount (₹)")
        addlabels(Categories, Amounts)
        plt.show()

    graph_window = Tk()
    graph_window.title('Graphs')
    graph_window.geometry("300x300")
    graph_window.configure(bg=label_colour)

    month_label = Label(graph_window, text="Select month:", bg = label_colour, font = (myfont, 12))
    month_text = StringVar()
    month_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    month_menu = OptionMenu(graph_window, month_text, *month_list)
    month_menu.configure(bg=button_colour)
    month_text.set("")
        
    bar_button = Button(graph_window,text="Bar Graph",width=20, command=view_bar, bg = button_colour, font = (myfont, 12))
    pie_button = Button(graph_window,text="Pie Chart",width=20, command=view_pie, bg = button_colour, font = (myfont, 12))
    month_label.pack(pady=15)
    month_menu.pack()
    bar_button.pack(pady=15)
    pie_button.pack(pady=15)

def viewTable(userid):
    def showFig():
        month = month_text.get()
        if(month == 'Jan'):
            month_selected = '01'
        elif(month == 'Feb'):
            month_selected = '02'
        elif(month == 'Mar'):
            month_selected = '03'
        elif(month == 'Apr'):
            month_selected = '04'
        elif(month == 'May'):
            month_selected = '05'
        elif(month == 'Jun'):
            month_selected = '06'
        elif(month == 'Jul'):
            month_selected = '07'
        elif(month == 'Aug'):
            month_selected = '08'
        elif(month == 'Sept'):
            month_selected = '09'
        elif(month == 'Oct'):
            month_selected = '10'
        elif(month == 'Nov'):
            month_selected = '11'
        elif(month == 'Dec'):
            month_selected = '12'
        
        pie_query = '''SELECT * FROM expenses 
            WHERE strftime('%m', date)= ?  AND userid = ? ORDER BY category, amount'''
        cur.execute(pie_query, (month_selected, userid))
        result = cur.fetchall()
        Amounts = []
        Categories = []
        Dates = []
        #(1, '2023-03-21', 3000.0, 'Travel', 'UPI', 'Petrol')
        for i in result:
            Dates.append(i[1])
            Amounts.append(i[2])
            Categories.append(i[3])

        fig = go.Figure(data=[go.Table(header=dict(values=["Date", "Amount (₹)", "Category"]),
                                    cells=dict(values=[Dates, Amounts, Categories]))])
        fig.show()

    def export():
        def createExcel():
            month = month_text.get()
            if(month == 'Jan'):
                month_selected = '01'
            elif(month == 'Feb'):
                month_selected = '02'
            elif(month == 'Mar'):
                month_selected = '03'
            elif(month == 'Apr'):
                month_selected = '04'
            elif(month == 'May'):
                month_selected = '05'
            elif(month == 'Jun'):
                month_selected = '06'
            elif(month == 'Jul'):
                month_selected = '07'
            elif(month == 'Aug'):
                month_selected = '08'
            elif(month == 'Sept'):
                month_selected = '09'
            elif(month == 'Oct'):
                month_selected = '10'
            elif(month == 'Nov'):
                month_selected = '11'
            elif(month == 'Dec'):
                month_selected = '12'
            
            cur.execute("SELECT DATE, AMOUNT, CATEGORY FROM expenses WHERE strftime('%m', date)= ?  AND userid = ? ORDER BY CATEGORY, AMOUNT",(month_selected, userid))
            rows = cur.fetchall()

            
            fname= ex_entry.get() + ".xlsx"
            df = pd.DataFrame(rows, columns=['Date', 'Amount (₹)', 'Category'])
            df.to_excel(fname, index=False)
            l = Label(ex_window, text="Created Successfully",bg = label_colour,font = (myfont, 12))
            l.pack(pady = 10)
            ex_window.after(1500, ex_window.destroy)

        ex_window = Tk()
        ex_window.title("Export")
        ex_window.geometry("200x200")
        ex_window.configure(bg=label_colour)
        ex_label=Label(ex_window, text = "Filename:", bg = label_colour)
        ex_label.pack(pady=10)
        ex_entry = Entry(ex_window, font = (myfont, 12))
        ex_entry.pack()
        ex_button = Button(ex_window, text = "Export", command = createExcel, bg = button_colour)
        ex_button.pack(pady=5)

    table_window = Tk()
    table_window.title('Table')
    table_window.geometry("300x300")
    table_window.configure(bg=label_colour)

    month_label = Label(table_window, text="Select month:", bg = label_colour, font = (myfont, 12))
    month_text = StringVar()
    month_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    month_menu = OptionMenu(table_window, month_text, *month_list)
    month_menu.configure(bg=button_colour)
    month_text.set("")
    month_label.pack(pady=15)
    month_menu.pack()

    label = Label(table_window, text = 'View as table:', bg = label_colour, font = (myfont, 11, 'italic'))
    label.pack(pady = 10)
    b = Button(table_window, text="View",width=20, command= showFig, bg = button_colour, font = (myfont, 12))
    b.pack(pady = 10)

    label = Label(table_window, text = 'Export to excel:', bg = label_colour, font = (myfont, 11, 'italic'))
    label.pack(pady = 10)
    b2 = Button(table_window, text="Excel",width=20, command= export, bg = button_colour, font = (myfont, 12))
    b2.pack()