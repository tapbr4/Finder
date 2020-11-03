import psycopg2
import tkinter
from datetime import datetime
from tkinter import messagebox
from tkinter import *

## IMAGENS: Foto de perfil e pescado;
## FOLLOW: Seguir o perfil de um amigo;
## FORMS: Expressões regulares para validação / Deleção de contas.

connection = psycopg2.connect(database='finder',user='postgres',password='postgres',host='localhost')
print('Sucesso na conexão.')
cursor = connection.cursor()

class SignInGUI:
    def __init__(self):
        #Window
        self.signin_window = Toplevel()
        self.signin_window.title(' ')
        self.signin_window.geometry('190x190')
        self.signin_window.resizable(width=False,height=False)
        self.signin_window['bg'] = 'black'
        #
        self.new_username_label = Label(self.signin_window,text='Username',bg='black',fg='white')
        self.new_username_entry = Entry(self.signin_window,width=20)
        self.new_email_label = Label(self.signin_window,text='E-mail',bg='black',fg='white')
        self.new_email_entry = Entry(self.signin_window,width=20)
        self.new_name_label = Label(self.signin_window,text='Nome',bg='black',fg='white')
        self.new_name_entry = Entry(self.signin_window,width=20)
        self.new_cpf_label = Label(self.signin_window,text='CPF',bg='black',fg='white')
        self.new_cpf_entry = Entry(self.signin_window,width=20)
        self.new_phone_label = Label(self.signin_window,text='Telefone',bg='black',fg='white')
        self.new_phone_entry = Entry(self.signin_window,width=20)
        self.new_address_label = Label(self.signin_window,text='Endereço',bg='black',fg='white')
        self.new_address_entry = Entry(self.signin_window,width=20)
        self.new_password_label = Label(self.signin_window,text='Senha',bg='black',fg='white')
        self.new_password_entry = Entry(self.signin_window,width=20,show='*')
        self.new_account_button = Button(self.signin_window,width=25,text='Criar nova conta', command = self.create_account_button)
        #
        self.new_username_label.grid(row=0,column=0)
        self.new_username_entry.grid(row=0,column=1)
        self.new_email_label.grid(row=1,column=0)
        self.new_email_entry.grid(row=1,column=1)
        self.new_name_label.grid(row=2,column=0)
        self.new_name_entry.grid(row=2,column=1)
        self.new_cpf_label.grid(row=3,column=0)
        self.new_cpf_entry.grid(row=3,column=1)
        self.new_phone_label.grid(row=4,column=0)
        self.new_phone_entry.grid(row=4,column=1)
        self.new_address_label.grid(row=5,column=0)
        self.new_address_entry.grid(row=5,column=1)
        self.new_password_label.grid(row=6,column=0)
        self.new_password_entry.grid(row=6,column=1)
        self.new_account_button.place(x=3,y=155)
        #
        self.signin_window.mainloop()

    def create_account_button(self):
        cursor.execute("select username from login where username=%s",(self.new_username_entry.get(),))
        connection.commit()
        row = cursor.fetchall()
        if row:
            messagebox.showwarning('',f'O nome de usuário " {self.new_username_entry.get()} " já existe. Escolha um nome de usuário diferente.')
            return
        else:
            new_username = self.new_username_entry.get()
            new_email = self.new_email_entry.get()
            new_passw = self.new_password_entry.get()
            new_name = self.new_name_entry.get()
            new_cpf = self.new_cpf_entry.get()
            new_phone = self.new_phone_entry.get()
            new_address = self.new_address_entry.get()
            if len(new_username)==0 or len(new_email)==0 or len(new_passw)==0 or len(new_name)==0 or len(new_cpf)==0 or len(new_phone)==0 or len(new_address)==0:
                messagebox.showinfo('Error','Algo deu errado. Verifique todos os campos e tente novamente.')
                return
            else:
                cursor.execute("insert into login(username,email,password) values(%s,%s,%s)",(new_username,new_email,new_passw,))
                connection.commit()
                cursor.execute("select idUser from login order by idUser desc")
                connection.commit()
                rows = cursor.fetchall()
                idUser = int(rows[0][0])
                cursor.execute("insert into userinfo(idUser,nome,cpf,telefone,endereco) values(%s,%s,%s,%s,%s)",(idUser,new_name,new_cpf,new_phone,new_address))
                connection.commit()
                messagebox.showinfo('Succesful','Novo usuário criado com sucesso.')

class LoginGUI:
    def __init__(self):
        global current_name
        global current_profile
        #Window
        self.login_window = Tk()
        self.login_window.title('Finder - Login')
        self.login_window.geometry('480x560')
        self.login_window.resizable(width=False,height=False)
        self.login_window['bg'] = 'black'
        #
        current_profile = StringVar()
        current_name = StringVar()
        #
        self.logo = tkinter.PhotoImage(file="logo.png")
        self.logoframe = Label(self.login_window, image = self.logo,bg='green')
        self.delete_account_label = Label(self.login_window,text='Apagar Conta',bg='green',fg='grey')
        self.delete_account_label.bind('<Button-1>',lambda e: self.delete_account())
        self.login_label = Label(self.login_window, text='Login', bg='black', fg='white')
        self.login_label.config(font = ('Terminal','13'))
        self.login_entry = Entry(self.login_window, width=30)
        self.passw_label = Label(self.login_window, text='Senha', bg='black', fg='white')
        self.passw_label.config(font = ('Terminal','13'))
        self.passw_entry = Entry(self.login_window, show='*', width=30)
        self.signin_label = Label(self.login_window, text='Criar nova conta', bg='black', fg='green')
        self.signin_label.config(font = ('Terminal','10'))
        self.signin_label.bind('<Button-1>', lambda e: self.signinButton())
        #
        self.login_button = Button(self.login_window, width=11, text='Entrar', command=self.loginButton)
        #
        self.logoframe.place(x=0,y=0)
        self.login_label.place(x=50,y=500)
        self.login_entry.place(x=150,y=501)
        self.passw_label.place(x=50,y=520)
        self.passw_entry.place(x=150,y=521)
        self.login_button.place(bordermode=OUTSIDE, x=360,y=500)
        self.signin_label.place(x=360,y=525)
        self.delete_account_label.place(x=0,y=0)
        #
        self.login_window.mainloop()

    def signinButton(self):
        sigin = SignInGUI()

    def loginButton(self):
        cursor.execute("select idUser,username,password from login where username=%s and password=%s",(self.login_entry.get(),self.passw_entry.get(),))
        connection.commit()
        rows = cursor.fetchall()
##        try:
        if rows[0][0]:
            op = messagebox.showinfo('Aviso','Login efetuado com sucesso.')
            if op:
                current_profile.set(f'{int(rows[0][0])}')
                current_name.set(f'{rows[0][1]}')
                self.login_window.destroy()
                network = networkGUI()
##        except:
##            messagebox.showerror('Error','Algo deu errado. Verifique se a senha está incorreta ou a conta é inexistente.')

    def delete_account(self):
        delete = deleteGUI()
        
class networkGUI:
    def __init__(self):
        #Window
        self.network_window = Tk()
        self.network_window.title('Finder - Login')
        self.network_window.geometry('588x565')
        self.network_window.resizable(width=False,height=False)
        self.network_window['bg'] = 'green'
        #
        nome = StringVar()
        cpf = StringVar()
        telefone = StringVar()
        endereco = StringVar()
        ndepescados = StringVar()
        maiorpescado = StringVar()
        cursor.execute(f"select userinfo.nome,userinfo.cpf,userinfo.telefone,userinfo.endereco from userinfo where userinfo.idUser = {current_profile.get()}")
        connection.commit()
        rows = cursor.fetchall()
        nome.set(f'{rows[0][0]}')
        cpf.set(f'{rows[0][1]}')
        telefone.set(f'{rows[0][2]}')
        endereco.set(f'{rows[0][3]}')
        
        self.profile_pic = tkinter.PhotoImage(file="default.png")
        self.picframe = Label(self.network_window, image = self.profile_pic,bg='white')

        self.ranking_amount_label = Label(self.network_window,justify=LEFT,text=f'Líderes (Qtd):\nPrimeiro\nSegundo\nTerceiro',bg='green',fg='white')
        self.ranking_weight_label = Label(self.network_window,justify=LEFT,text=f'Líderes (Peso):\nPrimeiro\nSegundo\nTerceiro',bg='green',fg='white')

        self.g_medal = tkinter.PhotoImage(file="g_medal.png")
        self.g_medalframe = Label(self.network_window, image = self.g_medal,bg='green')
        self.g_medalframe1 = Label(self.network_window, image = self.g_medal, bg='green')
        
        self.s_medal = tkinter.PhotoImage(file="s_medal.png")
        self.s_medalframe = Label(self.network_window, image = self.s_medal,bg='green')
        self.s_medalframe1 = Label(self.network_window, image = self.s_medal, bg='green')

        self.b_medal = tkinter.PhotoImage(file="b_medal.png")
        self.b_medalframe = Label(self.network_window, image = self.b_medal,bg='green')
        self.b_medalframe1 = Label(self.network_window, image = self.b_medal, bg='green')
        
        self.update_userinfo = Button(self.network_window,width=37,height=2,text='Alterar informações de usuário',command = self.update_info)
        self.new_post = Button(self.network_window, width=42,height=2,text='Nova publicação')

        self.hello_label = Label(self.network_window,text=f"Bem-vindo, {current_name.get().upper()}!",bg='green',fg='white')
        self.hello_label.config(font=('Terminal','20'))

        self.about_me = Label(self.network_window,justify=LEFT,text=f'Sobre mim\nNome completo: {nome.get()}\nCPF: {cpf.get()}\nTelefone: {telefone.get()}\nEndereço: {endereco.get()}',bg='green',fg='white')

        self.scrollbar = Scrollbar(self.network_window, orient='vertical')    
        self.posts = Listbox(self.network_window, width=94,height=15,yscrollcommand = self.scrollbar.set)
        self.scrollbar.place(x=570,y=300, relheight=0.432)
        self.scrollbar.config(command = self.posts.yview)
        
        self.logged_has_label= Label(self.network_window,bg='green',fg='white',text=f'Conectado como {current_name.get()}, clique para sair.')
        self.logged_has_label.bind('<Button-1>', lambda e: self.logout())
        self.refresh_label = Label(self.network_window,bg='green',fg='white',text='Refresh')
        self.refresh_label.bind('<Button-1>', lambda e: self.refresh())
        
        self.picframe.place(x=4,y=0)
        self.hello_label.place(x=280,y=5)
        self.about_me.place(x=280,y=35)

        self.ranking_amount_label.place(x=325,y=168)
        self.ranking_weight_label.place(x=471,y=168)
        self.g_medalframe.place(x=309,y=185)
        self.g_medalframe1.place(x=455,y=185)
        self.s_medalframe.place(x=309,y=200)
        self.s_medalframe1.place(x=455,y=200)
        self.b_medalframe.place(x=309,y=215)
        self.b_medalframe1.place(x=455,y=215)
        
        self.update_userinfo.place(x=4,y=250)
        self.new_post.place(x=280,y=250)

        self.posts.place(x=4,y=300)
        self.logged_has_label.place(x=0,y=545)
        self.refresh_label.place(x=540,y=545)
        #
        self.insert_posts()
        self.network_window.mainloop()

    def insert_posts(self):
        post_list=[]
        cursor.execute(f"select * from post order by idpost")
        connection.commit()
        rows = cursor.fetchall()
        if rows[0][0]:       
            dados = []
            cursor.execute(f"select post.idpost,conteudo,datetime,iduser,massa,tamanho,qtd from post inner join pescado on post.idpost = pescado.idpost order by post.idpost")
            connection.commit()
            data = cursor.fetchall()
            if data:
                for d in data:
                    dados.append('pescado')
                    dados.append(d)
                    post_list.append(dados)
                    dados=[]
            cursor.execute(f"select post.idpost,conteudo,post.datetime,iduser,endereco,pescaria.datetime from post inner join pescaria on post.idpost = pescaria.idpost order by post.idpost")
            connection.commit()
            data = cursor.fetchall()
            if data:
                for d in data:
                    dados.append('pescaria')
                    dados.append(d)
                    post_list.append(dados)
                    dados=[]
        else:
            pass
        
        for x in post_list:
            if x[0] == 'pescado':
                self.posts.insert("end",f"ID:{x[1][3]} disse: {x[1][1]} - {x[1][2]} - Massa: {x[1][4]} - Tamanho: {x[1][5]} - Qtd: {x[1][6]}")
            else:
                self.posts.insert("end",f"[Pescaria] ID:{x[1][3]} marcou: {x[1][1]} - {x[1][4]} - {x[1][5]}")
            
 

    def update_info(self):
        update = update_userinfo()

    def logout(self):
        self.network_window.destroy()
        login = LoginGUI()
        
    def refresh(self):
        self.network_window.destroy()
        network = networkGUI()

class update_userinfo(networkGUI):
    def __init__(self):
        self.update_userinfo_window = Toplevel()
        self.update_userinfo_window.title('')
        self.update_userinfo_window.geometry('190x200')
        self.update_userinfo_window.resizable(width=False,height=False)
        self.update_userinfo_window['bg'] = 'black'
        #
        self.update_name_label = Label(self.update_userinfo_window,text='Nome',bg='black',fg='white')
        self.update_name_entry = Entry(self.update_userinfo_window,width=20)
        self.update_cpf_label = Label(self.update_userinfo_window,text='CPF',bg='black',fg='white')
        self.update_cpf_entry = Entry(self.update_userinfo_window,width=20)
        self.update_phone_label = Label(self.update_userinfo_window,text='Telefone',bg='black',fg='white')
        self.update_phone_entry = Entry(self.update_userinfo_window,width=20)
        self.update_address_label = Label(self.update_userinfo_window,text='Endereço',bg='black',fg='white')
        self.update_address_entry = Entry(self.update_userinfo_window,width=20)
        self.update_password_label = Label(self.update_userinfo_window,text='Senha',bg='black',fg='white')
        self.update_password_entry = Entry(self.update_userinfo_window,width=20,show='*')
        self.advice_label = Label(self.update_userinfo_window,text='Caso não queira alterar um dado,\n repita-o na entrada.',bg='black',fg='yellow')
        self.update_account_button = Button(self.update_userinfo_window,width=25,text='Alterar dados', command = self.update_account_button)
        #
        self.update_name_label.grid(row=2,column=0)
        self.update_name_entry.grid(row=2,column=1)
        self.update_cpf_label.grid(row=3,column=0)
        self.update_cpf_entry.grid(row=3,column=1)
        self.update_phone_label.grid(row=4,column=0)
        self.update_phone_entry.grid(row=4,column=1)
        self.update_address_label.grid(row=5,column=0)
        self.update_address_entry.grid(row=5,column=1)
        self.update_password_label.grid(row=6,column=0)
        self.update_password_entry.grid(row=6,column=1)
        self.advice_label.place(x=3,y=110)
        self.update_account_button.place(x=3,y=155)
        #
        self.update_userinfo_window.mainloop()        

    def update_account_button(self):
        upd_passw = self.update_password_entry.get()
        upd_name = self.update_name_entry.get()
        upd_cpf = self.update_cpf_entry.get()
        upd_phone = self.update_phone_entry.get()
        upd_address = self.update_address_entry.get()
        if len(upd_passw)==0 or len(upd_name)==0 or len(upd_cpf)==0 or len(upd_phone)==0 or len(upd_address)==0:
            messagebox.showinfo('Error','Algo deu errado. Verifique todos os campos e tente novamente.')
            return
        else:
            cursor.execute(f"update userinfo set nome='{upd_name}',endereco='{upd_address}',telefone='{upd_phone}',cpf='{upd_cpf}' where idUser={current_profile.get()}")
            connection.commit()
            cursor.execute(f"update login set password='{upd_passw}' where idUser={current_profile.get()}")
            connection.commit()
            ok = messagebox.showinfo('Succesful','Dados alterados com sucesso. AS ALTERAÇÕES SERÃO PERCEBIDAS SOMENTE APÓS UM REFRESH.')
            if ok:
                self.update_userinfo_window.destroy()

class deleteGUI:
    def __init__(self):
        self.delete_window = Toplevel()
        self.delete_window.title('')
        self.delete_window.geometry('160x75')
        self.delete_window.resizable(width=False,height=False)
        self.delete_window['bg'] = 'black'

        self.DEL_login_label = Label(self.delete_window, text='Login', bg='black', fg='white')
        self.DEL_login_entry = Entry(self.delete_window, width=18)
        self.DEL_passw_label = Label(self.delete_window, text='Senha', bg='black', fg='white')
        self.DEL_passw_entry = Entry(self.delete_window, show='*', width=18)

        self.DEL_login_button = Button(self.delete_window, width=11, text='Deletar', command=self.deleteDATA)
        
        self.DEL_login_label.grid(row=0,column=0)
        self.DEL_login_entry.grid(row=0,column=1)
        self.DEL_passw_label.grid(row=1,column=0)
        self.DEL_passw_entry.grid(row=1,column=1)
        self.DEL_login_button.grid(row=2,column=1)

        self.delete_window.mainloop()

    def deleteDATA(self):
        cursor.execute("select idUser,username,password from login where username=%s and password=%s",(self.DEL_login_entry.get(),self.DEL_passw_entry.get(),))
        connection.commit()
        rows = cursor.fetchall()
##        try:
        if rows[0][0]:
            yesno = messagebox.askyesno('Warning','Tem certeza que deseja deletar sua conta?\nEssa ação não pode ser desfeita.')
            if yesno == True:
                cursor.execute("delete from pescado,pescaria,post,userinfo,login where idUser = %s",(rows[0][0],))
                connection.commit()
                cursor.execute("delete from login where idUser = %s",(rows[0][0],))
                connection.commit()
                messagebox.showinfo('','A conta foi excluída.')
                return
            else:
                return
##        except:
##            messagebox.showerror('Error','Senha incorreta ou conta inexistente.')

login = LoginGUI()

if not login:
        cursor.close()
        connection.close()
    
