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
            newlist=newline.decode().split(":")
            if categoria_var.get()=='Tutto' or categoria_var.get()==newlist[5]:
                if state_inserzione.get()==0 or inserzione_var.get()==newlist[6]:
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
            listed=newline.decode().split(':')

            if int(listed[6])==int(lezione_var.get()) and (i<=int(wordnumber_var.get()) or  state_wordnumber.get()==0):

                if state_wordnumber.get()!=0:
                    i+=1
                valid_list.append(listed)
    definitions=str()
    message=Text(lezione,width=10,height=10,wrap='word')
    string=''
    spaces=' '
    longue=0
    for i in range(len(valid_list)):



        #insert((i+1).0,valid_list[i][2])
        #insert((i+1).(30-len(valid_list[i][0])),valid_list[i][0])
        spaces=' '*(50-len(valid_list[i][4])-len(valid_list[i][0]))
        tradu=valid_list[i][4]+'    =    '+valid_list[i][0]
        string=str(i+1)+'.0'
        #message.insert(string,valid_list[i][4])
        string=str(i+1)+'.end'
        # message.insert('end',spaces)
        tradu=tradu.replace(",",", ")
        if len(tradu)>longue:
            longue=len(tradu)
            print(longue)
        message['width']=longue
        message.insert('end',tradu)

        definitions+=tradu
        #message.insert('end','\n')
    print(message['width'])
    start_lezione()
    i=2+0.10
    #message.insert(i,definitions)
    message['state']='disabled'
    message.grid(row=0,column=0,padx=10,pady=10)
    scroll=Scrollbar(lezione,orient='vertical',command=message.yview)
    scroll.grid(row=0,column=1,sticky='ns')
    message['yscrollcommand']=scroll.set

def trans(event):
    translate()

def newword():
    global valid_list, rand,lang,trad,syn_list
    entry_trad.delete(0,50)
    length=len(valid_list)-1
    rand=randint(0,length)

    string=""
    syn_list=[]
    if lingua_var.get()=="Italiano":

        string=valid_list[rand][4].replace(",",", ")
        with open('synonyms.txt','rb') as fichier:
            for newline in fichier.readlines():
                print(newline)
                fullist=newline.decode().split(':')
                print(fullist[0])
                print(valid_list[rand][4])
                for trads in valid_list[rand][4].split(","):
                    if fullist[0]==trads:
                        for i in range(len(fullist)-1):
                            syn_list.append(fullist[i+1])

    else:
        string+=valid_list[rand][lang]+" "+valid_list[rand][lang+1]
    trad_var.set(string)

def translate():
    global valid_list, rand,lang,trad,syn_list
    traduc=entry_var.get()
    if traduc=="":
        info['fg']='black'
        info_var.set('Il campo è vuoto')
        return
    if lingua_var.get()=="Arabo" and verify(traduc):
        info_var.set('Bravo!')
        info['fg']='green'

    elif len(traduc.split())==1 and verify(traduc):
        print("1")
        if valid_list[rand][1]=="-":
            info_var.set('Bravo!')
            info['fg']='green'
        else :
            print("2")
            if valid_list[rand][5]=="Nome":
                info_var.set('E il plurale?')
            elif valid_list[rand][5]=="Verbo":
                info_var.set('E il presente?')
            info['fg']='orange'
            return
    elif len(traduc.split())==2:
        if traduc.split()[0]==valid_list[rand][trad]:
            if traduc.split()[1]==valid_list[rand][3]:
                info_var.set('Bravo!')
                info['fg']='green'
            else :
                if valid_list[rand][5]=="Nome":
                    info_var.set('Il plurale\nè sbagliato')
                elif valid_list[rand][5]=="Verbo":
                    info_var.set('Il presente\nè sbagliato')
                entry_trad.delete(0,20)
                info['fg']='red'
                return
    elif syn_list:
        for synonyme in syn_list:
            if traduc.split()[0]==synonyme:
                info_var.set('Un sinonimo?')
                info['fg']='orange'
                entry_trad.delete(0,20)
                return

    elif traduc.split()[0]!=valid_list[rand][trad]:
        info_var.set('Riprova!')
        info['fg']='red'
        entry_trad.delete(0,20)
        return

    newword()

def verify(string):
    global rand, trad, valid_list
    for traduc in valid_list[rand][trad].split(","):
        print(string)
        print(traduc)
        if string==traduc:
            return True
    return False




def start_quiz():
    global rand,lang,trad
    menu.grid_remove()
    para.grid_remove()
    lezione.grid_remove()
    cadre.grid(padx=50,pady=50)
    entry_trad.bind("<Return>",trans)
    entry_trad.focus_set()
    if windows:
        if lingua_var.get()=="Italiano":
            arab()
            lang=4
            trad=2
        else:
            french()
            lang=0
            trad=4
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
    lezione.grid(padx=50,pady=50)

def get_solution():
    global rand,valid_list,trad
    string=valid_list[rand][trad]
    if valid_list[rand][3]!="-" and lingua_var.get()=="Italiano":
        string+=" "+valid_list[rand][3]
    entry_var.set(string)

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

#fen.rowconfigure(0,minsize=800)
#fen.columnconfigure(0,minsize=1000)

menu=LabelFrame(fen,text='Menu')
menu.grid(row=0,column=0,padx=50,pady=50)

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
info.grid(padx=30,pady=30,row=6,column=1,rowspan=2)
info_var.set('Traduzione?')
trad_var=StringVar()
traduction=Label(cadre,textvariable=trad_var)
traduction.grid(padx=30,pady=30,column=0,columnspan=3,row=4)

entry_var=StringVar()
entry_trad=Entry(cadre,textvariable=entry_var)
entry_trad.grid(padx=30,pady=30,row=5,column=0,columnspan=3)

para_back=Button(cadre,text='Parametri',command=start_para)
para_back.grid(padx=30,pady=30,row=6,column=0)

menu_back=Button(cadre,text='Menu',command=start_menu)
menu_back.grid(padx=30,pady=30,row=7,column=0)

if windows:
    fen.protocol("WM_DELETE_WINDOW",exiting)
    layout=py_win_keyboard_layout.get_foreground_window_keyboard_layout()

fen.mainloop()


