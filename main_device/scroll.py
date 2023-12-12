from tkinter import *
from graphics import *
from search_database import *


def search(device, choice, start_date = "", end_date = ""): # here is the text view and buttons to graphics.py ver132, added calendar recommend changes!!!
    device, searchhistory = choicev(device, choice, start_date, end_date) # here we call a search_database.py function # ver 132 calemdar update
    #print(searchhistory)
    userdate = 0 # this are the python list index numbers what we show on graphics.py
    temp_in = 1
    humidity_in = 2
    temp_out = 3
    humidity_out = 4 
    top = Toplevel()
    top.geometry("1880x1080")
    top.configure(background="black")
    scrollbar = Scrollbar(top)
    scrollbar.pack( side = RIGHT, fill = Y )
    if choice == "max" or choice == "min":
        btn3 = Button(top, text="exit",width=30, height=3,fg="white", bg="black",font=("helvetica", 15), command=lambda: top.destroy()).pack()
        
    else: 
        if device == "hedgerun": #here we tested out how many buttons to show user this option is 2 buttons
            userdate = 0
            btn2 = Button(top, text="exit",width=20, height=3,fg="white", bg="black",font=("helvetica", 15), command=top.destroy).pack()
            btn3 = Button(top, text="runnings in to graphics",width=30, height=3,fg="white", bg="black",font=("helvetica", 15), command=lambda: show_graphics(searchhistory, device, temp_in, userdate)).pack()
      
        if device == "livingroom" or device == "kitchen":  # 5 buttons
            btn2 = Button(top, text="exit",width=20, height=3,fg="white", bg="black",font=("helvetica", 15), command=top.destroy).pack()
            btn3 = Button(top, text="temperature in to graphics",width=30, height=3,fg="white", bg="black",font=("helvetica", 15), command=lambda: show_graphics(searchhistory, device, temp_in, userdate)).pack()
            btn3 = Button(top, text="humidity in to graphics",width=30, height=3,fg="white", bg="black",font=("helvetica", 15), command=lambda: show_graphics(searchhistory, device, humidity_in, userdate)).pack()
            btn4 = Button(top, text="temperature out to graphics",width=30, height=3,fg="white", bg="black",font=("helvetica", 15), command=lambda: show_graphics(searchhistory, device, temp_out, userdate)).pack()
            btn5 = Button(top, text="humidity out to graphics",width=30, height=3,fg="white", bg="black",font=("helvetica", 15), command=lambda: show_graphics(searchhistory, device, humidity_out, userdate)).pack()
      
        if device == "hedgeroom" or device == "bedroom": # 3 buttons
            btn2 = Button(top, text="exit",width=20, height=3,fg="white", bg="black",font=("helvetica", 15), command=top.destroy).pack()
            btn3 = Button(top, text="temperature in to graphics",width=30, height=3,fg="white", bg="black",font=("helvetica", 15), command=lambda: show_graphics(searchhistory, device, temp_in, userdate)).pack()
            btn3 = Button(top, text="humidity in to graphics",width=30, height=3,fg="white", bg="black",font=("helvetica", 15), command=lambda: show_graphics(searchhistory, device, humidity_in, userdate)).pack()
    
    
    
    mylist = Listbox(top, width=150, height=200,fg="white", bg="black",font=("helvetica", 12), yscrollcommand = scrollbar.set )
    mylist.pack( side = LEFT, fill = BOTH )
    scrollbar.config( command = mylist.yview )
    
    #mainloop()
    print(device, choice)
    i=0
    if device == "livingroom" or device == "kitchen":
        for i in range (len(searchhistory)):
        
            try:
                printlist = searchhistory[i]
                #print(printlist)
                mylist.insert(END, device + " result is: Time " + str(printlist[0]) + " temp: " + str(printlist[1]) + " hum: " + str(printlist[2]) + " and outside temp: " + str(printlist[3]) + " hum " + str(printlist[4]) + "lux value: " + str(printlist[5])) ## here is a mistake.. now you print out the whole list in that db save
            except IndexError: # this is because if user takes a min or max values there is differentlenght list
                printlist = searchhistory[i]
                
                mylist.insert(END, device + " result is: Time in " + str(printlist[0]) + " temp in: " + str(printlist[1]) + " time out: " + str(printlist[0]) + "temp out" + str(printlist[3]) ) 
                
            

    if device == "bedroom":
        for i in range (len(searchhistory)):
            try:
                
                printlist = searchhistory[i]
                #print(printlist)
                mylist.insert(END, device + " result is: Time " + str(printlist[0]) + " temp: " + str(printlist[1]) + " hum: " + str(printlist[2]))
            except IndexError:  # this is because if user takes a min or max values there is differentlenght list
                printlist = searchhistory[i]
                #print(printlist)
                mylist.insert(END, device + " result is: Time " + str(printlist[0]) + " temp: " + str(printlist[1]))
                
    if device == "hedgerun": # hedgehogsdevice
        for i in range (len(searchhistory)):
            
            printlist = searchhistory[i]
            print(printlist)
            mylist.insert(END, device + " result is: Time " + str(printlist[1]) + "  and running is: " + str(printlist[0]))
            
            
            
            

#search("livingroom", "veek")