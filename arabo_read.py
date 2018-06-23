from tkinter import *
import platform
if platform.system()=='Windows':
    windows=True
else :
    windows=False
print(windows)    
from random import randint
if windows:
        import py_win_keyboard_layout

with open('dictionary.txt','rb') as fichier:
    print(fichier.read())


fen=Tk()
fen.option_add("*Font","Calibri 22")
valid_list=[]
syn_list=[]
rand=0
lang=0
trad=0
def disable_inserzione():
    if state_inserzione.get()==0:
        which_inserzione['state']='disabled';
    else:
        which_inserzione['state']='readonly';

def search():
    
    global valid_list,rand,lang,trad
    valid_list=[]
    
    with open('dictionary.txt','rb') as fichier:
        
        for newline in fichier.readlines():
            newlist=newline.decode().split()
            if categoria_var.get()=='Tutto' or categoria_var.get()==newlist[3]:
                if state_inserzione.get()==0 or inserzione_var.get()==newlist[4]:
                    valid_list.append(newlist)


    if valid_list==[]:
        print('There is no matching word in the dictionary file')
        return
    start_quiz()


def lez_search():
    global valid_list
    labels=[]
    valid_list=[]
    i=0
    with open('dictionary.txt','rb') as fichier:
        for newline in fichier.readlines() :
            listed=newline.decode().split()
            if listed[4]==lezione_var.get() and i<=int(wordnumber_var.get()):
                i+=1
                valid_list.append(listed)
    definitions=str()
    message=Text(lezione,width=30,height=10)
    for i in range(len(valid_list)):
        #insert((i+1).0,valid_list[i][2])
        #insert((i+1).(30-len(valid_list[i][0])),valid_list[i][0])
        tradu=valid_list[i][2]+'     =     '+valid_list[i][0]+'\n'
        definitions+=tradu

    start_lezione()
    message.insert(2.10,definitions)
    message['state']='disabled'
    message.grid(row=0,column=0,padx=10,pady=10)
    scroll=Scrollbar(lezione,orient='vertical',command=message.yview)
    scroll.grid(row=0,column=1,sticky='ns')
    message['yscrollcommand']=scroll.set

def trans(event):
    translate()

def newword():
    global valid_list, rand,lang,trad,syn_list
    entry_trad.delete(0,20)    
    length=len(valid_list)-1
    rand=randint(0,length)

    string= '"'+valid_list[rand][lang]+'"' + " : "
    trad_var.set(string)
    syn_list=[]
    if lingua_var.get()=="Italiano":
        with open('synonyms.txt','rb') as fichier:
            for newline in fichier.readlines():
                print(newline)
                fullist=newline.split()
                print(fullist[0].decode())
                print(valid_list[rand][2])
                if fullist[0].decode()==valid_list[rand][2]:
                    for i in range(len(fullist)-1):
                        syn_list.append(fullist[i+1])
    
def translate():
    global valid_list, rand,lang,trad,syn_list

    if entry_var.get()=="":
        info['fg']='black'
        info_var.set('Il campo è vuoto')
        return
    
    if entry_var.get()==valid_list[rand][trad]:
        info_var.set('Bravo!')
        info['fg']='green'

    else:
        for synonyme in syn_list:
            if entry_var.get()==synonyme.decode():
                info_var.set('Un sinonimo?')
                info['fg']='orange'
                entry_trad.delete(0,20)
                return
    
    if entry_var.get()!=valid_list[rand][trad]:
        info_var.set('Riprova!')
        info['fg']='red'
        entry_trad.delete(0,20)
        return

    newword()

def start_quiz():
    global rand,lang,trad
    menu.grid_remove()
    para.grid_remove()
    lezione.grid_remove()
    cadre.grid()
    entry_trad.bind("<Return>",trans)
    entry_trad.focus_set()
    if windows:
        if lingua_var.get()=="Italiano":
            arab()
            lang=2
            trad=1
        else:
            french()
            lang=0
            trad=2
    newword()

            
def start_para():
    menu.grid_remove()
    cadre.grid_remove()
    para.grid(row=0,column=0,padx=50,pady=50)

def start_menu():
    cadre.grid_remove()
    para.grid_remove()
    lezione_par.grid_remove()
    lezione.grid_remove()
    menu.grid(padx=50,pady=50)

def start_parlezione():
    menu.grid_remove()
    lezione_par.grid(padx=50,pady=50)

def start_lezione():
    lezione_par.grid_remove()
    lezione.grid()
    
def get_solution():
    global rand,valid_list,trad
    entry_var.set(valid_list[rand][trad])

def arab():
    py_win_keyboard_layout.change_foreground_window_keyboard_layout(-255851519)
    return False
def french():
    py_win_keyboard_layout.change_foreground_window_keyboard_layout(layout)
    return False

def exiting():
    py_win_keyboard_layout.change_foreground_window_keyboard_layout(layout)
    fen.destroy()
    
def disable_wordnumber():
    if state_wordnumber.get()==0:
        which_wordnumber['state']='disabled';
    else:
        which_wordnumber['state']='readonly';

fen.rowconfigure(0,minsize=800)
fen.columnconfigure(0,minsize=1000)

menu=LabelFrame(fen,text='Menu')
menu.grid(row=0,column=0)

lezione_but=Button(menu,text='Lezione',command=start_parlezione)
lezione_but.grid(column=0,row=1,padx=50,pady=50)

quiz=Button(menu,text='Quiz',command=start_para)
quiz.grid(column=0,row=0,padx=50,pady=50)

but_quit=Button(menu,text='Uscire',command=exiting)
but_quit.grid(column=0,row=2,padx=50,pady=50)

para=LabelFrame(fen,text='Parametri')


lezione_par=LabelFrame(fen,text='Parametri')

lez_insert=Label(lezione_par,text="Lezione numero :")
lez_insert.grid(padx=10,pady=10,row=0,column=0)
lezione_var=StringVar()
which_lezione=Spinbox(lezione_par,increment=1,from_=1,to=1000,textvariable=lezione_var,state='readonly')
which_lezione.grid(padx=10,pady=10,row=1,column=0,columnspan=1)

state_wordnumber=IntVar()
word_number=Checkbutton(lezione_par,text="Numero di parole :",variable=state_wordnumber,command=disable_wordnumber)
word_number.grid(row=0,column=1)
wordnumber_var=StringVar()
which_wordnumber=Spinbox(lezione_par,increment=1,state='disabled',from_=10,to=1000,textvariable=wordnumber_var)
which_wordnumber.grid(row=1,column=1)

okay_lez=Button(lezione_par,text='Okay',command=lez_search)
okay_lez.grid(row=2,column=1)

backmenu_lez=Button(lezione_par,text='Menu',command=start_menu)
backmenu_lez.grid(row=2,column=0)
lezione=LabelFrame(fen,text='Lezione')


quiz_lez=Button(lezione,text='Quiz',command=start_quiz)
quiz_lez.grid(row=0,column=2,padx=10,pady=10)

cadre=LabelFrame(fen,text='Quiz')
cadre.columnconfigure(1,minsize=300)


lingua=Label(para,text="Lingua iniziale :")
lingua.grid(padx=10,pady=10,row=0,column=0)
lingua_var=StringVar()
which_lingua=Spinbox(para,values=("Italiano","Arabo"),textvariable=lingua_var,state='readonly',wrap=True)
which_lingua.grid(padx=10,pady=10,row=1,column=0)

categoria=Label(para,text='Categoria grammaticale :')
categoria.grid(padx=10,pady=10,row=0,column=1)
categoria_var=StringVar()
which_categoria=Spinbox(para,values=('Tutto','Verbo','Nome','Aggettivo','Avverbio'),textvariable=categoria_var,state='readonly',wrap=True)
which_categoria.grid(padx=10,pady=10,row=1,column=1)

state_inserzione=IntVar()
inserzione=Checkbutton(para,text="Scegliete un'inserzione",variable=state_inserzione,command=disable_inserzione)
inserzione.grid(padx=10,pady=10,row=2,column=0,columnspan=2)
inserzione_var=StringVar()
which_inserzione=Spinbox(para,increment=1,from_=1,to=1000,textvariable=inserzione_var,state='disabled')
which_inserzione.grid(padx=10,pady=10,row=3,column=0,columnspan=2)

okay=Button(para,text='Okay',command=search)
okay.grid(padx=50,pady=50,column=1,row=4)

anuller=Button(para,text='Menu',command=start_menu)
anuller.grid(padx=50,pady=50,column=0,row=4)

start=Button(cadre,command=translate,text='Continuare')
start.grid(padx=30,pady=30,column=2,row=7)


solution=Button(cadre,text='Soluzione',command=get_solution)
solution.grid(padx=30,pady=30,column=2,row=6)
info_var=StringVar()
info=Label(cadre,textvariable=info_var)
info.grid(padx=30,pady=30,row=6,column=1)
info_var.set('Traduzione?')           
trad_var=StringVar()
traduction=Label(cadre,textvariable=trad_var)
traduction.grid(padx=30,pady=30,column=0,columnspan=3,row=4)

entry_var=StringVar()
entry_trad=Entry(cadre,textvariable=entry_var)
entry_trad.grid(padx=30,pady=30,row=5,column=0,columnspan=3)

para_back=Button(cadre,text='Parametri',command=start_quiz)
para_back.grid(padx=30,pady=30,row=6,column=0)

menu_back=Button(cadre,text='Menu',command=start_menu)
menu_back.grid(padx=30,pady=30,row=7,column=0)

if windows:
    fen.protocol("WM_DELETE_WINDOW",exiting)
    layout=py_win_keyboard_layout.get_foreground_window_keyboard_layout()

fen.mainloop()
