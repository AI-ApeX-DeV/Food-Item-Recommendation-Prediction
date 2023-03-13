import pandas as pd
import matplotlib.pyplot as plt
import pymysql
from tkcalendar import *
from tkinter import ttk
import numpy as mp
from tkinter import *
import mysql.connector
from datetime import datetime
from PIL import Image,ImageTk
import numpy as np
listbox=1
passee="5"
useree="s"
db=mysql.connector.connect(host="localhost",user="root",passwd="Shahsai@2002",database="shahsai")
mc=db.cursor()
security=Tk()

def secure():
    usernme=rn.get()
    passwrd=rn1.get()
    if(usernme==useree and passwrd==passee):
        security.destroy()
        root= Tk()
        root.geometry("1920x1080")
        img=Image.open(("canteen.png"))
        img = img.resize((1400,130), Image.ANTIALIAS)
        photo=ImageTk.PhotoImage(img)
        f1=Frame(root,borderwidth=8, relief=SUNKEN, bg="dark grey")
        f1.pack()
        l1=Label(f1,image=photo,height=130,width=1920)
        l1.pack()
        l=Label(f1,text="TCET CANTEEN (FOOD RECOMMENDATION AND PREDICTION MODEL)",font=("times new roman",18,'bold'))
        l.pack()
        
        def prediction():
            calendar=Tk()
            cal = Calendar(calendar)
            cal.pack()
            def retrieve_date():
                daten=cal.get_date()
                m,d,y=daten.split("/")
                y=int(str(20)+y)
                m=int(m)
                d=int(d)
                calendar.destroy()
                user = Tk()
##########################

                db=mysql.connector.connect(host="localhost",user="root",passwd="Shahsai@2002",database="shahsai")
                mc=db.cursor()
                s="create table vv as select name,sum(quantity) as sum_of_quan from tcetdata where day(date)=%s and month(date)=%s and year(date)=%s group by name"
                mc.execute(s, (d, m, y))
                s="ALTER TABLE vv add COLUMN probability FLOAT;"
                mc.execute(s)
                query = "SELECT * FROM vv"
                mc.execute(query)
                rows = mc.fetchall()

                for row in rows:
                    name = row[0]
                    quan = row[1]
                    s="select sum(sum_of_quan) from vv"
                    mc.execute(s)
                    a=mc.fetchone()
                    # Calculate the desired value for the "quantity" column
                    prob = float(quan)/float(a[0])

                    # Update the row in the table
                    update_query = "UPDATE vv SET probability=%s WHERE name = %s"
                    mc.execute(update_query, (prob, name))
                db.commit()
                date = datetime.strptime(daten, '%m/%d/%y')
                date=date.date()
                date = date.strftime('%Y-%m-%d')
                for i in range(1,10):
                    
                    s="create table v1 as select name,sum(quantity) as sum_of_quan from tcetdata where date=DATE_SUB(%s, INTERVAL 7*%s DAY) group by name"
                    mc.execute(s, (date,i,))
                    s="ALTER TABLE v1 add COLUMN probability FLOAT;"
                    mc.execute(s)
                    query = "SELECT * FROM v1"
                    mc.execute(query)
                    rows = mc.fetchall()
                    s="select sum(sum_of_quan) from v1"
                    mc.execute(s)
                    a=mc.fetchone()
                    for row in rows:
                        name = row[0]
                        quan = row[1]

                        # Calculate the desired value for the "quantity" column
                        prob = float(quan)/float(a[0])

                        # Update the row in the table
                        update_query = "UPDATE v1 SET probability=%s WHERE name = %s"
                        mc.execute(update_query, (prob, name))

                    s="UPDATE vv r JOIN v1 st ON r.name = st.name SET r.probability = r.probability + st.probability"
                    mc.execute(s)
                    s="drop table v1"
                    mc.execute(s)

                s="update vv set probability=probability/10"
                mc.execute(s)
                db.commit()
                query = "SELECT * FROM vv"
                mc.execute(query)
                rows = mc.fetchall()
                s="select sum(probability) from vv"
                mc.execute(s)
                a=mc.fetchone()
                for row in rows:
                    name = row[0]
                    probi = row[2]
                    # Calculate the desired value for the "quantity" column
                    prob = float(probi)/float(a[0])

                    # Update the row in the table
                    update_query = "UPDATE vv SET probability=%s WHERE name = %s"
                    mc.execute(update_query, (prob, name))
                db.commit()



##########################
                tree = ttk.Treeview(user,height=40)
                #tree.pack()
                mc=db.cursor()
                s="select name,probability from vv"
                mc.execute(s)
                
                columns = [desc[0] for desc in mc.description]
                tree["columns"] = columns
                for col in columns:
                    tree.heading(col, text=col)
                for row in mc:
                    tree.insert("", "end", values=row)
                tree.pack()
######              
                mc.execute("SELECT name,probability FROM vv")
                rowss = mc.fetchall()
                Names = []
                probb = []

                for i in rowss:
                    Names.append(i[0])
                    probb.append(i[1])
                plt.bar(Names,probb)
                plt.autoscale()
                plt.xlabel('name')
                plt.ylabel('probability')
                plt.title('food item prediction')
                plt.show()
                s="drop table vv"
                mc.execute(s)
                db.commit()
########

                user.mainloop()
            button = Button(calendar, text="Retrieve Date", command=retrieve_date)
            button.pack()
            calendar.mainloop()


        def reload(f4,f5):
            def button_click(event):
                widget = event.widget
                row = widget.grid_info()["row"]
                delete(row)       
    
            def delete(row):
                db=mysql.connector.connect(host="localhost",user="root",passwd="Shahsai@2002",database="shahsai")
                mc=db.cursor()
                a=listbox.get(row)[0]
                b=listbox.get(row)[1]
                s="delete from tcet where name=%s and quantity=%s"
                e=[(a,b)]
                mc.executemany(s,e)       
                db.commit()            
                reload(f4,f5)

            for widget in f4.winfo_children():
                    widget.destroy()
            for widget in f5.winfo_children():
                    widget.destroy()
            #f5=Frame(root,height='1000',width='1000',borderwidth=6,bg='grey')
            db=mysql.connector.connect(host="localhost",user="root",passwd="Shahsai@2002",database="shahsai")
            mc=db.cursor()
            mc.execute("select name,sum(quantity),sum(money) from tcetdata where hour(time)=hour(curtime()) and day(date)=day(curdate()) group by name order by sum(quantity) desc limit 5")
            rows=mc.fetchall()
            listbox=Listbox(f5,font='50')
            for row in rows:
                listbox.insert(END,row)
                buttons = []
            for i in range(listbox.size()):
                item = listbox.get(i)
                button = Button(f5, text=item,width='25',height='2')
                button.grid(row=i, column=0)
                buttons.append(button)
            f5.pack(side=RIGHT,anchor='ne')

            #f4=Frame(root,height='1000',width='1000',borderwidth=6,bg='grey')
            db=mysql.connector.connect(host="localhost",user="root",passwd="Shahsai@2002",database="shahsai")
            mc=db.cursor()
            mc.execute("select name,quantity,money from tcet order by quantity desc")
            rows=mc.fetchall()
            listbox=Listbox(f4,font='50')
            for row in rows:
                listbox.insert(END,row)
                buttons = []
            for i in range(listbox.size()):
                item = listbox.get(i)
                button = Button(f4, text=item,width='25',height='2')
                button.grid(row=i, column=0)
                button.bind("<Button-1>", button_click)
                buttons.append(button)
            f4.pack(side=RIGHT,anchor='ne')       

        def moniter():
            calendar=Tk()
            cal = Calendar(calendar)
            cal.pack()
            def monigraph():
                def totalreven():
                    soo=Tk()
                    soo.geometry("500x500")
                    db=mysql.connector.connect(host="localhost",user="root",passwd="Shahsai@2002",database="shahsai")
                    mc=db.cursor()
                    s='select sum(money) from tcetdata where day(date)=%s and month(date)=%s and year(date)=%s '
                    mc.execute(s, (d, m, y))
                    c=mc.fetchone()
                    s1=Frame(soo,borderwidth=8, relief=SUNKEN, bg="dark grey")
                    l=Label(s1,text="TOTAL REVENUE")
                    l.grid(row=1,column=0,padx=20,pady=10)
                    l=Label(s1,text=c)
                    l.grid(row=3,column=0,padx=20,pady=10)
                    s1.pack()
                    soo.mainloop()


                db=mysql.connector.connect(host="localhost",user="root",passwd="Shahsai@2002",database="shahsai")
                mycursor = db.cursor()
                s="SELECT name,quantity FROM tcetdata where day(date)=%s and month(date)=%s and year(date)=%s"
                mycursor.execute(s, (d, m, y))
                rowss = mycursor.fetchall()
                Names = []
                Money = []

                for i in rowss:
                    Names.append(i[0])
                    Money.append(i[1])
                plt.bar(Names,Money)
                plt.autoscale()
                plt.xlabel('name')
                plt.ylabel('quantity')
                plt.title('food statistics')
                plt.show()
                totalreven()


            def retrieve_date():
                daten=cal.get_date()
                global m,d,y
                m,d,y=daten.split("/")
                y=int(str(20)+y)
                m=int(m)
                d=int(d)
                calendar.destroy()
                user = Tk()

                db=mysql.connector.connect(host="localhost",user="root",passwd="Shahsai@2002",database="shahsai")
                mc = db.cursor()
                tree = ttk.Treeview(user,height=40)
                tree.pack()
                mc=db.cursor()
                s="select * from tcetdata where day(date)=%s and month(date)=%s and year(date)=%s order by time desc"
                mc.execute(s, (d, m, y))
                
                columns = [desc[0] for desc in mc.description]
                tree["columns"] = columns
                for col in columns:
                    tree.heading(col, text=col)
                for row in mc:
                    tree.insert("", "end", values=row)
                monigraph()

                user.mainloop()
            button = Button(calendar, text="Retrieve Date", command=retrieve_date)
            button.pack()
            calendar.mainloop()            


        def userlog():
            calendar=Tk()
            cal = Calendar(calendar)
            cal.pack()
            def retrieve_date():
                daten=cal.get_date()
                m,d,y=daten.split("/")
                y=int(str(20)+y)
                m=int(m)
                d=int(d)
                calendar.destroy()
                user = Tk()

                db=mysql.connector.connect(host="localhost",user="root",passwd="Shahsai@2002",database="shahsai")
                mc = db.cursor()
                tree = ttk.Treeview(user,height=40)
                tree.pack()
                mc=db.cursor()
                s="select * from tcetdata where day(date)=%s and month(date)=%s and year(date)=%s order by time desc"
                mc.execute(s, (d, m, y))
                
                columns = [desc[0] for desc in mc.description]
                tree["columns"] = columns
                for col in columns:
                    tree.heading(col, text=col)
                for row in mc:
                    tree.insert("", "end", values=row)

                user.mainloop()
            button = Button(calendar, text="Retrieve Date", command=retrieve_date)
            button.pack()
            calendar.mainloop()



           

        def mrevenue():
            soo=Tk()
            soo.geometry("500x500")
            db=mysql.connector.connect(host="localhost",user="root",passwd="Shahsai@2002",database="shahsai")
            mc=db.cursor()
            s='select sum(money) from tcetdata where month(date)=month(curdate())'
            mc.execute(s)
            c=mc.fetchone()
            s1=Frame(soo,borderwidth=8, relief=SUNKEN, bg="dark grey")
            l=Label(s1,text="MONTHLY REVENUE")
            l.grid(row=1,column=0,padx=20,pady=10)
            l=Label(s1,text=c)
            l.grid(row=3,column=0,padx=20,pady=10)
            s1.pack()
            soo.mainloop()

        def drevenue():
            soo=Tk()
            soo.geometry("500x500")
            db=mysql.connector.connect(host="localhost",user="root",passwd="Shahsai@2002",database="shahsai")
            mc=db.cursor()
            s='select sum(money) from tcetdata where day(date)=day(curdate())'
            mc.execute(s)
            c=mc.fetchone()
            s1=Frame(soo,borderwidth=8, relief=SUNKEN, bg="dark grey")
            l=Label(s1,text="DAILY REVENUE")
            l.grid(row=1,column=0,padx=20,pady=10)
            l=Label(s1,text=c)
            l.grid(row=3,column=0,padx=20,pady=10)
            s1.pack()
            soo.mainloop()

        def plotmm():
            db=mysql.connector.connect(host="localhost",user="root",passwd="Shahsai@2002",database="shahsai")
            mycursor = db.cursor()
            mycursor.execute("SELECT name, sum(money) as money FROM tcetdata WHERE MONTH(CURRENT_DATE()) = MONTH(date) group by name")
            rowss = mycursor.fetchall()
            Names = []
            Money = []

            for i in rowss:
                Names.append(i[0])
                Money.append(i[1])
            plt.bar(Names,Money)
            plt.autoscale()
            plt.xlabel('name')
            plt.ylabel('money')
            plt.title('food statistics (MONTHLY MONEY)')
            plt.show()
        def plothq():
            db=mysql.connector.connect(host="localhost",user="root",passwd="Shahsai@2002",database="shahsai")
            mycursor = db.cursor()
            mycursor.execute("select name,sum(quantity) as quantity from tcetdata where date=curdate() group by name")
            rowss = mycursor.fetchall()
            Names = []
            Money = []

            for i in rowss:
                Names.append(i[0])
                Money.append(i[1])
            plt.bar(Names,Money)
            plt.autoscale()
            plt.xlabel('name')
            plt.ylabel('money')
            plt.title('food statistics (DAILY QUANTITY)')
            plt.show()

        def plotmq():

            db=mysql.connector.connect(host="localhost",user="root",passwd="Shahsai@2002",database="shahsai")
            mycursor = db.cursor()
            mycursor.execute("SELECT name, sum(quantity) as quantity FROM tcetdata WHERE MONTH(CURRENT_DATE()) = MONTH(date) group by name")
            rowss = mycursor.fetchall()
            Names = []
            quantity = []

            for i in rowss:
                Names.append(i[0])
                quantity.append(i[1])
            plt.bar(Names,quantity)
            plt.autoscale()
            plt.xlabel('name')
            plt.ylabel('quantity')
            plt.title('food statistics (MONTHLY QUANTITY)')
            plt.show()

        def plothm():
            db=mysql.connector.connect(host="localhost",user="root",passwd="Shahsai@2002",database="shahsai")
            mycursor = db.cursor()
            mycursor.execute("select name,sum(money) as money from tcetdata where date=curdate() group by name")
            rowss = mycursor.fetchall()
            Names = []
            Money = []

            for i in rowss:
                Names.append(i[0])
                Money.append(i[1])
            plt.bar(Names,Money)
            plt.autoscale()
            plt.xlabel('name')
            plt.ylabel('money')
            plt.title('food statistics (DAILY MONEY)')
            plt.show()

        def modify(v,a,b):
    
            def yipee():
                def delete(n):
                    db=mysql.connector.connect(host="localhost",user="root",passwd="Shahsai@2002",database="shahsai")
                    mc=db.cursor()
                    a=listbox.get(n)[0]
                    b=listbox.get(n)[1]
                    s="delete from tcet where name=%s and quantity=%s"
                    e=[(a,b)]
                    mc.executemany(s,e)       
                    db.commit()    
                    reload(f4,f5)
                

                def button_click(event):
                    widget = event.widget
                    row = widget.grid_info()["row"]
                    column = widget.grid_info()["column"]
                    delete(row)               
                nin=lo.get()
                mon=int(nin)*int(a)
                db=mysql.connector.connect(host="localhost",user="root",passwd="Shahsai@2002",database="shahsai")
                mc=db.cursor()
                s="insert into tcet (name,quantity,date,time,money) values(%s,%s,curdate(),curtime(),%s)"
                e=[(v,nin,mon)]
                mc.executemany(s,e)
                db.commit()
                db=mysql.connector.connect(host="localhost",user="root",passwd="Shahsai@2002",database="shahsai")
                mc=db.cursor()
                s="insert into tcetdata (name,quantity,date,time,money) values(%s,%s,curdate(),curtime(),%s)"
                e=[(v,nin,mon)]
                mc.executemany(s,e)
                db.commit()                
                lo.destroy()
                sub.destroy()
                for widget in f4.winfo_children():
                    widget.destroy()
                for widget in f5.winfo_children():
                    widget.destroy()
                db=mysql.connector.connect(host="localhost",user="root",passwd="Shahsai@2002",database="shahsai")
                mc=db.cursor()
                mc.execute("select name,sum(quantity),sum(money) from tcetdata where hour(time)=hour(curtime()) and day(date)=day(curdate()) group by name order by sum(quantity) desc limit 5")
                rows=mc.fetchall()
                listbox=Listbox(f5,font='50')
                for row in rows:
                    listbox.insert(END,row)
                    buttons = []
                for i in range(listbox.size()):
                    item = listbox.get(i)
                    button = Button(f5, text=item,width='25',height='2')
                    button.grid(row=i, column=0)
                    buttons.append(button)
                f5.pack(side=RIGHT,anchor='ne')    
                db=mysql.connector.connect(host="localhost",user="root",passwd="Shahsai@2002",database="shahsai")
                mc=db.cursor()
                mc.execute("select name,quantity,money from tcet order by quantity desc")
                rows=mc.fetchall()
                listbox=Listbox(f4,font='50')
                #listbox.pack(expand=TRUE,fill=BOTH,side=TOP)
                for row in rows:
                    listbox.insert(END,row)
                buttons = []
                for i in range(listbox.size()):
                    item = listbox.get(i)
                    button = Button(f4, text=item,width='25',height='2')
                    button.grid(row=i, column=0)
                    button.bind("<Button-1>", button_click)
                    buttons.append(button)
                    #button.pack()
                f4.pack(side=RIGHT,anchor='ne')
                  
            lo=Entry(f3,width=8)
            lo.grid(row=(b),column=2,padx=10,pady=2)
            sub=Button(f3,text='ENTER',command=yipee)
            sub.grid(row=(b),column=3,padx=2,pady=2)                

        def button_click(event):
            widget = event.widget
            row = widget.grid_info()["row"]
            delete(row)       
        def delete(row):
            db=mysql.connector.connect(host="localhost",user="root",passwd="Shahsai@2002",database="shahsai")
            mc=db.cursor()
            a=listbox.get(row)[0]
            b=listbox.get(row)[1]
            s="delete from tcet where name=%s and quantity=%s"
            e=[(a,b)]
            mc.executemany(s,e)       
            db.commit()              
            reload(f4,f5)



        f3=Frame(root,borderwidth=6,bg='grey')
        f3.place(x=0,y=950)
        v1=Button(f3,text="samosa",font= ('Helvetica 10 bold'),command=lambda:modify('samosa',15,1))
        v1.grid(row=1,column=1,padx=5,pady=3)
        v1=Button(f3,text="vada pav",font= ('Helvetica 10 bold'),command=lambda:modify("vada pav",12,2))
        v1.grid(row=2,column=1,padx=5,pady=3)
        v1=Button(f3,text="masala dosa",font= ('Helvetica 10 bold'),command=lambda:modify('masala dosa',40,3))
        v1.grid(row=3,column=1,padx=5,pady=3)
        v1=Button(f3,text= "mysore dosa",font= ('Helvetica 10 bold'),command=lambda:modify('mysore dosa',55,4))
        v1.grid(row=4,column=1,padx=5,pady=3)
        v1=Button(f3,text=" pav bhaji",font= ('Helvetica 10 bold'),command=lambda:modify('pav bhaji',40,5))
        v1.grid(row=5,column=1,padx=5,pady=3)
        v1=Button(f3,text="mendu vada",font= ('Helvetica 10 bold'),command=lambda:modify('medu vada',35,6))
        v1.grid(row=6,column=1,padx=5,pady=3)
        v1=Button(f3,text="thali",font= ('Helvetica 10 bold'),command=lambda:modify('thali',60,7))
        v1.grid(row=7,column=1,padx=5,pady=3)
        v1=Button(f3,text="chole",font= ('Helvetica 10 bold'),command=lambda:modify('chole',40,8))
        v1.grid(row=8,column=1,padx=5,pady=3)
        v1=Button(f3,text="sandwich",font= ('Helvetica 10 bold'),command=lambda:modify('sandwich',65,9))
        v1.grid(row=9,column=1,padx=5,pady=3)
        v1=Button(f3,text="chinese noodles",font= ('Helvetica 10 bold'),command=lambda:modify('chinese noodles',50,10))
        v1.grid(row=10,column=1,padx=5,pady=3)
        v1=Button(f3,text="fried rice",font= ('Helvetica 10 bold'),command=lambda:modify('fried rice',60,11))
        v1.grid(row=11,column=1,padx=5,pady=3)
        v1=Button(f3,text="poori bhaji",font= ('Helvetica 10 bold'),command=lambda:modify('poori bhaji',45,12))
        v1.grid(row=12,column=1,padx=5,pady=3)
        v1=Button(f3,text="uttapam",font= ('Helvetica 10 bold'),command=lambda:modify('uttapam',70,13))
        v1.grid(row=13,column=1,padx=5,pady=3)
        v1=Button(f3,text="dal rice",font= ('Helvetica 10 bold'),command=lambda:modify('dal rice',30,14))
        v1.grid(row=14,column=1,padx=5,pady=3)
        v1=Button(f3,text="idli",font= ('Helvetica 10 bold'),command=lambda:modify('idli',35,15))
        v1.grid(row=15,column=1,padx=5,pady=3)
        v1=Button(f3,text="BAR GRAPH MONTHLY(quantity)",font= ('Helvetica 10 bold'),command=lambda:plotmq())
        v1.grid(row=1,column=8,padx=5,pady=2)
        v1=Button(f3,text="BAR GRAPH MONTHLY(money)",font= ('Helvetica 10 bold'),command=lambda:plotmm())
        v1.grid(row=2,column=8,padx=5,pady=2)
        v1=Button(f3,text="BAR GRAPH DAILY(money)",font= ('Helvetica 10 bold'),command=lambda:plothm())
        v1.grid(row=3,column=8,padx=5,pady=2)
        v1=Button(f3,text="BAR GRAPH DAILY(quantity)",font= ('Helvetica 10 bold'),command=lambda:plothq())
        v1.grid(row=4,column=8,padx=5,pady=2)
        v1=Button(f3,text="MONTHLY REVENUE",font= ('Helvetica 10 bold'),command=lambda:mrevenue())
        v1.grid(row=5,column=8,padx=5,pady=2)
        v1=Button(f3,text="DAILY REVENUE",font= ('Helvetica 10 bold'),command=lambda:drevenue())
        v1.grid(row=6,column=8,padx=5,pady=2)
        v1=Button(f3,text="USER LOGS",font= ('Helvetica 10 bold'),command=lambda:userlog())
        v1.grid(row=7,column=8,padx=5,pady=2)
        v1=Button(f3,text="MONITORING",font= ('Helvetica 10 bold'),command=lambda:moniter())
        v1.grid(row=8,column=8,padx=5,pady=2)
        v1=Button(f3,text="PREDICTION",font= ('Helvetica 10 bold'),command=lambda:prediction())
        v1.grid(row=9,column=8,padx=5,pady=2)


        f3.pack(side=LEFT,fill=BOTH)

        f5=Frame(root,height='1000',width='1000',borderwidth=6,bg='grey')
        db=mysql.connector.connect(host="localhost",user="root",passwd="Shahsai@2002",database="shahsai")
        mc=db.cursor()
        mc.execute("select name,sum(quantity),sum(money) from tcetdata where hour(time)=hour(curtime()) and day(date)=day(curdate()) group by name order by sum(quantity) desc limit 5")
        rows=mc.fetchall()
        listbox=Listbox(f5,font='50')
        for row in rows:
            listbox.insert(END,row)
            buttons = []
        for i in range(listbox.size()):
            item = listbox.get(i)
            button = Button(f5, text=item,width='25',height='2')
            button.grid(row=i, column=0)
            buttons.append(button)
        f5.pack(side=RIGHT,anchor='ne')

        f4=Frame(root,height='1000',width='1000',borderwidth=6,bg='grey')
        db=mysql.connector.connect(host="localhost",user="root",passwd="Shahsai@2002",database="shahsai")
        mc=db.cursor()
        mc.execute("select name,quantity,money from tcet order by quantity desc")
        rows=mc.fetchall()
        listbox=Listbox(f4,font=("Helvetica",50))
        for row in rows:
            listbox.insert(END,row)
            buttons = []
        for i in range(listbox.size()):
            item = listbox.get(i)
            button = Button(f4, text=item,width='25',height='2')
            button.grid(row=i, column=0)
            button.bind("<Button-1>", button_click)
            buttons.append(button)
        f4.pack(side=RIGHT,anchor='ne')



        root.mainloop()
    else:
        name_label=Label(sec,text="INVALID USERNAME/PASSWORD",bg="grey")
        name_label.grid(row=3,column=0,columnspan=2)  
sec=Frame(security,borderwidth=8, relief=SUNKEN, bg="dark grey")
name_label=Label(sec,text="USERNAME",bg="grey")
name_label.grid(row=0,column=0)    
rn=Entry(sec,width=30)
rn.grid(row=0,column=1,padx=30)
name_label=Label(sec,text="PASSWORD",bg="grey")
name_label.grid(row=1,column=0)    
rn1=Entry(sec,width=30)
rn1.grid(row=1,column=1,padx=30)
submit=Button(sec,text=" ENTER ",command=secure)
submit.grid(row=2,column=0,columnspan=2,padx=20,pady=5)
sec.pack(side=TOP,fill=BOTH,expand=TRUE)
security.mainloop()