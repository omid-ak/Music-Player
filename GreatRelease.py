import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
import pygame
from pygame import *
import os
import time


#******************App Frame Configurations*******************
Main_Window=Tk()
Main_Window.geometry('800x500')
Main_Window.title('Musicly')
Main_Window.resizable(False,False)
Main_Panel=Frame(bd=2,relief="groove")
Main_Panel.place(x=190,y=75,height=400,width=580)
#*************************************************************
#******************Canvas OF Panel****************************
canvas=Canvas(Main_Window,bg="#000000",width=800,height=500)
canvas.pack()
Main_Panel=Frame(bd=2,bg="#b3b3b3",relief="groove")
Main_Panel.place(x=190,y=10,height=400,width=580)
#..............................................................












#************************Controller Variables***********************************

Playlist_Require_Directory_Addr=StringVar() ####Directory Container For Add Playlist
Add_Music_dir=StringVar() ##Directory Container For Add Music
List_Of_Music_dir="" ##This Lists Our Available Musics In Directory Above

##These Vars Are For Controlling Current Frames and List Just To Make Playing Songs Easier............................................
Current_Frame_in_MainPanel_Name=""
Current_Frame_in_MainPanel_Controller= ""
Current_List_To_Play=""

List_Of_My_Music_GeneralMusic="" #When Click General Music , You See A List Containing Your Musics
List_Of_Playlist_Music=""

##These Vars Control the Frames In Edit Frame
List_Of_Playlist_Names_Edit= ""
Entry_Playlist_Name=""
Rename_Playlist_Name_Edit_Frame= ""
delete_btn_Edit_Frame=""


List_Of_Playlist_Names_Queue_AddPl= "" ##A List Containing Existing Playlist Names Ready To Modify
queue_give_playlist_frame=""##For switching between comboboxx options PlayQueue
queue_give_database_frame=""##For switching between comboboxx options PlayQueue

Playlist_frame="" #This Frame Is Containing Existing Playlist Which Are Load In This Frame

Player_Btns_Controller=1 ##Controlling Switching Pause And Resume





#***************Creating DataBase Files When App Starts *****************
DataBase_File_AddMusic= '/home/omid/Music/Database_AddMusic.csv'
DataBase_File_Playlist='/home/omid/Music/Database_Playlist.csv'
Database_File_Queue='/home/omid/Music/Database_Queue.csv'
if not os.path.isfile(Database_File_Queue):
    file=open(Database_File_Queue, 'a')
    file.write(" , "+'\n')
    file.close()

if not os.path.isfile(DataBase_File_AddMusic):
    file=open(DataBase_File_AddMusic, 'a')
    file.write(" , "+'\n')
    file.close()

if not os.path.isfile(DataBase_File_Playlist):
    file=open(DataBase_File_Playlist, 'a')
    file.write(" , "+'\n')
    file.close()




#*****************************Program Classes******************
class StopWatch(Frame):
    def __init__(self, parent=None, **kw):
        Frame.__init__(self, parent, kw)
        self._start = 0.0
        self._elapsedtime = 0.0
        self._running = 0
        self.timestr = StringVar()
        self.makeWidgets()

    def makeWidgets(self):
        l = Label(self,bg="#FFFF00",textvariable=self.timestr,bd=2,relief="groove")
        self._setTime(self._elapsedtime)
        l.pack( pady=2, padx=2)

    def _update(self):
        self._elapsedtime = time.time() - self._start
        self._setTime(self._elapsedtime)
        self._timer = self.after(50, self._update)

    def _setTime(self, elap):
        minutes = int(elap/60)
        seconds = int(elap - minutes*60.0)
        hseconds = int((elap - minutes*60.0 - seconds)*100)
        self.timestr.set('%02d:%02d:%02d' % (minutes, seconds, hseconds))

    def Start(self):
        if not self._running:
            self._start = time.time() - self._elapsedtime
            self._update()
            self._running = 1

    def Stop(self):
        if self._running:
            self.after_cancel(self._timer)
            self._elapsedtime = time.time() - self._start
            self._setTime(self._elapsedtime)
            self._running = 0

    def Reset(self):
        self._start = time.time()
        self._elapsedtime = 0.0
        self._setTime(self._elapsedtime)
Timer_Object= "" #Controlling Timer Label

class Stack:
    def __init__(self):
        self.items=[]

    def push(self,e):
        self.items=self.items +[e]

    def pop(self):
        return self.items.pop()
General_Music_Stack=Stack() ##Stack For When You Want To Play Music in General Music Frame
Queue_Muisc_Stack=Stack() ##Stack For When You Want To Play Music in Play Queue Frame

class Queue:
    def __init__(self):
        self.items=[]

    def push(self,e):
        self.items.append(e)

    def pop(self):
        head=self.items[0]
        self.items=self.items[1:]
        return head
My_General_Queue_To_Play=Queue()
Queue_Play_For_GeneralMusic="" ##Queue For When You Want To Play Music in General Music Frame
Queue_Play_For_AppQueue="" ##Queue For When You Want To Play Music in Play Queue Frame

class Node_Playlist:
    def __init__(self,PLName):
        self.Playlist_name=PLName
        self.Nodes=[]

    def Addto_Playlist_Nodes(self, songname):
        self.Nodes.append(songname)

    def get_songs(self):
        return self.Nodes
Root_Playlist_Node=Node_Playlist("Root") ##Root Node of Tree,Which We Creat it Here To use When We Creat A New Playlist
New_Node_Of_Tree=""                      ##









#**************************************Main Functions*****************************************

def Close_App():
    answer=tkinter.messagebox.askquestion("Close","Are You Sure Of Exiting Program ?")
    if answer == "yes":
        Main_Window.destroy()

def Play_Music():
    global Timer_Object
    global General_Music_Stack
    global Queue_Muisc_Stack
    global Player_Btns_Controller
    global List_Of_My_Music_GeneralMusic
    global List_Of_Playlist_Music
    global Current_Frame_in_MainPanel_Controller
    global Current_Frame_in_MainPanel_Name
    global Current_List_To_Play
    global Queue_Play_For_GeneralMusic ##Raji Attitude
    global Queue_Play_For_AppQueue##Raji Attitude
    generalpath=""
    name_of_music=""
    if Current_Frame_in_MainPanel_Name=="General_Music_Panel":
        name_of_music=Current_List_To_Play.get('active')
        for item in Queue_Play_For_GeneralMusic.items:
            if (item.split('/'))[-1]==name_of_music:
                for i in range(0,((Queue_Play_For_GeneralMusic.items).copy()).index(item)):
                    head=(Queue_Play_For_GeneralMusic.pop())
                    General_Music_Stack.push(head)
                for i in (item.split('/'))[0:-1]:
                    generalpath=generalpath+i+"/"
                break
    elif Current_Frame_in_MainPanel_Name=="Play_Queue_Playtime_frame":
        name_of_music=Current_List_To_Play.get('active')
        for item in Queue_Play_For_AppQueue.items:
            if (item.split('/'))[-1]==name_of_music:
                for i in range(0,((Queue_Play_For_AppQueue.items).copy()).index(item)):
                    head=(Queue_Play_For_AppQueue.items).pop()
                    Queue_Muisc_Stack.push(head)
                for i in (item.split('/'))[0:-1]:
                    generalpath=generalpath+i+"/"
                break
    if Player_Btns_Controller!=0:
        pygame.mixer.init()
        pygame.mixer.music.load(generalpath+'/'+name_of_music)
        pygame.mixer.music.play()
        Timer_Object.Start()
    else:
        Resume_Music()

def Resume_Music():
    global Timer_Object
    global Player_Btns_Controller
    Player_Btns_Controller=1
    Timer_Object.Start()
    pygame.mixer.music.unpause()

def Pause_Music():
    global Timer_Object
    global Player_Btns_Controller
    pygame.mixer.music.pause()
    Timer_Object.Stop()

    Player_Btns_Controller=0

def Stop_Music():
    global Timer_Object
    Timer_Object.Stop()
    Timer_Object.Reset()
    pygame.mixer.music.stop()

def Increase_Volume():
    pygame.mixer.music.set_volume(pygame.mixer.music.get_volume()+0.28)

def Decrease_Volume():
    if   pygame.mixer.music.get_volume()<0.2:
        pygame.mixer.music.set_volume(0)
    pygame.mixer.music.set_volume(pygame.mixer.music.get_volume()-0.2)

def Next_Song():
    ##using 2 stack and 1 queue for looping around songs
    global Timer_Object
    global Queue_Play_For_AppQueue ##Raji Attitude
    global Queue_Play_For_GeneralMusic ##Raji Attitude
    global General_Music_Stack
    global Queue_Muisc_Stack

    global Current_List_To_Play
    global List_Of_My_Music_GeneralMusic
    global Current_Frame_in_MainPanel_Name
    Timer_Object.Stop()
    Timer_Object.Reset()
    ###this 2 variable is just for reducing number of codes for both main frame General Music and Queue Play Frame
    Which_Stack=""
    Which_Queue=""
    if Current_Frame_in_MainPanel_Name=="General_Music_Panel":
        Which_Stack=General_Music_Stack
        Which_Queue=Queue_Play_For_GeneralMusic
    elif Current_Frame_in_MainPanel_Name=="Play_Queue_Playtime_frame":
        Which_Stack=Queue_Muisc_Stack
        Which_Queue=Queue_Play_For_AppQueue

    current_index=0
    for i in range(0,Current_List_To_Play.size()):
        if Current_List_To_Play.get(i)==Current_List_To_Play.get('active'):
            current_index=i
    current_music=Current_List_To_Play.get('active')
    if current_index<Current_List_To_Play.size()-1:
        Current_List_To_Play.activate(current_index+1)
        for music in Which_Queue.items:
            if music.split('/')[-1] !=current_music:
                head=Which_Queue.pop()
                Which_Stack.push(head)
            else:
                head=Which_Queue.pop()
                Which_Stack.push(head)
                break

    elif current_index==Current_List_To_Play.size()-1:
        Current_List_To_Play.activate(0)
        temp_stack=Stack()
        Which_Stack.push(Which_Queue.pop())
        while len(Which_Stack.items) !=0:
            temp_stack.push(Which_Stack.pop())
        while len(temp_stack.items) !=0:
            Which_Queue.push(temp_stack.pop())

    pygame.mixer.stop()
    pygame.mixer.music.load((Which_Queue.items)[0])
    pygame.mixer.music.play()
    Timer_Object.Start()

def Previous_Music():
    global Timer_Object
    Timer_Object.Stop()
    Timer_Object.Reset()
    global Queue_Play_For_AppQueue ##Raji Attitude
    global Queue_Play_For_GeneralMusic ##Raji Attitude
    global General_Music_Stack
    global Queue_Muisc_Stack
    global Current_List_To_Play
    global Current_Frame_in_MainPanel_Name
    global List_Of_My_Music_GeneralMusic
    Which_Stack=""
    Which_Queue=""
    if Current_Frame_in_MainPanel_Name=="General_Music_Panel":
        Which_Stack=General_Music_Stack
        Which_Queue=Queue_Play_For_GeneralMusic
    elif Current_Frame_in_MainPanel_Name=="Play_Queue_Playtime_frame":
        Which_Stack=Queue_Muisc_Stack
        Which_Queue=Queue_Play_For_AppQueue

    curren_index=0
    for i in range(0,Current_List_To_Play.size()):
        if Current_List_To_Play.get(i)==Current_List_To_Play.get('active'):
            current_index=i
    current_music=Current_List_To_Play.get('active')
    if current_index==0:
        for i in range(0, len(Which_Queue.items) - 1):
            dele=Which_Queue.pop()
            Which_Stack.push(dele)
        Current_List_To_Play.activate(Current_List_To_Play.size()-1)
        for i in range(0, len(Which_Queue.items) - 1):
            head=Which_Queue.pop()
            Which_Queue.push(head)

    else:
        Current_List_To_Play.activate(current_index-1)
        current_size_for_pop=len(Which_Queue.items)
        head=Which_Stack.pop()
        Which_Queue.push(head)
        for i in range(0,current_size_for_pop):
            ele=Which_Queue.pop()
            Which_Queue.push(ele)

    pygame.mixer.init()
    pygame.mixer.music.load((Which_Queue.items)[0])
    pygame.mixer.music.play()
    Timer_Object.Start()


##Initialize List Of PlayLists,Reading Database File And Add PlayLits Names To Gui Playlist Frame
def Initialize_Playlist():
    global Playlist_frame
    name_btn=StringVar()
    database_playlist_file=open(DataBase_File_Playlist,'r')
    database_playlist_content=database_playlist_file.readlines()
    database_playlist_file.close()
    pl_names=[]
    for name in database_playlist_content:
        if  name!=' , \n' and '/' not in name:
            pl_names.append((((name[:-1]).split(','))[0]))
    for items in pl_names:
        lbl=tkinter.Label(Playlist_frame,text=items,width=130,bd=2,relief="groove")
        lbl.pack() ##Initialize List

##When Creat New PlayList,For Choose btn
def Ask_for_Directory_Playlist():
    global Playlist_Require_Directory_Addr
    global Entry_Playlist_Name
    global List_Of_Playlist_Music
    global New_Node_Of_Tree
    directory=filedialog.askdirectory()
    Playlist_Require_Directory_Addr.set(directory)
    label_dir=Label(Main_Panel, bd=2, relief="groove", textvariable=Playlist_Require_Directory_Addr)
    label_dir.place(x=22,y=100,width=300,height=40)
    for root, dirs, files in os.walk(Playlist_Require_Directory_Addr.get()):
        for filename in files :
            if filename.endswith("mp3"):
                List_Of_Playlist_Music.insert(END,filename)

    Save_Node_btn=Button(Main_Panel,text="Save Playlist For Me",command=Save_New_Playlist)
    Save_Node_btn.place(width=180, height=25, x=350, y=315)

##When Creat New Playlist We Add Or Remove Songs To A Tree Structure Before We Really Save
def Add_Muisc_To_Tree_Before_saving_Playlist():
    global Playlist_Require_Directory_Addr
    global List_Of_Playlist_Music
    global Entry_Playlist_Name
    global Root_Playlist_Node
    global New_Node_Of_Tree
    if Entry_Playlist_Name.get()!="" and  Playlist_Require_Directory_Addr!="":
        messagebox.showinfo("Success","''"+List_Of_Playlist_Music.get('active')+"'' Was Added Successfully")
        New_Node_Of_Tree.Addto_Playlist_Nodes(Playlist_Require_Directory_Addr.get()+'/'+List_Of_Playlist_Music.get('active'))

## In Edit Frame We Can Delete Songs Of a Playlist
def Delete_Playlist_Song_Edit():
    global List_Of_Playlist_Names_Edit
    global List_Of_Selected_Playlist

    if List_Of_Playlist_Names_Edit.get(0)=="Empty":
        messagebox.showerror("Error","No Playlist To Delete Song From")
    else:

        Delete_song=Tk()
        Delete_song.geometry('500x300')
        Delete_song.resizable(False,False)
        Delete_song.title("PlayList  "+List_Of_Playlist_Names_Edit.get('active'))
        List_Of_Selected_Playlist=Listbox(Delete_song)
        List_Of_Selected_Playlist.place(x=10,y=20,width=360,height=250)
        Remove_Song_btn=Button(Delete_song,text="Remove Song")
        Remove_Song_btn.place(x=390,y=30,width=100,height=22)
        database_file=open(DataBase_File_Playlist,'r')
        database_file_Playlist_content=database_file.readlines()
        database_file.close()
        for name in database_file_Playlist_content.copy():
            if name!=" , \n":
                if '/' not in (((name[:-1]).split(','))[0])and (((name[:-1]).split(','))[0])==List_Of_Playlist_Names_Edit.get('active'):
                    for i in range(database_file_Playlist_content.index(name)+1,database_file_Playlist_content.index(name)+1+int((((name[:-1]).split(','))[1]))):
                        List_Of_Selected_Playlist.insert(END,(((database_file_Playlist_content[i])[:-1]).split('/'))[-1])


        def Delete_Playlist_song():
            if List_Of_Selected_Playlist.get(0)=="Empty":
                messagebox.showerror("Error","No Music For Deleting")
            else:
                print(List_Of_Selected_Playlist.size())
                answer=messagebox.askyesno("Deleting","Deleting "+"''"+List_Of_Selected_Playlist.get('active')+"''??")
                if answer:
                    for i in range(0,List_Of_Selected_Playlist.size()):
                        if List_Of_Selected_Playlist.get(i)==List_Of_Selected_Playlist.get('active'):
                            content_to_delete=List_Of_Selected_Playlist.get(i)
                            List_Of_Selected_Playlist.delete(i)#changing veiw in listbox

                            for name in database_file_Playlist_content.copy():
                                if name!=" , \n":
                                    if '/' not in (((name[:-1]).split(','))[0]) and (((name[:-1]).split(','))[0])==List_Of_Playlist_Names_Edit.get('active'):
                                        Number_Of_Music_To_Delete=((((name[:-1]).split(','))[1]))
                                        index_Playlist_To_Delete=(database_file_Playlist_content.index(name))
                                        database_file_Playlist_content[database_file_Playlist_content.index(name)]=(((name[:-1]).split(','))[0])+","+str(int((((name[:-1]).split(','))[1]))-1)+'\n'
                                        for i in range(index_Playlist_To_Delete+1,index_Playlist_To_Delete+1+int(Number_Of_Music_To_Delete)):
                                            if ((((database_file_Playlist_content[i])[:-1]).split('/'))[-1])==content_to_delete:

                                                del database_file_Playlist_content[i]



                    database_file=open(DataBase_File_Playlist,'w')
                    for i in database_file_Playlist_content:
                        database_file.write(i)
                    database_file.close()





        Remove_Song_btn=Button(Delete_song,text="Remove Song",command=Delete_Playlist_song)
        Remove_Song_btn.place(x=390,y=30,width=100,height=22)



        Delete_song.mainloop()

##When We Creat A Playlist We Can See List Of Our Current Music in Node Of Tree SO Then We Can Remove Them
def Show_Playlist_New_Node():
    global New_Node_Of_Tree
    Show_Playlist=Tk()
    Show_Playlist.geometry('500x300')
    Show_Playlist.resizable(False,False)
    Show_Playlist.title("New PlayList Songs")
    List_Of_New_Playlist=Listbox(Show_Playlist)
    List_Of_New_Playlist.place(x=10,y=20,width=360,height=250)
    if len(New_Node_Of_Tree.Nodes)==0:
        List_Of_New_Playlist.insert(END,"Empty")
    elif List_Of_New_Playlist.get(0)=="Empty":
        List_Of_New_Playlist.destroy(0)
    for music in New_Node_Of_Tree.Nodes:
        List_Of_New_Playlist.insert(END,(music.split('/'))[-1])
    def Remove_song_btn():#Remove song before saving // in show playlist Listbox
        answer=messagebox.askyesno("Delete","Are You Sure For Deleting")
        if answer:
            content_to_delete=List_Of_New_Playlist.get('active')
            for i in range(0,List_Of_New_Playlist.size()):
                if List_Of_New_Playlist.get(i)==content_to_delete:
                    List_Of_New_Playlist.delete(i)

            messagebox.showinfo("success","''"+content_to_delete+"'' Was Deleted Successfully!!!!")

            for music in (New_Node_Of_Tree.Nodes):
                if content_to_delete==((music.split('/'))[len(music.split('/'))-1]):
                    del (New_Node_Of_Tree.Nodes)[(New_Node_Of_Tree.Nodes).index(music)]
            if List_Of_New_Playlist.size()==0:
                List_Of_New_Playlist.insert(END,"Empty")
            Show_Playlist.destroy()

    Remove_Song_btn=Button(Show_Playlist,text="Remove Song",command=Remove_song_btn)
    Remove_Song_btn.place(x=390,y=30,width=100,height=22)

    Show_Playlist.mainloop()

##Open a Frame For Editing Playlist
def Edit_PlayList_Frame():
    global Current_Frame_in_MainPanel_Controller
    if Current_Frame_in_MainPanel_Controller!= "":
        Current_Frame_in_MainPanel_Controller.destroy()
    global List_Of_Playlist_Names_Edit
    Edit_Playlist_Setup_Frame =Frame(Main_Panel,bd=2,relief="groove")
    Current_Frame_in_MainPanel_Controller=Edit_Playlist_Setup_Frame
    List_Of_Playlist_Names_Edit=Listbox(Edit_Playlist_Setup_Frame)
    List_Of_Playlist_Names_Edit.place(x=5, y=40, width=300, height=250)



    database_Playlist_file=open(DataBase_File_Playlist,'r')
    database_Playlist_content=database_Playlist_file.readlines()
    database_Playlist_file.close()
    for i in database_Playlist_content.copy():
        if i!=" , \n":
            if '/' not in (((i[:-1]).split(','))[0]) and  (((i[:-1]).split(','))[0])!="" : #get only names not path from first Column
                List_Of_Playlist_Names_Edit.insert(END, ((i[:-1]).split(','))[0])

    if len(database_Playlist_content)==1:
        List_Of_Playlist_Names_Edit.insert(END,"Empty")
    if len(database_Playlist_content)>=2 and List_Of_Playlist_Names_Edit.get(0)=="Empty":
        List_Of_Playlist_Names_Edit.delete(0)

    # print(List_Of_Playlist_Names.get('active'))
    #
    # old_name.set(List_Of_Playlist_Names.get('active'))
    # def Rename():
    #     label_old_name=Label(Edit_Playlist_Setup_Frame,textvariable=old_name)
    #
    #






    Rename_btn=Button(Edit_Playlist_Setup_Frame, text="Rename", command=Rename_Playlist_btn)
    Rename_btn.place(x=340,y=65,width=80,height=20)

    Delete_btn=Button(Edit_Playlist_Setup_Frame, text="Delete", command=Delete_Playlist_Edit)
    Delete_btn.place(x=340,y=95,width=80,height=20)


    Delete_song_btn=Button(Edit_Playlist_Setup_Frame,text="Delete a Song from PlayList",command=Delete_Playlist_Song_Edit)
    Delete_song_btn.place(x=340,y=125,width=190,height=25)

    Add_song_btn=Button(Edit_Playlist_Setup_Frame,text="Add a Song To PlayList",command=Add_Song_Playlist_Edit)
    Add_song_btn.place(x=340,y=160,width=190,height=25)



    Edit_Playlist_Setup_Frame.place(x=10,y=10,width=555,height=350)

##In Edit FRame We Can Add Song To Existing Playlists
def Add_Song_Playlist_Edit():
    global List_Of_Playlist_Names_Edit
    if List_Of_Playlist_Names_Edit.get(0)=="Empty":
        messagebox.showerror("Error","No Playlist To Add Song")
    else:
        Add_Song_Window=Tk()
        Add_Song_Window.geometry('525x290')
        Add_Song_Window.title("Adding Song")
        Add_Song_Window.resizable(False,False)
        label=Label(Add_Song_Window,bd=2,relief="groove",text="Choose a Directory To add Music To Playlist ''"+List_Of_Playlist_Names_Edit.get('active')+"''")
        label.place(x=2,y=5,width=380,height=25)

        def Ask_Directory():
            global directory_addsong_pl_edit
            global List_of_directory_music
            label_content=StringVar()
            a="ss"
            label_content.set(a)
            directory_addsong_pl_edit=filedialog.askdirectory()

            print(directory_addsong_pl_edit)
            label_content.set(directory_addsong_pl_edit)
            label_addr=Label(Add_Song_Window,bd=2,relief="groove",textvariable=label_content)
            label_addr.place(x=2,y=35,width=350,height=25)
            List_of_directory_music=Listbox(Add_Song_Window)
            List_of_directory_music.place(x=2,y=65,width=410,height=200)
            add_to_playlist_btn=Button(Add_Song_Window,text="Add This Song",command=Add_NewMusic_To_Playlist)
            add_to_playlist_btn.place(x=420,y=170,width=105,height=25)
            for root, dirs, files in os.walk(directory_addsong_pl_edit):
                for filename in files:
                    if filename.endswith("mp3"):
                        List_of_directory_music.insert(END,filename)

        def Add_NewMusic_To_Playlist():
            answer=messagebox.askyesno("Add","Are You Sure You Want To Add ''"+List_of_directory_music.get('active')+"''")
            if answer:
                databse_file_playlist=open(DataBase_File_Playlist,'r')
                databse_file_playlist_content=databse_file_playlist.readlines()
                databse_file_playlist.close()
                for items in databse_file_playlist_content:
                    if items!=' , \n':
                        if '/' not in items:
                            if (items[:-1].split(','))[0]==List_Of_Playlist_Names_Edit.get('active'):
                                databse_file_playlist_content.insert(databse_file_playlist_content.index(items)+int((items[:-1].split(','))[1])+1,directory_addsong_pl_edit+"/"+List_of_directory_music.get('active'))
                                databse_file_playlist_content[databse_file_playlist_content.index(items)]=(items[:-1].split(','))[0]+','+str(int((items[:-1].split(','))[1])+1)+'\n'


                databse_file_playlist=open(DataBase_File_Playlist,'w')
                for music in  databse_file_playlist_content:
                    databse_file_playlist.write(music)
                databse_file_playlist.close()
        directory_ask_btn=Button(Add_Song_Window,text="Choose",command=Ask_Directory)
        directory_ask_btn.place(x=385,y=5,width=80,height=25)


        Add_Song_Window.mainloop()


##In Edit Frame We Can Rename Existing Playlists
def Rename_Playlist_btn():

    global Current_Frame_in_MainPanel_Controller
    old_name=StringVar()
    New_Name=StringVar()
    global label_old_name
    global Rename_Playlist_Name_Edit_Frame
    global List_Of_Playlist_Names_Edit
    global delete_btn_Edit_Frame
    if delete_btn_Edit_Frame!="":
        delete_btn_Edit_Frame.destroy()

    if List_Of_Playlist_Names_Edit.get(0)=="Empty":
        messagebox.showerror("Error","No Playlist To Rename")
    else:

        old_name.set("PlayList  " + "'" + List_Of_Playlist_Names_Edit.get('active')+"'"+"  Is Selected")
        Rename_Playlist_Name_Edit_Frame=Frame(Main_Panel, bd=2, relief="groove")
        Rename_Playlist_Name_Edit_Frame.place(x=320, y=190, width=235, height=110) #for old name and new name
        label_old_name=Label(Main_Panel,textvariable=old_name,bd=2,relief="groove")
        label_old_name.place(x=180,y=20,width=230,height=20)
        label_New_name=Label(Rename_Playlist_Name_Edit_Frame, text="Enter New Name Below :", bd=2, relief="groove")
        label_New_name.place(x=0,y=00,width=230,height=20)
        Entry_New_Name=Entry(Rename_Playlist_Name_Edit_Frame, textvariable=New_Name)
        Entry_New_Name.place(x=0,y=35,width=230,height=20)

        def Ask_Save():
            answer=messagebox.askyesno("Save Name","Are You Sure About This Name?")
            if answer:
                if Entry_New_Name.get()=="":
                    messagebox.showerror("Erro","Entry Name Can't Be Empty")
                else:
                    existing_controller=0

                    database_playlist_file=open(DataBase_File_Playlist,'r')
                    database_playlist_content=database_playlist_file.readlines()
                    database_playlist_file.close()
                    for i in database_playlist_content.copy():
                        if i.strip()!='':
                            if (((i[:-1]).split(','))[0]).lower()==(Entry_New_Name.get()).lower():
                                existing_controller=1

                    if existing_controller==1:
                        messagebox.showerror("Error","New Name Exist")

                    else:
                        database_file=open(DataBase_File_Playlist,'r')
                        database_file_Playlist_content=database_file.readlines()
                        database_file.close()
                        index=0
                        for i in range (0,len(database_file_Playlist_content)):
                            if database_file_Playlist_content[i].strip()!="" and database_file_Playlist_content[i]!="":
                                if (database_file_Playlist_content[i].split(','))[0]==List_Of_Playlist_Names_Edit.get('active'):
                                    database_file_Playlist_content[i]= Entry_New_Name.get()+","+ (database_file_Playlist_content[i].split(','))[1]

                        database_file=open(DataBase_File_Playlist,'w')
                        for i in database_file_Playlist_content:
                            database_file.write(i)
                        database_file.close()
                        Current_Frame_in_MainPanel_Controller.destroy()
                        Edit_PlayList_Frame()

                        messagebox.showinfo("Success","New Name was Set Successfully")





        Save_New_Name_btn=Button(Rename_Playlist_Name_Edit_Frame,text="Save Name", command=Ask_Save)
        Save_New_Name_btn.place(x=45,y=75,width=115,height=20)

##In Edit Frame We Can Delete A Entire Playlist
def Delete_Playlist_Edit():
    PlayList_To_Delete=StringVar()
    global  Rename_Playlist_Name_Edit_Frame
    global List_Of_Playlist_Names_Edit
    global label_old_name
    global  delete_btn_Edit_Frame

    if Rename_Playlist_Name_Edit_Frame!= "":
        Rename_Playlist_Name_Edit_Frame.destroy()
    if List_Of_Playlist_Names_Edit.get(0)=="Empty":
        messagebox.showerror("Error","No Playlist To Delete")
    else:
        PlayList_To_Delete.set("PlayList  " + "'" + List_Of_Playlist_Names_Edit.get('active')+"'"+"  Is Selected")
        label_old_name=Label(Main_Panel,textvariable=PlayList_To_Delete,bd=2,relief="groove")
        label_old_name.place(x=180,y=20,width=230,height=20)

        def Ask_Delete():
            answer=messagebox.askyesno("Delete Playlist","Are You Sure For Deleting This Playlist")
            if answer:
                content_to_delete=List_Of_Playlist_Names_Edit.get('active')
                database_file=open(DataBase_File_Playlist,'r')
                database_file_Playlist_content=database_file.readlines()
                database_file.close()
                index_Playlist_To_Delete=0 #understanding Position of Musics of deleted playlist
                Number_Of_Music_To_Delete=0 #understanding Position of Musics of deleted playlist
                for name in database_file_Playlist_content:
                    if name!=" , \n":
                        if '/' not in (((name[:-1]).split(','))[0])and (((name[:-1]).split(','))[0])==List_Of_Playlist_Names_Edit.get('active'):
                            Number_Of_Music_To_Delete=((((name[:-1]).split(','))[1]))
                            index_Playlist_To_Delete=(database_file_Playlist_content.index(name))
                            del database_file_Playlist_content[database_file_Playlist_content.index(name)]

                for music in database_file_Playlist_content.copy():  #Deleteing Songs Of Playlist
                    if  database_file_Playlist_content.index(music) >= int(index_Playlist_To_Delete) and database_file_Playlist_content.index(music)<int(Number_Of_Music_To_Delete)+int(index_Playlist_To_Delete):
                        del database_file_Playlist_content[database_file_Playlist_content.index(music)]

                database_file=open(DataBase_File_Playlist,'w')
                for i in database_file_Playlist_content:
                    database_file.write(i)
                database_file.close()
                for i in range(0,List_Of_Playlist_Names_Edit.size()):
                    if List_Of_Playlist_Names_Edit.get(i)==List_Of_Playlist_Names_Edit.get('active'):
                        List_Of_Playlist_Names_Edit.delete(i)

                database_file=open(DataBase_File_Playlist,'r')
                database_Playlist_content=database_file.readlines()
                database_file.close()

                if len(database_Playlist_content)==1:
                    List_Of_Playlist_Names_Edit.insert(END,"Empty")
                if len(database_Playlist_content)>=2 and List_Of_Playlist_Names_Edit.get(0)=="Empty":
                    List_Of_Playlist_Names_Edit.delete(0)

                messagebox.showinfo("Success","Playlist ''" +content_to_delete  +"'' Was Deleted Successfully")
                label_old_name.destroy()
                delete_btn_Edit_Frame.destroy()
        delete_btn_Edit_Frame=Button(Main_Panel,text="Delete Selected Playlist",command=Ask_Delete)
        delete_btn_Edit_Frame.place(x=300,y=320,width=210,height=20)

##This is The Final Step Of Creating New PlayList Which We Save It In Database File
def Save_New_Playlist():
    global Current_Frame_in_MainPanel_Controller
    global Entry_Playlist_Name
    global Playlist_Require_Directory_Addr
    global New_Node_Of_Tree
    global Playlist_frame
    Existing_Controller=0 ## controlling for loop and if statement after this line
    answer=messagebox.askyesno("Save?","Are You Sure You Want to Save This Playlist")
    if answer==True:
        saving_controller=""##for control the process of saving new playlist based on if playlist empty or not ,, this also for control messagebox of them
        if len(New_Node_Of_Tree.Nodes)==0:
            reply=messagebox.askyesno("Empty List","Playlist Empty Continue Saving??")
            saving_controller=reply
        if saving_controller==True or len(New_Node_Of_Tree.Nodes)!=0:

            if Entry_Playlist_Name.get()!="": ##if user didnt enter name
                database_playlist_file=open(DataBase_File_Playlist,'r')
                database_playlist_content=database_playlist_file.readlines()
                database_playlist_file.close()

                for i in database_playlist_content.copy():#cheking Existance
                    if i.strip()!='':
                        if (((i[:-1]).split(','))[0]).lower()==(Entry_Playlist_Name.get()).lower():
                            Existing_Controller=1
                            messagebox.showerror("Error","Playlist Name Exist")

                if Existing_Controller==0:
                    Label(Playlist_frame,bd=2,relief="groove",text=Entry_Playlist_Name.get(),width=100).pack(anchor=W)
                    database_playlist_file=open(DataBase_File_Playlist,'a')
                    database_playlist_file.write(Entry_Playlist_Name.get()+","+str(len(New_Node_Of_Tree.Nodes))+'\n')
                    for item in New_Node_Of_Tree.Nodes:
                        database_playlist_file.write(item+'\n')
                    database_playlist_file.close()
                Current_Frame_in_MainPanel_Controller.destroy()
                Add_Playlist_frame()
            else:
                messagebox.showerror("Error","PlayList Name Empty")

##A Frame Which You Can Creat New Playlist
def Add_Playlist_frame():
    global List_Of_My_Music_GeneralMusic
    global Playlist_Require_Directory_Addr
    global List_Of_Playlist_Music
    global Entry_Playlist_Name
    global New_Node_Of_Tree
    global Current_Frame_in_MainPanel_Controller
    if Current_Frame_in_MainPanel_Controller!= "":
        Current_Frame_in_MainPanel_Controller.destroy()
    List_Of_My_Music_GeneralMusic=""
    New_Playlist_Setup_Frame =Frame(Main_Panel,bd=2,relief="groove")
    Current_Frame_in_MainPanel_Controller=New_Playlist_Setup_Frame
    Label_Add_Playlist=Label(New_Playlist_Setup_Frame,text="Enter Playlist Name : ",bd=2,relief="groove").place(x=10,y=10,width=140,height=35)
    Entry_Playlist_Name=Entry(New_Playlist_Setup_Frame,width=15)
    Label_Add_Playlist_Dirchoose=Label(New_Playlist_Setup_Frame,text="Choose a Directory To Add Music To Playlist : ",bd=2,relief="groove").place(x=10,y=50,width=300,height=35)
    Directory_Playlist_Btn=Button(New_Playlist_Setup_Frame, text="Choose ...", command=Ask_for_Directory_Playlist).place(x=340, y=50, width=100, height=35)
    List_Of_Playlist_Music=Listbox(New_Playlist_Setup_Frame)
    Add_To_Node_btn=Button(New_Playlist_Setup_Frame,text="Add To Playlist",command=Add_Muisc_To_Tree_Before_saving_Playlist)
    Add_To_Node_btn.place(width=110, height=25, x=420, y=140)
    Show_Node_btn=Button(New_Playlist_Setup_Frame,text="Show Me This Playlist",command=Show_Playlist_New_Node)
    Show_Node_btn.place(width=150, height=25, x=390, y=320)
    New_Node_Of_Tree=Node_Playlist(Entry_Playlist_Name.get())#creat a empty node at first
    List_Of_Playlist_Music.place(width=400, height=180, x=10, y=140)
    New_Playlist_Setup_Frame.place(x=10,y=10,width=555,height=350)
    Entry_Playlist_Name.place(y=15,x=160)




##This Function is declared here because you may want to show queue even you choose db or pl for queue in combobox
def Show_Queue_Songs(): #For btn below

    Show_Me_Queue_Window=Tk()
    Show_Me_Queue_Window.geometry('500x300')
    Show_Me_Queue_Window.title("Songs Queue")
    Show_Me_Queue_Window.resizable(False,False)
    list_of_queue=Listbox(Show_Me_Queue_Window)
    list_of_queue.place(x=10,y=10,width=350,height=270)
    if len(My_General_Queue_To_Play.items)==0:
        list_of_queue.insert(END,"Empty")

    def Remove_Song_From_Queue():#remove song frome original queue

        if list_of_queue.get(0)=="Empty":
            messagebox.showerror("Error","No Music To Delete")
        else:
            for music in My_General_Queue_To_Play.items:
                content_To_Remove=list_of_queue.get('active')
                if (music.split('/')[-1]) == list_of_queue.get('active'):
                    index_to_delete=( My_General_Queue_To_Play.items).index(music)
                    number_elements_to_push_after_delete=len(My_General_Queue_To_Play.items)-index_to_delete-1
                    for i in range(0,index_to_delete):
                        poped_element=My_General_Queue_To_Play.pop()
                        My_General_Queue_To_Play.push(poped_element)
                    My_General_Queue_To_Play.pop()
                    for i in range(0,number_elements_to_push_after_delete):
                        poped_element=My_General_Queue_To_Play.pop()
                        My_General_Queue_To_Play.push(poped_element)

            for i in range(0,list_of_queue.size()): ##to see deleting from list
                if list_of_queue.get(i)==list_of_queue.get('active'):
                    list_of_queue.delete(i)
                    if list_of_queue.size()==0:

                        list_of_queue.insert(END,"Empty")
            messagebox.showinfo("Success",content_To_Remove+"  Successfully Removed")
    remove_song_btn=Button(Show_Me_Queue_Window,text="Remove Song",command=Remove_Song_From_Queue)
    remove_song_btn.place(x=378,y=30,width=110,height=30)
    for music in My_General_Queue_To_Play.items:
        list_of_queue.insert(END,(music.split('/'))[-1])

    Show_Me_Queue_Window.mainloop()##This Fu##This

##A Function To Open A Frame To Start Building Your Queue Play
def Play_Queue_Building_Frame():
    global Current_Frame_in_MainPanel_Controller
    global Play_queue_frame
    global My_General_Queue_To_Play
    global My_Queue_Database_List  ##when combobox choosed database for its list
    #**************************************************************
    if Current_Frame_in_MainPanel_Controller!="":
        Current_Frame_in_MainPanel_Controller.destroy()

    Combobox_variable=StringVar(value="Choose What To Be Queue")

    Play_queue_frame =Frame(Main_Panel,bd=2,relief="groove")
    Play_queue_frame.place(x=10,y=10,width=555,height=350)
    Current_Frame_in_MainPanel_Controller=Play_queue_frame

    #*************************************************************
    label_Help=Label(Play_queue_frame,bd=2,relief="groove",text="Build Your Favourite Queue By Choosing Songs From DB or Your Own Playlists")
    label_Help.place(x=10,y=5,width=530,height=25)
    choose_combobox=ttk.Combobox(Play_queue_frame,textvariable=Combobox_variable)
    choose_combobox['values']=('PlayList','General Musics')
    choose_combobox.place(x=120,y=40,height=25,width=210)
    def give_database(): #for when database choosed in combo box
        global queue_give_playlist_frame
        global  My_Queue_Database_List
        global Add_To_Queue_btn
        global Show_Queue_btn
        global queue_give_database_frame
        if queue_give_playlist_frame!="":
            queue_give_playlist_frame.destroy()
        queue_give_database_frame=Frame(Play_queue_frame,bd=2,relief="groove")
        My_Queue_Database_List=Listbox(queue_give_database_frame)
        My_Queue_Database_List.place(x=0,y=5,width=360,height=250)
        Add_To_Queue_btn=Button(queue_give_database_frame,text="Add To Queue",command=Add_To_Queue_DB)
        Add_To_Queue_btn.place(x=370,y=60,width=120,height=20)
        queue_give_database_frame.place(x=10,y=75,width=500,height=270)


        Show_Queue_btn=Button(queue_give_database_frame,text="Show Me Queue",command=Show_Queue_Songs)
        Show_Queue_btn.place(x=370,y=120,width=120,height=20)


        Finish_building_btn=Button(queue_give_database_frame,text="Finish Building",command=Finish_Build_Queue)
        Finish_building_btn.place(x=370,y=238,width=120,height=20)


        List_Of_Music_file=open(DataBase_File_AddMusic)
        List_Of_Music_file_content=List_Of_Music_file.readlines()
        List_Of_Music_file.close()
        if len(List_Of_Music_file_content)==1:
            My_Queue_Database_List.insert(END, 'Empty')
        if len(List_Of_Music_file_content)!=1: #(empty set is ['\n'])if file was empty(first time)prevent us from getting error
            My_Queue_Database_List.delete(0)
            for i in List_Of_Music_file_content:
                if i.strip()!='' and i!=' , \n':
                    My_Queue_Database_List.insert(END, ((i[:-1]).split(','))[1])

    def give_Playlist():

        global  List_Of_Playlist_Songs
        global List_Of_Playlist_Names_Queue_AddPl

        global queue_give_playlist_frame
        global queue_give_database_frame
        if  queue_give_database_frame!="":
            queue_give_database_frame.destroy()


        # global  My_Queue_Database_List
        # global Add_To_Queue_btn
        # global  Show_Queue_btn
        # Add_To_Queue_btn.destroy()
        # Show_Queue_btn.destroy()
        # My_Queue_Database_List.destroy()
        queue_give_playlist_frame=Frame(Play_queue_frame,bd=2,relief="groove")
        label_title=Label(queue_give_playlist_frame,bd=2,relief="groove",text="My PlayLists")
        label_title.place(x=160,y=15,width=110,height=20)
        List_Of_Playlist_Names_Queue_AddPl=Listbox(queue_give_playlist_frame)
        List_Of_Playlist_Names_Queue_AddPl.place(x=20, y=40, width=350, height=200)
        queue_give_playlist_frame.place(x=10,y=85,width=530,height=260)

        Finish_building_btn=Button(queue_give_playlist_frame,text="Finish Building",command=Finish_Build_Queue)
        Finish_building_btn.place(x=380,y=220,width=120,height=20)


        List_Of_Playlist_file=open(DataBase_File_Playlist)
        List_Of_Playlist_file_content=List_Of_Playlist_file.readlines()
        List_Of_Playlist_file.close()
        for i in List_Of_Playlist_file_content.copy():
            if i!=" , \n":
                if '/' not in (((i[:-1]).split(','))[0]): #get only names not path from first Column
                    List_Of_Playlist_Names_Queue_AddPl.insert(END, ((i[:-1]).split(','))[0])


        def Add_Whole_Playlist():
            answer=messagebox.askyesno("Whole Adding","Adding Whole Songs in Playlist ''"+List_Of_Playlist_Names_Queue_AddPl.get('active')+"''")
            if answer:
                messagebox.showinfo("Success","Songs Added Successfully")
                playlist_database_file=open(DataBase_File_Playlist,'r')
                playlist_database_file_content=playlist_database_file.readlines()
                playlist_database_file.close()
                for item in playlist_database_file_content:
                    if item !=" , \n" :
                        if '/' not in item:
                            if (item[:-1].split(','))[0]==List_Of_Playlist_Names_Queue_AddPl.get('active'):
                                for i in range(playlist_database_file_content.index(item)+1,playlist_database_file_content.index(item)+1+int((item[:-1].split(','))[1])):
                                    My_General_Queue_To_Play.push(playlist_database_file_content[i])




        def Go_To_Playlist():
            global queue_give_playlist_frame
            global List_Of_Playlist_Songs
            song_title=StringVar()
            name_of_playlist=List_Of_Playlist_Names_Queue_AddPl.get('active')
            queue_give_playlist_frame.destroy()
            song_title.set("PlayList  ''"+name_of_playlist+"''  Songs")

            Go_To_Playlist_Songs_frame=Frame(Play_queue_frame,bd=2,relief="groove")

            Add_To_Queue_btn_Playlist=Button(Go_To_Playlist_Songs_frame,text="Add To Queue",command=Add_To_Queue_PL)
            Add_To_Queue_btn_Playlist.place(x=390,y=100,width=120,height=20)
            Go_To_Playlist_Songs_frame.place(x=10,y=85,width=530,height=260)






            Show_Queue_btn=Button(Go_To_Playlist_Songs_frame,text="Show Me Queue",command=Show_Queue_Songs)
            Show_Queue_btn.place(x=390,y=130,width=120,height=20)




            def BackTo_Playlists():
                Go_To_Playlist_Songs_frame.destroy()
                give_Playlist()

            BackTo_PLaylists_btn=Button(Go_To_Playlist_Songs_frame,text="Back To PlayLists",command=BackTo_Playlists)
            BackTo_PLaylists_btn.place(x=390,y=190,width=120,height=20)

            Finish_building_btn=Button(Go_To_Playlist_Songs_frame,text="Finish Building",command=Finish_Build_Queue)
            Finish_building_btn.place(x=380,y=230,width=120,height=20)





            label_playlist_songs_title=Label(Play_queue_frame,textvariable=song_title,relief="groove",bd=2)
            label_playlist_songs_title.place(x=170,y=95,width=185,height=20)
            List_Of_Playlist_Songs=Listbox(Play_queue_frame)
            List_Of_Playlist_Songs.place(x=40,y=120,width=350,height=200)
            database_file=open(DataBase_File_Playlist,'r')
            database_file_Playlist_content=database_file.readlines()
            database_file.close()
            for name in database_file_Playlist_content.copy():
                if name!=",\n":
                    if '/' not in (((name[:-1]).split(','))[0])and (((name[:-1]).split(','))[0])==name_of_playlist:
                        for i in range(database_file_Playlist_content.index(name)+1,database_file_Playlist_content.index(name)+1+int((((name[:-1]).split(','))[1]))):
                            List_Of_Playlist_Songs.insert(END,(((database_file_Playlist_content[i])[:-1]).split('/'))[-1])




        Add_Whole_Playlist_Songs=Button(queue_give_playlist_frame,text="Add Whole Playlist",command=Add_Whole_Playlist)
        Add_Whole_Playlist_Songs.place(x=380,y=130,width=130,height=20)

        Go_To_Playlist_Songs=Button(queue_give_playlist_frame,text="Go To PlayList",command=Go_To_Playlist)
        Go_To_Playlist_Songs.place(x=380,y=100,width=120,height=20)


    def Add_To_Queue_DB():
        if My_Queue_Database_List.get(0)=="Empty":
            messagebox.showerror("Error","No Music To Add")
        else:
            List_Of_Music_file=open(DataBase_File_AddMusic)
            List_Of_Music_file_content=List_Of_Music_file.readlines()
            List_Of_Music_file.close()

            for music in List_Of_Music_file_content.copy():
                if music!=' , \n':
                    if (((music[:-1]).split(','))[1])==My_Queue_Database_List.get('active'):
                        My_General_Queue_To_Play.push((((music[:-1]).split(','))[0]) +'/'+My_Queue_Database_List.get('active'))
            messagebox.showinfo("Success",My_Queue_Database_List.get('active')+" Successfully Added")
    def Add_To_Queue_PL():
        global List_Of_Playlist_Names_Queue_AddPl
        List_Of_Music_file=open(DataBase_File_Playlist,'r')
        List_Of_Music_file_content=List_Of_Music_file.readlines()
        List_Of_Music_file.close()
        pl_name=List_Of_Playlist_Names_Queue_AddPl
        print(pl_name.get('active'))

        for music in List_Of_Music_file_content.copy():
            if music!=' , \n':
                if '/' not in music:
                    if (((music[:-1]).split(','))[0])==pl_name:
                        print(pl_name)

                        # for i in range(List_Of_Music_file_content.index(music)+1,List_Of_Music_file_content.index(music)+1+(((music[:-1]).split(','))[1])):
                        #     if (((i[:-1]).split('/'))[-1])==List_Of_Playlist_Names_Queue_AddPl.get('active'):
                        #         My_General_Queue_To_Play.push((((music[:-1]).split(','))[0]) +'/'+List_Of_Playlist_Songs.get('active'))

        # messagebox.showinfo("Success",List_Of_Playlist_Names_Queue_AddPl.get('active')+" Successfully Added")

    def Decide_To_Open_PL_DB():#controller of combobox element
        if Combobox_variable.get()=='Choose What To Be Queue':
            messagebox.showerror("Errot","Please Select an Option")
        if Combobox_variable.get()=='General Musics':
            give_database()
        if Combobox_variable.get()=='PlayList':
            give_Playlist()

    def Finish_Build_Queue():
        if len(My_General_Queue_To_Play.items)==0:
            messagebox.showinfo("Alert","Your Queue is Still Empty")
            answer=messagebox.askyesno("Finish","Are Your Sure You Want To Abort Selecting Step")
            if answer==True:
                Play_queue_frame.destroy()

        else:
            javab=messagebox.askyesno("Finish","Are Your Sure You Want To Complete Queueing ")
            if javab==True:
                Play_queue_frame.destroy()
                queue_database_file=open(Database_File_Queue,'w')
                for musics in My_General_Queue_To_Play.items:
                    queue_database_file.write(musics+'\n')
                queue_database_file.close()
                reply=messagebox.askyesno("Success","Are You Ready To Play Your Queue")
                if reply:
                    Play_Queue_Playtime_Frame()

    GO_btn=Button(Play_queue_frame,text="GO",command=Decide_To_Open_PL_DB)
    GO_btn.place(x=350,y=40,height=25,width=80)

##This Function Asks User To Load Previous Queue Or To Start A New Process Of Building Queue
def Play_Queue_Decider_Function():
    global Current_Frame_in_MainPanel_Controller
    queue_database_file=open(Database_File_Queue)
    queue_database_file_content=queue_database_file.readlines()
    queue_database_file.close()
    if len(queue_database_file_content)>=1 and queue_database_file_content[0]!=" , \n":
        answer=messagebox.askyesno("Existance","You Have Already Defined A Queue,Do You Want To Load Them?")
        if answer==True:
            if Current_Frame_in_MainPanel_Controller!="":
                Current_Frame_in_MainPanel_Controller.destroy()
            Play_Queue_Playtime_Frame()
        else:
            if Current_Frame_in_MainPanel_Controller!="":
                Current_Frame_in_MainPanel_Controller.destroy()
            Play_Queue_Building_Frame()

    else:
        if Current_Frame_in_MainPanel_Controller!="":
            Current_Frame_in_MainPanel_Controller.destroy()
        My_General_Queue_To_Play.items=[]
        Play_Queue_Building_Frame()

##This Function Is Result Say Yes To Decider Function Or Finish Building Queue btn
def Play_Queue_Playtime_Frame():
    global Current_List_To_Play
    global Current_Frame_in_MainPanel_Name
    #**************************************************************
    global Current_Frame_in_MainPanel_Controller
    if Current_Frame_in_MainPanel_Controller!="":
        Current_Frame_in_MainPanel_Controller.destroy()
    Play_Queue_Playtime_frame=Frame(Main_Panel,bd=2,relief="groove")
    Play_Queue_Playtime_frame.place(x=5,y=5,width=565,height=350)
    Current_Frame_in_MainPanel_Controller=Play_Queue_Playtime_frame
    #***************************************************************
    Play_Queue_Playtime_title=Label(Play_Queue_Playtime_frame,bd=2,font=8,relief="groove",text="My Enjoyable Queue Ever")
    Play_Queue_Playtime_title.place(x=190,y=18,width=225,height=20)
    Play_Queue_Playtime_list=Listbox(Play_Queue_Playtime_frame)
    Play_Queue_Playtime_list.place(x=60,y=45,width=450,height=240)
    database_queue_file=open(Database_File_Queue,'r')
    database_queue_file_content=database_queue_file.readlines()
    database_queue_file.close()
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%Queue For Play%%%%%%%%%%%%%%%%%%%%%%%%%%%55

    global Queue_Play_For_AppQueue  ##This is above Queue
    Queue_Play_For_AppQueue=Queue()
    for music in database_queue_file_content:
        Queue_Play_For_AppQueue.push(music[:-1])
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%Queue For Play%%%%%%%%%%%%%%%%%%%%%%%%%%%55




    for music in database_queue_file_content:
        if music!='\n':
            Play_Queue_Playtime_list.insert(END,(music[:-1].split('/'))[-1])

    Current_Frame_in_MainPanel_Name="Play_Queue_Playtime_frame"
    Current_List_To_Play=Play_Queue_Playtime_list




##A Frame Which You Can Add Music To Your App , These Apps Are Not Specific(Playlist) But Are General
def Genral_Music_Frame():
    global List_Of_Music_dir
    global List_Of_My_Music_GeneralMusic
    global List_Of_Playlist_Music
    global Current_Frame_in_MainPanel_Controller
    global Current_List_To_Play
    global Current_Frame_in_MainPanel_Name
    global Queue_Play_For_GeneralMusic
    #********************************
    Current_Frame_in_MainPanel_Name="General_Music_Panel"
    if Current_Frame_in_MainPanel_Controller!= "":
        Current_Frame_in_MainPanel_Controller.destroy()
    #********************************
    List_Of_Playlist_Music=""
    Genral_Music_Frame =Frame(Main_Panel,bd=2,relief="groove")
    Current_Frame_in_MainPanel_Controller=Genral_Music_Frame
    Genral_Music_Frame.place(x=10,y=10,width=555,height=350)
    label_All_Musics=Label(Genral_Music_Frame,text="List Of Your Musics")
    label_All_Musics.place(width=150,height=20,x=190,y=30)
    #********************************************************
    List_Of_My_Music_GeneralMusic=Listbox(Main_Panel)
    List_Of_My_Music_GeneralMusic.place(width=450, height=200, x=60, y=85)
    Current_List_To_Play=List_Of_My_Music_GeneralMusic
    #********************************************************
    List_Of_Music_file=open(DataBase_File_AddMusic)
    List_Of_Music_file_content=List_Of_Music_file.readlines()
    List_Of_Music_file.close()
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%Queue For Play%%%%%%%%%%%%%%%%%%%%%%%%%%%55
    if len(List_Of_Music_file_content)>1:
        Queue_Play_For_GeneralMusic=Queue()
        for music in List_Of_Music_file_content:
            if music !=" , \n":
                Queue_Play_For_GeneralMusic.push((music[:-1].split(','))[0] + "/" + (music[:-1].split(','))[1])
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%Queue For Play%%%%%%%%%%%%%%%%%%%%%%%%%%%55


    if len(List_Of_Music_file_content)==1:
        List_Of_My_Music_GeneralMusic.insert(END, 'Empty')
    if len(List_Of_Music_file_content)!=1: #(empty set is ['\n'])if file was empty(first time)prevent us from getting error
        List_Of_My_Music_GeneralMusic.delete(0)
        for i in List_Of_Music_file_content:
            if i!=" , \n":
                List_Of_My_Music_GeneralMusic.insert(END, ((i[:-1]).split(','))[1])
    Add_Btn=Button(Main_Panel,text="Add a Song",command=Add_Music_Frame)
    Add_Btn.place(width=130,height=25,x=90,y=300)


    Remove_Btn=Button(Main_Panel,text="Remove a Song",command=Remove_Song_Databse)
    Remove_Btn.place(width=130,height=25,x=250,y=300)

##Adding Muisc To General Muisc Database
def Add_Music_To_Database():
    global List_Of_Music_dir
    global Add_Music_dir
    database_file=open(DataBase_File_AddMusic, 'a')
    database_file.write(Add_Music_dir.get()+','+List_Of_Music_dir.get('active')+'\n')
    database_file.close()
    messagebox.showinfo("Success","''"+List_Of_Music_dir.get('active')+"'' Successfully Added ")

##Like Playlist Above For Choose btn
def Ask_To_Add_Music():
    global Add_Music_dir
    global List_Of_Music_dir
    dir_addr=filedialog.askdirectory()
    Add_Music_dir.set(dir_addr)
    label_dir=Label(Main_Panel,bd=2,relief="groove",textvariable=Add_Music_dir)
    label_dir.place(x=23,y=60,width=300,height=40)
    List_Of_Music_dir=Listbox(Main_Panel)
    List_Of_Music_dir.place(width=400,height=180,x=20,y=110)
    AddTo_Genral_Btn=Button(Main_Panel,text="Add To General Music",command=Add_Music_To_Database)
    AddTo_Genral_Btn.place(x=330,y=310,width=150,height=30)
    for root, dirs, files in os.walk(Add_Music_dir.get()):
        for filename in files :
            if filename.endswith("mp3"):
                List_Of_Music_dir.insert(END,filename)

##This is File Tab In The Right Above Corner Of App , Which You Can Add Music To You General Music
##This Fucntion Also Used In General Music Frame For More Flexibility
def Add_Music_Frame():
    global Current_Frame_in_MainPanel_Controller
    if Current_Frame_in_MainPanel_Controller!= "":
        Current_Frame_in_MainPanel_Controller.destroy()
    New_AddMusic_setup =Frame(Main_Panel,bd=2,relief="groove")
    Current_Frame_in_MainPanel_Controller=New_AddMusic_setup
    New_AddMusic_setup.place(x=10,y=10,width=555,height=350)
    Label_Add_Playlist_Dirchoose=Label(New_AddMusic_setup,text="Choose a Directory To Add Music To Play : ",bd=2,relief="groove").place(x=10,y=10,width=300,height=35)
    Directory_Playlist_Btn=Button(New_AddMusic_setup,text="Choose ...",command=Ask_To_Add_Music).place(x=330,y=10,width=100,height=35)

##You Can Remove Songs From Your General Music
def Remove_Song_Databse():
    global List_Of_My_Music_GeneralMusic
    global DataBase_File_AddMusic

    content_to_delete=List_Of_My_Music_GeneralMusic.get('active')
    database_file=open(DataBase_File_AddMusic, 'r')
    data_base_content=database_file.readlines()
    database_file.close()
    answer=messagebox.askyesno("Deleting","Are You Sure For Deleting ''" + content_to_delete+"''")
    if answer:
        if List_Of_My_Music_GeneralMusic.get(0)=="Empty":
            messagebox.showerror("Error","You Have No Music To Delete")

        else:
            for i in data_base_content.copy():
                if i.strip()!='':
                    if ((i[:-1]).split(','))[1]==content_to_delete:
                        del data_base_content[data_base_content.index(i)]

            database_file=open(DataBase_File_AddMusic, 'w')
            for i in data_base_content:
                database_file.write(i)
            database_file.close()
            for i in range(0,List_Of_My_Music_GeneralMusic.size()):
                if List_Of_My_Music_GeneralMusic.get(i)==content_to_delete:
                    List_Of_My_Music_GeneralMusic.delete(i)
            if List_Of_My_Music_GeneralMusic.size()==0:
                List_Of_My_Music_GeneralMusic.insert(END,"Empty")
            messagebox.showinfo("Success",content_to_delete+" Successfully Removed")





##Help Of App
def Help_APP():
    messagebox.showinfo("Help","Visit 'WWW.Musicly.com' To See Documentation")

##About Us
def About_APP():
    About_Window=Tk()
    About_Window.geometry('390x200')
    About_Window.resizable(False,False)
    About_Window.title("About Us")
    label_About_Us=Text(About_Window,width=170,height=180,font="Times,4,Bold")
    label_About_Us.pack()
    label_About_Us.insert(END,"Musicly is Combinataion of Inovation , Flexibility Features Which Every App Wish To Have.Our Great Executive Team Are Consist Of Creative Designers , Programmers Which Try To Redefine Meaning Of Usablity. ")

    About_Window.mainloop()

#***************************************************************************************************

#..................................GUI Elements......................................................
Menu_Bar=Menu()
Options_File=Menu()
Options_Playlist=Menu()
Options_Help=Menu()
Options_Control=Menu()
Options_Playlist.add_command(label="add Playlist",command=Add_Playlist_frame)
Options_Playlist.add_command(label="Edit Playlist",command=Edit_PlayList_Frame)
Options_File.add_command(label="Add Music", command=Add_Music_Frame)
Options_File.add_cascade(label="Playlist",menu=Options_Playlist)
Options_File.add_separator()
Options_File.add_command(label="Close",command=Close_App)
Options_Help.add_command(label="Help",command=Help_APP)
Options_Help.add_command(label="About Us",command=About_APP)
Options_Control.add_command(label="Play",command=Play_Music)
Options_Control.add_command(label="Pause",command=Pause_Music)
Options_Control.add_command(label="Stop",command=Stop_Music)
Options_Control.add_separator()
Options_Control.add_command(label="Next Music",command=Next_Song)
Options_Control.add_command(label="Previous Music",command=Previous_Music)
Options_Control.add_separator()
Options_Control.add_command(label="Increase Volume",command=Increase_Volume)
Options_Control.add_command(label="Decrease Volume",command=Decrease_Volume)
Menu_Bar.add_cascade(label="File",menu=Options_File)
Menu_Bar.add_cascade(label="Control",menu=Options_Control)
Menu_Bar.add_cascade(label="Help",menu=Options_Help)
library_label=Label(text="Library",borderwidth=3, relief="groove",font="12").place(x=10,y=10,width=80,height=35)
library_frame=Listbox(bg="#d9d9d9",bd=2,relief="groove")
Playlist_label=Label(text="Playlists",borderwidth=3, relief="groove",font="12").place(x=10,y=260,width=80,height=35)
Playlist_frame=Listbox(bg="#d9d9d9",bd=2 , relief="groove")
PlayQueue_btn=Button(library_frame,bg="#8c8c8c", text="Play Queue", width=130, command=Play_Queue_Decider_Function).pack(anchor=W)
Music_btn=Button(library_frame,bg="#8c8c8c",text="General_Music",width=130,command=Genral_Music_Frame).pack(anchor=W,pady=5)
Playlist_frame.place(x=20,y=300,height=190,width=130)
library_frame.place(x=20,y=48,height=190,width=130)
Music_Control_btn_frame=Frame(bd=2,bg="#0a0f0f",relief="groove")
Timer_frame=Frame(Music_Control_btn_frame,bd=2,relief="groove",width=105,height=10)
label_App_Slogan_part1=Label(Main_Panel,bg="#737373",text="Welcome To Musicly Player",font=12)
label_App_Slogan_part2=Label(Main_Panel,bg="#737373",text="Musicly A Player That Every One Wish To Have",font=12)
label_App_Slogan_part3=Label(Main_Panel,bg="#737373",text="Start Journey To Songs From Here",font=12)
label_App_Slogan_part1.place(x=190,y=85,width=230,height=25)
label_App_Slogan_part2.place(x=130,y=170,width=393,height=25)
label_App_Slogan_part3.place(x=184,y=235,width=280,height=25)

#....................................Control Player btn ..............................
Volume_Decrease=Button(Music_Control_btn_frame,text="-V",bg="#991f00",command=Decrease_Volume).grid(row=0,column=0,padx=10)
Volume_Increase=Button(Music_Control_btn_frame,text="+V",bg="#991f00",command=Increase_Volume).grid(row=0,column=1,padx=10)
Previous_Music=Button(Music_Control_btn_frame,bg="#991f00",text="<<",command=Previous_Music).grid(row=0,column=2,padx=10)
Stop=Button(Music_Control_btn_frame,bg="#991f00",text="Stop",command=Stop_Music).grid(row=0,column=3,padx=10)
Pause_Music=Button(Music_Control_btn_frame,bg="#991f00",text="||",command=Pause_Music).grid(row=0,column=4,padx=10)
Play_music=Button(Music_Control_btn_frame,bg="#991f00",text="|>",command=Play_Music).grid(row=0,column=5,padx=10)
Next_Music=Button(Music_Control_btn_frame,bg="#991f00",text=">>",command=Next_Song).grid(row=0,column=6,padx=10)
Timer_Object = StopWatch(Timer_frame)
Timer_Object.pack(side=TOP)
Music_Control_btn_frame.place(x=195,y=430,height=39,width=560)
Timer_frame.grid(row=0,column=7)

#..................................................................................



Initialize_Playlist() #Initializing Playlist Frame




Main_Window.config(menu=Menu_Bar)
Main_Window.mainloop()



