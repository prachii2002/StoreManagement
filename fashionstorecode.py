#%%
import mysql.connector

con=mysql.connector.connect(host='localhost',user='root',password='1111')
cursor=con.cursor()
cursor.execute('create database if not exists store;')
cursor.execute('use store;')

cursor.execute('''create table if not exists inventory1(sno int primary key,
                        type varchar(20) check(type in('Tops','Bottoms','Accessories')),
                        name varchar(100) not null,
                        quantity int not null,
                        costprice int not null,
                        saleprice int not null,
                        totalcostprice int,
                        totalsaleprice int,
                        assumedprofit int,
                       
                        sold int not null);''')


import tkinter as tk
import tkinter.messagebox
root=tk.Tk()
root.title('Store management')
root.geometry('800x220')
root.configure(background='white')
qry='''update inventory1 set totalcostprice=costprice*quantity;'''
cursor.execute(qry)
qry='''update inventory1 set totalsaleprice=saleprice*quantity;'''
cursor.execute(qry)
qry='''update inventory1 set assumedprofit=totalsaleprice-totalcostprice;'''
cursor.execute(qry)


pdlist=[]
pdqtylist=[]
pdpricelist=[]
pdidlist=[]

   

   


def add():
   
    sno=e1.get()
    typ=e2.get()
    nm=e3.get()
    qty=e4.get()
    cp=e5.get()
    sp=e6.get()
    sld=e7.get()
    e1.delete(0,tk.END)
    e2.delete(0,tk.END)
    e3.delete(0,tk.END)
    e4.delete(0,tk.END)
    e5.delete(0,tk.END)
    e6.delete(0,tk.END)
    e7.delete(0,tk.END)
   
    print(sno)
    qry='''select sno from inventory1;'''
    cursor.execute(qry)
    d=cursor.fetchall()
    print(d)
    l=[]
    for i in d:
        l.append(int((i[0])))
    print(l)
    if int(sno) in l:
        tkinter.messagebox.showinfo('Error','Product with same sno already in inventory')
    if typ not in ['Tops','Bottoms','Accessories']:
        tkinter.messagebox.showinfo('Error','Enter a valid product type')
    if qty.isdigit()==False or cp.isdigit()==False or sp.isdigit()==False:
        tkinter.messagebox.showinfo('Error','The quantity,costprice,saleprice should be numbers')
    if cp>sp:
        tkinter.messagebox.showinfo('Error','The saleprice is less than costprice!')
       
       
    else:
   
        w='''insert into inventory1 (sno,type,name,quantity,costprice,saleprice,sold)
        values({},'{}','{}',{},{},{},{})'''.format(sno,typ,nm,qty,cp,sp,sld)
        cursor.execute(w)
        con.commit()
qry='''select sno from inventory1;'''
cursor.execute(qry)
d=cursor.fetchall()
print(d)
l=[]
for i in d:
    l.append(int((i[0])))
    #print(l)
   
   
   
def display():
    top=tk.Toplevel()
    top.configure(background='lightblue')
    cursor.execute('select*from inventory1;')
    disp=cursor.fetchall()
    a=''
    for row in disp:
        a+=str(row)
        a+='\n'
    mylabel=tk.Label(top,text=a,bg='white',fg='black')
    mylabel.grid()
   
   

def graph():
    top=tk.Toplevel()
    import matplotlib
    matplotlib.use('TkAgg')
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    figure=Figure(figsize=(5,4),dpi=100)
    plot=figure.add_subplot(1,1,1)
    canvas=FigureCanvasTkAgg(figure,top)
    canvas.get_tk_widget().grid(row=0,column=0)
   
    cursor.execute('select*from inventory1;')
    dis=cursor.fetchall()
    print(dis)
   
    import numpy as np
    li=[]
    for i in dis:
        li.append(i[8])      #sold
    name=[]
    for i in dis:
        name.append(i[2])
    print(name)
    ww=np.arange(len(name))
    plot.bar(ww,li,color='r',width=0.1)
    plot.set_title('Performance')
    plot.set_xticks(ww)
    plot.set_xticklabels(name)
    plot.set_xlabel('Product Name')
    plot.set_ylabel('Assumed profit')
   
   
def update():
    sno=e1.get()
    typ=e2.get()
    nm=e3.get()
    qty=e4.get()
    cp=e5.get()
    sp=e6.get()
    sld=e7.get()
    e1.delete(0,tk.END)
    e2.delete(0,tk.END)
    e3.delete(0,tk.END)
    e4.delete(0,tk.END)
    e5.delete(0,tk.END)
    e6.delete(0,tk.END)
    e7.delete(0,tk.END)
    q='''update inventory1
         set type='{}',name='{}',quantity={},costprice ={},saleprice={},sold={}
         where sno={};'''.format(typ,nm,qty,cp,sp,sld,sno)
    cursor.execute(q)
    con.commit()



   
   
   
def deleterec():
    rec=e1.get()
    e1.delete(0,tk.END)
    if int(rec) in l:
        d='''delete from inventory1
        where sno={};'''.format(rec)
        cursor.execute(d)
        con.commit()
    else:
       tkinter.messagebox.showinfo('Error','Entered sno. not in inventory')


def clearfields():
    e1.delete(0,tk.END)
    e2.delete(0,tk.END)
    e3.delete(0,tk.END)
    e4.delete(0,tk.END)
    e5.delete(0,tk.END)
    e6.delete(0,tk.END)
    e7.delete(0,tk.END)
clrbutn=tk.Button(root,text='Clear all entry fields',bg='orange',command=clearfields)
clrbutn.grid(row=0,column=3)



def bill():
    top=tk.Toplevel()
    top.geometry("1000x700")
    top.title('Billing')
   
    left=tk.Frame(top,width=500,height=768,bg='white')
    left.grid(row=0,column=0,columnspan=4,rowspan=12)
   
    right=tk.Frame(top,width=500,height=768,bg='lightblue')
    right.grid(row=0,column=5,columnspan=4,rowspan=12)
   
    heading=tk.Label(top,text='PERSONA STORE',font=('Arial 15 bold'),bg='white')
    heading.grid(row=0,column=1,columnspan=2)
   
    pr=tk.Label(top,text='Products',font=('Arial 15 bold'),bg='lightblue',fg='white')
    pr.grid(row=0,column=6)
   
    qt=tk.Label(top,text='Quantity',font=('Arial 15 bold'),bg='lightblue',fg='white')
    qt.grid(row=0,column=7)
   
    amt=tk.Label(top,text='Amount',font=('Arial 15 bold'),bg='lightblue',fg='white')
    amt.grid(row=0,column=8)
   
    ensno=tk.Label(top,text='Enter sno',font=('Arial 15 bold'),bg='white')
    ensno.grid(row=1,column=0)
   
    ensnoe=tk.Entry(top,width=25)
    ensnoe.grid(row=1,column=1)
    ensnoe.focus()
   
   
    prname=tk.Label(top,text='',font=('Arial 15 bold'),bg='white')
    prname.grid(row=3,column=0)
   
    pprice=tk.Label(top,text='',font=('Arial 15 bold'),bg='white')
    pprice.grid(row=4,column=0)
   
    def ajax():
        a=int(ensnoe.get())
       
        qry1='''select sno from inventory1'''
        cursor.execute(qry1)
        er=cursor.fetchall()
        #print(er)
        sn=[]
        for i in er:
            sn.append(i[0])
       # print(sn)
        if a not in sn:
            tkinter.messagebox.showinfo('Error','Invalid Serial No.')
        else:
            print('Search button working')
       
           
           
        t=()
        t+=(a,)
        print(t)
        qry='''select name,saleprice
        from inventory1 where sno={};'''.format(a)
        #getsno=ensnoe.get()
        cursor.execute(qry)
        re2=cursor.fetchall()
       
       
        print(re2)
        for r in re2:
            getnm=r[0]
            getprice=r[1]
        prname.configure(text='product name:'+str(getnm))
        pprice.configure(text='Price'+str(getprice))
       
        qtyl=tk.Label(top,text='Enter qty:',font=('Arial 15 bold'),bg='white')
        qtyl.grid(row=5,column=0)
       
        qtye=tk.Entry(top,text='Enter qty:',font=('Arial 15 bold'),bg='white')
        qtye.grid(row=5,column=1)
        qtye.focus()
       
       
       
        changel=tk.Label(top,text='Given Amount:',font=('Arial 15 bold'),bg='white')
        changel.grid(row=8,column=0)
       
        changee=tk.Entry(top,width=15)
        changee.grid(row=8,column=1)
       
       
       
        billbtn=tk.Button(top,text='Generate bill',width=20,height=2,bg='orange')
        billbtn.grid(row=11,column=1)
       
        def finorder():
            qtyreq=int(qtye.get())
            pdid=ensnoe.get()
           
            qry='''select quantity from inventory1 where sno={}'''.format(pdid)
            cursor.execute(qry)
            d=cursor.fetchall()
            #print(d[0][0 ])
            qtyinstock=int(d[0][0])
            if qtyinstock<qtyreq:
                tkinter.messagebox.showinfo('Error','Not enough item in stock.')
           
            else:
               
                finalprice=float(qtyreq)*float(getprice)
                if pdid in pdidlist:
                    tkinter.messagebox.showinfo('Error','Item is already added')
                else:
                   
                    pdlist.append(getnm)
                    pdqtylist.append(qtyreq)
                    pdpricelist.append(finalprice)
                    pdidlist.append(pdid)
                    print(pdlist)
                    print(pdqtylist)
                    print(pdpricelist)
                    count=0
               
                    for p in pdlist:
                        count+=1
                        tempname=tk.Label(top,text=str(p),font=('arial 15 bold'),bg='lightblue',fg='white')
                        tempname.grid(row=0+count,column=6)
                    count=0
                    for p in pdqtylist:
                        count+=1
                        tempname=tk.Label(top,text=str(p),font=('arial 15 bold'),bg='lightblue',fg='white')
                        tempname.grid(row=0+count,column=7)
                    count=0
                    for p in pdpricelist:
                        count+=1
                        tempname=tk.Label(top,text=str(p),font=('arial 15 bold'),bg='lightblue',fg='white')
                        tempname.grid(row=0+count,column=8)
                    totprice=sum(pdpricelist)
                    totallabel=tk.Label(top,text='Total:'+str(totprice),bg='lightblue',font=('arial 15 bold'),fg='white')
                    totallabel.grid(row=10,column=8)  
                    def change():
                        givenamt=changee.get()
                        if float(givenamt)<totprice:
                            tkinter.messagebox.showinfo('Error','Amount received is less than price')
                        else:
                            change=float(givenamt)-totprice
                            changecal=tk.Label(top,text='Change:'+str(change),bg='lightblue',fg='white',font=('Arial 15 bold'))
                            changecal.grid(row=10,column=7)
                   
               
           
            changebtn=tk.Button(top,text='Calculate change',width=15,height=2,bg='orange',command=change)
            changebtn.grid(row=9,column=1)
        buybtn=tk.Button(top,text='Add to cart',width=15,height=2,bg='orange',command=finorder)
        buybtn.grid(row=7,column=1)
       
    totallabel=tk.Label(top,text='',bg='lightblue',font=('arial 15 bold'),fg='white')
    totallabel.grid(row=10,column=6)    
    searchbtn=tk.Button(top,text='Search',width=15,height=1,bg='orange',command=ajax)
    searchbtn.grid(row=2,column=1)

   

       
   
cursor.execute('select*from inventory1;')
dis=cursor.fetchall()
   




e1=tk.Entry(root,width=50)
e1.grid(row=0,column=1)

e2=tk.Entry(root,text='Enter pr type',width=50)
e2.grid(row=2,column=1)

e3=tk.Entry(root,text='Enter pr name',width=50)
e3.grid(row=4,column=1)

e4=tk.Entry(root,text='Enter qty',width=50)
e4.grid(row=6,column=1)

e5=tk.Entry(root,text='Enter costprice',width=50)
e5.grid(row=8,column=1)

e6=tk.Entry(root,text='Enter saleprice',width=50)
e6.grid(row=10,column=1)

e7=tk.Entry(root,text='Enter qty sold',width=50)
e7.grid(row=12,column=1)




e1lab=tk.Label(root,text='Enter sno:',bg='white',fg='black')
e1lab.grid(row=0,column=0)

e2lab=tk.Label(root,text='Enter pr type:',bg='white',fg='black')
e2lab.grid(row=2,column=0)

e3lab=tk.Label(root,text='Enter pr name :',bg='white',fg='black')
e3lab.grid(row=4,column=0)

e4lab=tk.Label(root,text='Enter qty',bg='white',fg='black')
e4lab.grid(row=6,column=0)

e5lab=tk.Label(root,text='Enter cost price:',bg='white',fg='black')
e5lab.grid(row=8,column=0)

e6lab=tk.Label(root,text='Enter sale price:',bg='white',fg='black')
e6lab.grid(row=10,column=0)

e7lab=tk.Label(root,text='Enter qty sold:',bg='white',fg='black')
e7lab.grid(row=12,column=0)




mybutton=tk.Button(root,text='Click me to display items',state='active',command=display,bg='orange')
mybutton.grid(row=14,column=1)

mybutton2=tk.Button(root,text='Click after entering sno to delete record',state='active',command=deleterec,bg='orange')
mybutton2.grid(row=14,column=3)

mybutton1=tk.Button(root,text='Click to add new items',state='active',command=add,bg='orange')
mybutton1.grid(row=14,column=0)

mygraphbtn=tk.Button(text='Click to see the performance graph',command=graph,bg='orange')
mygraphbtn.grid(row=16,column=3)

mybutton3=tk.Button(root,text='Click to update the data for entered sno.',command=update,bg='orange')
mybutton3.grid(row=16,column=0)

mybutton4=tk.Button(root,text='Click to generate a bill',bg='orange',command=bill)
mybutton4.grid(row=16,column=1)



root.mainloop()
con.close()