from tkinter import *
import re
import platform
if platform.system()=='Windows':
    windows=True
else :
    windows=False

if windows:
        import py_win_keyboard_layout

def deNoise(text):
    noise = re.compile("""   َ    | # Fatha
                             ً    | # Tanwin Fath
                             ُ    | # Damma
                             ٌ    | # Tanwin Damm
                             ِ    | # Kasra
                             ٍ    | # Tanwin Kasr
                             ْ    | # Sukun
                             ـ     # Tatwil/Kashida
                         """, re.VERBOSE)
    text = re.sub(noise, '', text)
    return text


def callback():
    writesyn=False
    newsyn=False
    categoria=var.get()
    arabic=re.sub(' +',' ',entry_arab.get().strip())
    first_less=deNoise(arabic)
    if len(arabic.split(":"))==1:
        arabic+=":-"
    else:
        arabic=arabic.split(":")[0].strip()+":"+arabic.split(":")[1].strip()
    arabic_less=deNoise(arabic)
    trad=entry_french.get()
    inserzione=number.get()
    if len(categoria)==0 or len(arabic)==0 or len(trad)==0 or len(inserzione)==0:
        print('Error: Some Entries were not filled')
        return;
#    if not inserzione.isdigit():
 #       print('Error: The entry "Inserzione numero:" can only accept numbers')
 #       return;
    arab_encoded=arabic.encode('utf-8')
    less_encoded=arabic_less.encode('utf-8')
    space=':'.encode('utf-8')
    synonyms=0
    synlist=[]
    trad=re.sub(" +"," ",trad)
    trad=trad.replace(" ,",",")
    trad=trad.replace(", ",",")
    all_trads=[]
    with open('synonyms.txt','ba') as synfile:
        print()
    with open('synonyms.txt','br') as synfile:
        everysyn=synfile.readlines()
        for i in range(len(everysyn)):
            newline=everysyn[i]
            fullist=newline.decode().split(":")
            for new_trad in trad.split(","):
                all_trads.append(new_trad)
                if new_trad==fullist[0]:
                    writesyn=True
                    everysyn[i]=newline+space+first_less.encode('utf-8')
    if writesyn:
        with open('synonyms.txt','bw') as synwrite:
            synwrite.writelines(everysyn)

    with open('dictionary.txt','rb') as fichier:
        lines=fichier.readlines()
    for newline in lines:
        fullist=newline.decode().split(":")
        for new_trad in trad.split(","):
            not_new=False
            for other_trad in fullist[4].split(","):
                for one_trad in all_trads:
                    if new_trad==one_trad:
                        not_new=True
                if new_trad==other_trad and not not_new:
                    with open('synonyms.txt','br') as synfile:
                        everysyn=synfile.readlines()
                    with open('synonyms.txt','ab') as fichier:
                        print(len(everysyn))
                        if len(everysyn)!=0:

                            fichier.write('\n'.encode('utf-8'))
                        string=new_trad.encode('utf-8')+space+fullist[2].encode('utf-8')+space+arabic_less.split(":")[0].encode('utf-8')
                        fichier.write(string)

    with open('dictionary.txt','ab') as fichier:
        fichier.write(arab_encoded)
        fichier.write(space)
        fichier.write(less_encoded)
    with open('dictionary.txt','a') as fichier:
        endstr=':'+trad+':'+categoria+':'+inserzione+'\n'
        fichier.write(endstr)
    entry_arab.delete(0,50)
    entry_french.delete(0,50)

    read_last()


def arab():
    py_win_keyboard_layout.change_foreground_window_keyboard_layout(-255851519)
    return False
def french():
    py_win_keyboard_layout.change_foreground_window_keyboard_layout(layout)
    return False

def exiting():
    py_win_keyboard_layout.change_foreground_window_keyboard_layout(layout)
    master.destroy()

def clear():
    file=open('dictionary.txt','w')
    file.close()
    file=open('synonyms.txt','w')
    file.close()
    hide()

def show():
    pop_up.deiconify()

def hide():
    pop_up.withdraw()


def last_line():
    with open('dictionary.txt','rb') as fichier:
        liste=fichier.readlines()
        longueur=len(liste)
        if longueur:
            deleted=liste[longueur-1].decode()
            del liste[longueur-1]
    with open('dictionary.txt','wb') as fichier:
        fichier.writelines(liste)

    with open('synonyms.txt','rb') as fichier:
        del_list=deleted.split(":")
        syn1=fichier.readlines()
        syn=syn1
        i=0
        for lines in syn:
            line=lines.decode().split(":")
            it_trad=deleted.split(":")[4].split(",")
            for trad in it_trad:
                if trad==line[0]:
                    if len(line)<4:
                        del syn1[i]
                    else:
                        del line[len(line)-1]
                        result=":".join(line)
                        syn1[i]=result.encode("utf-8")
            i+=1
    with open('synonyms.txt','wb') as fichier:
        fichier.writelines(syn1)

    read_last()

def call(event):
    callback()
    entry_arab.focus_set()

def read_last():
    with open('dictionary.txt','rb') as fichier:
        liste=fichier.readlines()
        longueur=len(liste)
        if longueur:
            string=""
            string+=liste[longueur-3].decode()+liste[longueur-2].decode()+liste[longueur-1].decode()
            previous1['state']="normal"
            previous1.delete("0.0","end")
            previous1.insert('end',string)
            previous1['state']="disabled"
            #var_pre2.set(liste[longueur-2])
            #var_pre3.set(liste[longueur-1])

category=('Verbo', 'Nome', 'Aggettivo', 'Avverbio');
master = Tk()
master.option_add("*Font","Calibri 22")
var = StringVar()

entry_arab = Entry(master,validate='focusin')
entry_arab.grid(row=2,column=0,padx=10,pady=10)


entry_french=Entry(master,validate='focusin')
entry_french.grid(row=2,column=1,padx=10,pady=10)

presentation=Label(master,text='Scrivere qua tutte le informazioni sulla parola :')
presentation.grid(row=0,column=0,columnspan=4,padx=10,pady=10)

arabo=Label(master,text='Arabo :')
arabo.grid(row=1,column=0,padx=10,pady=10)

ita=Label(master,text='Italiano :')
ita.grid(row=1,column=1,padx=10,pady=10)

grammatica=Spinbox(master,values=('Verbo','Nome','Aggettivo','Avverbio'),textvariable=var,state='readonly',wrap=True)
grammatica.grid(row=4,column=0,padx=10,pady=10)
gramm=Label(master,text='Categoria grammaticale')
gramm.grid(row=3,column=0,padx=10,pady=10)
number=StringVar()
numero_en=Spinbox(master,increment=1,from_=1,to=1000,textvariable=number,state='readonly')
numero_en.grid(row=4,column=1,padx=10,pady=10)
insert=Label(master,text="Numero d'inserzione :")
insert.grid(row=3,column=1,padx=10,pady=10)
okay = Button(master, text="Okay", width=10, command=callback)
okay.grid(row=5,column=1,padx=10,pady=10)

empty=Button(master,text='Empty',command=show)
empty.grid(row=5,column=0,padx=10,pady=10)

pop_up=Toplevel()

warning=Label(pop_up,text='The file <dictionary.txt> is going to be cleared',fg='red')
warning.grid(row=0,column=0,columnspan=2,padx=10,pady=10)
clear_but=Button(pop_up,text='Okay',command=clear,bg='red')
clear_but.grid(row=1,column=1,padx=10,pady=10)

back=Button(pop_up,text='Cancel',command=hide)
back.grid(row=1,column=0,padx=10,pady=10)
hide()

var_pre1=StringVar()
#var_pre2=StringVar()
#var_pre3=StringVar()
previous1=Text(master,width=30,height=3,wrap='word')
#previous2=Label(master,textvariable=var_pre2)
#previous3=Label(master,textvariable=var_pre3)
previous1.grid(row=6,column=0,columnspan=2,padx=10,pady=10)
#previous2.grid(row=7,column=0,columnspan=2)
#previous3.grid(row=8,column=0,columnspan=2)

read_last()

remove=Button(master,text='Remove',command=last_line)
remove.grid(row=5,column=0,columnspan=2,padx=10,pady=10)

master.bind("<Return>",call)
entry_arab.focus_set()
if windows:
    print('ok')
    layout=py_win_keyboard_layout.get_foreground_window_keyboard_layout()
    master.protocol("WM_DELETE_WINDOW",exiting)
    entry_arab['validatecommand']=arab
    entry_french['validatecommand']=french

master.mainloop()

