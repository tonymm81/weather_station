from tkinter import *
import datetime as dt
from scroll import *
#from search_database import *
from tkcalendar import Calendar

start_date = dt.datetime.now()
end_date = dt.datetime.now()

date = ""
def history(): # here user can choose the device what history to search
    top = Toplevel()
    top.title('view history')
    top.configure(background="black")
    living = "livingroom"
    kitch = "kitchen"
    hedrun = "hedgerun"
    bedroom = "bedroom"
    
    lbl = Label(top, text="what you want to search?",fg="white", bg="black",  font=("helvetica", 20)).pack()
    btn2 = Button(top, text="show living room history",fg="white", bg="black",font=("helvetica", 15), command= lambda: history_veek(living)).pack()
    btn3 = Button(top, text="show kitchen history", fg="white", bg="black", font=("helvetica", 15),command= lambda: history_veek(kitch)).pack()
    btn5 = Button(top, text="show hedgehogs running history",fg="white", bg="black",font=("helvetica", 15), command= lambda: history_veek(hedrun)).pack() # have to use lambda comand if you want to take a value and give it to function
    btn14 = Button(top, text="show bedrooms history",fg="white", bg="black",font=("helvetica", 15), command= lambda: history_veek(bedroom)).pack()
    btn8 = Button(top, text="exit on this view", fg="white", bg="black",font=("helvetica", 15), command=top.destroy).pack()
    
    top.mainloop() 
  

 
def history_veek(device): # here we show what data user wants to choose. veek or month etc. 
       
    
    top = Toplevel()  
    top.title('history page')
    top.configure(background="black")
    choice = ""
    top.update()
    #print(device)
    lbl1 = Label(top, text="what you want to search?",fg="white", bg="black",  font=("helvetica", 20)).pack()
    btn9 = Button(top, text= device + " history per veek"  ,fg="white", bg="black",font=("helvetica", 15), command= lambda: search(device, "veek")).pack()
    btn10 = Button(top, text= device + " history per month", fg="white", bg="black", font=("helvetica", 15),command= lambda: search(device, "month")).pack()
    btn11 = Button(top, text=device + " make a custom search",fg="white", bg="black", font=("helvetica", 15), command= lambda: chooce_from_calendar(device)).pack()
    btn12 = Button(top, text=device + " min value",fg="white", bg="black",font=("helvetica", 15), command= lambda:  search(device, "min")).pack()
    btn14 = Button(top, text=device + " max value", fg="white", bg="black",font=("helvetica", 15), command= lambda: search(device, "max")).pack()
    btn13 = Button(top, text="exit on this view", fg="white", bg="black",font=("helvetica", 15), command=top.destroy).pack()
    top.update()
   


def chooce_from_calendar(device):
    global start_date, end_date
    
    start = StringVar()
    ending = StringVar()
    top2 = Toplevel()
    top2.geometry("600x600")
    top2.title('choose from calendar')
    # Add Calendar
    cal = Calendar(top2, selectmode = 'day',
                   year = 2023, month = 2,
                   day = 1, date_pattern="y-mm-dd")
    cal.pack(pady = 20)
    Button(top2, text = "Get start Date",
       command = lambda: [grad_date(cal,"start"), start.set(str("You choose start date: "+ start_date))]).pack()
    Button(top2, text = "Get end Date",
       command = lambda: [grad_date(cal,"end"), ending.set(str("You choose end date: " + end_date))]).pack()
    Button(top2, text = "search from database",
       command = lambda: [search(device, "custom", start_date, end_date), top2.destroy()]).pack()
    start.set(str(start_date))
    ending.set(str(end_date))
    date2 = Label(top2, textvariable=ending)
    date2.pack(side = BOTTOM)
    date = Label(top2, textvariable=start)
    date.pack(side = BOTTOM)
    
    top2.mainloop()
    
    
def grad_date(cal, date_select): # take a datetime from calendar make here strftime what changes to date correct format.
    global start_date, end_date
    
    if date_select == "start":
        date_select = cal.get_date()
        date_select = dt.datetime.strptime(date_select, '%Y-%m-%d')
        start_date = date_select.strftime("'%Y-%m-%d'")
        #date_select = date_select.strftime("'%YYYY-%m-%d'")# edit these
        
    if date_select == "end":
        date_select = cal.get_date()
        date_select = dt.datetime.strptime(date_select, '%Y-%m-%d')
        end_date = date_select.strftime("'%Y-%m-%d'")
        
        
    print(date_select)
        
    return date_select
    


#history()
