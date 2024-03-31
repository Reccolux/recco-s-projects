from flask import Flask, render_template, request
import json
from datetime import datetime
app = Flask(__name__)

g_user = ""
conv=[]
actconvresult = ''
dic_themes = {"theme_1":{"princ":("#00e8ff","#740cb8","#f300ff"),'ombre':'#bd07da','input':'#5e539a','mess':['#680B8A','#D363FC']},"theme_2":{"princ":("#FA6402","#FAE704","#F54640"),'ombre':'#FD8F01','input':'#D1882A','mess':['#E74A10','#F99831']},"theme_3":{'princ':('#4AE19F','#0DDE49','#53ECD7'),'ombre':'#81F336','input':'#73BD42','mess':['#3DAB09','#89F041']}}

def read(fichier):
  """retourne les données d'un fichier json"""
  with open(fichier, 'r',encoding="utf8",errors='ignore') as fichier_lu:
    data = json.load(fichier_lu)
  return data

def remplacer(data,fichier):
  """modifie et renvoie les données d'un fichier json """
  with open(fichier,"w",encoding="utf8",errors='ignore') as new_fichier:
    new_fichier.truncate(0)
    json.dump(data,new_fichier,ensure_ascii=False)


def add(user, mdp, fichier = "comptes.json"):
  """ajoute une clé(user/mdp) dans le comptes.json"""
  data = read(fichier)
  data[user] = mdp
  remplacer(data,fichier)

def afficher_contacts(fichier="conversation.json"):
  """affiche la liste des contacts"""
  global autreconctact
  autreconctact = []
  data = read(fichier)
  liste_boutons=""
  tab_date_mess = []
  compt=0
  for loop in data:
    tab_interlocs=[]
    nom_contact = ""
    interlocs_separes =""
    test = loop.split('@')
    for i in range(len(test)):
      if g_user==test[i]:
        for x in range(len(test)):
          if x!=i:
            tab_interlocs.append(test[x])
        break
    for t in range(len(tab_interlocs)):
      nom_contact +=tab_interlocs[t]
      interlocs_separes += tab_interlocs[t]
      if t!=len(tab_interlocs)-1:
        interlocs_separes+="@"
      autreconctact.append(interlocs_separes)
      liste_boutons=" <button class='bouton_conv'  id="+interlocs_separes+"  >"+nom_contact+"</button> <br> <script> contenant  = document.getElementById('contenu') \n tabs = contenant.getElementsByTagName('button')\n tabs"
    if g_user==test[i]:
      if len(data[loop])>=1:
        for v in data[loop].keys():
          if v.split(";")[1] == str(len(data[loop])):
            tab_date_mess.append((v.split(";")[2], liste_boutons))
      else:

        tab_date_mess.append(("2023-05-20 00:00:00.878011",liste_boutons))


  tab_date_mess.sort(reverse = True)

  contacts = ""
  for i in tab_date_mess:
    contacts += i[1]+'['+str(compt)+"].addEventListener('click', onClick);</script>"
    compt+=1
  print(autreconctact,"AAAAAAAAAAAAARg")
  return contacts

def afficher_contacts_crea(fichier="conversation.json"):
  """affiche les contacts (checkbox) pour creation groupe"""
  global conv
  data = read(fichier)
  liste_boutons=""
  tab_date_mess = []
  compt=0
  for loop in data:
    if g_user==loop.split("@")[0]:
      nom_contact = loop.split("@")[1]
      conv.append(nom_contact)
      if len(loop.split("@")) <=2:
        liste_boutons= "<input type='checkbox' id="+nom_contact+"> <label class='titre' for='pizza'>Ajouter "+nom_contact+"</label>"
        if len(data[loop])>=1:
          for v in data[loop].keys():
            if v.split(";")[1] == str(len(data[loop])):
              tab_date_mess.append((v.split(";")[2], liste_boutons))
        else:
          tab_date_mess.append(("2023-05-20 00:00:00.878011",liste_boutons))

    elif g_user==loop.split("@")[1]:
      nom_contact= loop.split("@")[0]
      conv.append(nom_contact)
      if len(loop.split('@'))<=2:
        liste_boutons= "<input type='checkbox' id="+nom_contact+"> <label class='titre' for='pizza'>Ajouter "+nom_contact+"</label>"

        if len(data[loop])>=1:
          for v in data[loop].keys():
            if v.split(";")[1] == str(len(data[loop])):
              tab_date_mess.append((v.split(";")[2], liste_boutons))
        else:
          tab_date_mess.append(("2023-05-20 00:00:00.878011",liste_boutons))


  tab_date_mess.sort(reverse = True)

  contacts = ""
  for i in tab_date_mess:
    contacts += i[1]
    compt+=1


  return contacts 
def afficher_mess(other_user,fichier="conversation.json"):
  "afficher les messages de la conversation selectionée"
  data = read(fichier)
  other_user = other_user.split("@")
  div_mess = "<div id='div_mess'>"
  for cle,valeur in data.items():
    verif=0
    if g_user in cle and len(other_user)+1==len(cle.split('@')):
      for loop in other_user:
        if loop not in cle:
          verif=1
          break
      if verif != 1:
        for nom, mess in valeur.items():
          if nom.split(';')[0] == g_user:
            div_mess+= "<div class='div_mess' ><div class = 'message_droite'> <p class='p_droite'>"+mess+"</p></div> </div> "
          else:
            div_mess+= "<div class='div_mess' ><div class = 'message_gauche'><p class='p_gauche'>"+mess+"</p></div> </div>"
  div_mess+="</div>"

  return div_mess

  

def recherche_conv(u1,other_user,fichier):
  """recherche de conversation"""
  data = read(fichier)
  other_user = other_user.split("@")
  compt= 0
  other_user.insert(0,u1)
  for cle in data.keys():
    test = 0
    if len(cle.split("@")) == len(other_user):
      for loop in other_user:
        if loop not in cle:
          test =1
      if test == 0:
        return cle,data[cle]


def send(u1,other_user,message,fichier):
  """ajoute un message dans la conversation avec u1 = utilisateur actuel"""
  data = read(fichier)
  conv = recherche_conv(u1,other_user,fichier)[1]
  conv[u1+";"+str(len(conv)+1)+";"+str(datetime.now())] = message
  data[recherche_conv(u1,other_user,fichier)[0]]=conv
  remplacer(data,fichier)

def lstoption_users(u1=g_user,fichier='comptes.json'):
  global autreconctact
  data=read(fichier)
  a=''
  for loop in data.keys():
    print("1. ", loop)
    if loop!=g_user and loop not in autreconctact:
      a+= "<option value="+loop+">"
  print(a)
  return a


#----------------------REDIRECTIONS----------------------#


@app.route("/")#Démarrage | racine du site
def index ():
  return render_template("index.html")

@app.route("/accueil", methods = ["POST"]) #redirection vers l'accueil(creer/connection d'un compte)
def accueil():
    global g_user, dic_themes
    data = read("comptes.json")
    result = request.form
    user,mdp = result["username"],result["password"]
    valeur = result["valeur"]

    if valeur == "CREER":
      for lettre in user:
        if lettre == "@" or lettre == ";":
          return render_template("index.html", erreur = "<div id = 'err' class = 'erreur'><p class = 'mess_err'>Caractère problématique</p></div>")
      confirm = result["confirm"]
      if user in data.keys():
        return render_template("index.html", erreur = "<div id = 'err' class = 'erreur'><p class = 'mess_err'>Cet utilisateur existe déjà</p></div>")
      else:
        if mdp == confirm:
          add(user,mdp)
          g_user = user
          pref = read('preferences.json')
          pref[g_user] = {'clarte':'sombre','theme':'theme_1'}
          remplacer(pref,'preferences.json')
          theme =  dic_themes[pref[g_user]['theme']]
          return render_template("accueil.html",conversation = afficher_contacts(),fond=pref[g_user]['clarte'],princ_1=theme['princ'][0],princ_2=theme['princ'][1],princ_3=theme['princ'][2],b_input=theme['input'],ombre=theme['ombre'],mess_g=theme['mess'][0],mess_d=theme['mess'][1],usersforauto=lstoption_users())
        return render_template("index.html",erreur = "<div id = 'err' class = 'erreur'><p class = 'mess_err'>Mauvaise confirmation</p></div>")

    elif valeur == "CONNECTER":
      if user in data.keys():
        if data[user] == mdp:
          g_user = user
          pref = read('preferences.json')[g_user]
          theme = dic_themes[pref['theme']]
          return render_template("accueil.html",conversation = afficher_contacts(),fond = pref['clarte'],princ_1=theme['princ'][0],princ_2=theme['princ'][1],princ_3=theme['princ'][2],b_input=theme['input'],ombre=theme['ombre'],mess_g=theme['mess'][0],mess_d=theme['mess'][1],usersforauto=lstoption_users())
        else:
          return render_template("index.html", erreur = "<div id = 'err' class = 'erreur'><p class = 'mess_err'>Mot de passe incorrect</p></div>")
      else:
        return render_template("index.html", erreur = "<div id = 'err' class = 'erreur'><p class = 'mess_err'>Ce compte n'existe pas</p></div>")

@app.route("/appliquer", methods = ["GET"])
def appliquer():
  global g_user, dic_themes
  pref = read("preferences.json")
  pref[g_user]['clarte'] = request.args["clarte"]
  pref[g_user]['theme'] = request.args["theme"]
  remplacer(pref,"preferences.json")
  theme = dic_themes[pref[g_user]['theme']]
  clarte = pref[g_user]['clarte']
  return render_template("accueil.html",conversation=afficher_contacts(),fond = clarte,princ_1=theme['princ'][0],princ_2=theme['princ'][1],princ_3=theme['princ'][2],b_input=theme['input'],ombre=theme['ombre'],mess_g=theme['mess'][0],mess_d=theme['mess'][1],usersforauto=lstoption_users())

@app.route("/settings", methods = ["POST"])# redirection inutile pour l'instant vers les parametres
def settings():
  global g_user,dic_themes
  pref = read('preferences.json')[g_user]
  check = ''
  cl = 'p_clair'
  if pref['clarte'] == 'sombre':
    check = 'checked'
    cl = 'p_sombre'
  bouton = "<input type='checkbox' id = 'clarte' onclick = 'changerClarte()'"+check+"/>"
  theme = dic_themes[pref['theme']]
  return render_template("parametres.html",fond = pref['clarte'], switch = bouton, cl = cl,princ_1=theme['princ'][0],princ_2=theme['princ'][1],princ_3=theme['princ'][2],ombre=theme['ombre'])

@app.route("/envoi", methods = ["POST"])#refresh --> envoi message
def envoi():
  global actconvresult, g_user,dic_themes
  resultin = request.form
  message = resultin["mess"]
  send(g_user,actconvresult,message,"conversation.json")
  theme = dic_themes[read('preferences.json')[g_user]['theme']]
  return render_template("accueil.html",conv_act=afficher_mess(actconvresult), conversation=afficher_contacts(),champsmess="<form action = 'envoi' method = 'post'id='form_input_envoi'><input id='input_mess' name = 'mess' placeholder='Saisissez un message...' autofocus/><button class='bouton_input' type = 'submit'>ENVOI</button></form>",autre = actconvresult,fond = read('preferences.json')[g_user]['clarte'],princ_1=theme['princ'][0],princ_2=theme['princ'][1],princ_3=theme['princ'][2],b_input=theme['input'],ombre=theme['ombre'],mess_g=theme['mess'][0],mess_d=theme['mess'][1],usersforauto=lstoption_users())

@app.route("/convac",methods=["GET"])#refresh --> affiche la conversation cliquée
def convac():
  global actconvresult,dic_themes
  actconvresult = request.args["param"]
  theme = dic_themes[read('preferences.json')[g_user]['theme']]
  return render_template("accueil.html",conv_act=afficher_mess(actconvresult),conversation=afficher_contacts(),champsmess="<form action = 'envoi' method = 'post'id='form_input_envoi'><input id='input_mess' name = 'mess' placeholder='Saisissez un message...' autofocus/><button class='bouton_input' type = 'submit'>ENVOI</button></form>",autre = actconvresult,fond = read('preferences.json')[g_user]['clarte'],princ_1=theme['princ'][0],princ_2=theme['princ'][1],princ_3=theme['princ'][2],b_input=theme['input'],ombre=theme['ombre'],mess_g=theme['mess'][0],mess_d=theme['mess'][1],usersforauto=lstoption_users())

@app.route("/ajout", methods = ["POST"])#refresh --> ajoute un contact
def ajout():
  global g_user,dic_themes
  data = read("conversation.json")
  users = read("comptes.json")
  new_contact = request.form["entrer_ajout"]
  theme = dic_themes[read('preferences.json')[g_user]['theme']]
  if new_contact in users.keys():
    data[g_user + "@" + new_contact] = {}
    remplacer(data, 'conversation.json')
    return render_template("accueil.html",conversation=afficher_contacts(),champsmess="<form action = 'envoi' method = 'post' id='form_input_envoi'><input id='input_mess' name = 'mess'placeholder='Saisissez un message...'/><button class='bouton_input' type = 'submit'>ENVOI</button></form>",fond = read('preferences.json')[g_user]['clarte'],princ_1=theme['princ'][0],princ_2=theme['princ'][1],princ_3=theme['princ'][2],b_input=theme['input'],ombre=theme['ombre'])
  return render_template("accueil.html",conversation = afficher_contacts(),erreur ="<p>Utilisateur introuvable</p>",autre = new_contact,fond = read('preferences.json')[g_user]['clarte'],princ_1=theme['princ'][0],princ_2=theme['princ'][1],princ_3=theme['princ'][2],b_input=theme['input'],ombre=theme['ombre'],mess_g=theme['mess'][0],mess_d=theme['mess'][1],usersforauto=lstoption_users())

@app.route("/creer_grp", methods=["post"])#redirection vers creer_grp.html pour selectionner les contacts à ajouter dans le groupe 
def creer_grp():
  global dic_themes
  theme = dic_themes[read('preferences.json')[g_user]['theme']]
  return render_template("creer_grp.html", case_cocher=afficher_contacts_crea(),fond = read('preferences.json')[g_user]['clarte'],princ_1=theme['princ'][0],princ_2=theme['princ'][1],princ_3=theme['princ'][2],b_input=theme['input'],ombre=theme['ombre'])

@app.route("/creergrp", methods=["GET"])#redirection vers accueil + créer le groupe
def creer():
  global dic_themes
  data = read("conversation.json")
  users = read("comptes.json")
  contacts = request.args['newgrp']
  data[g_user+"@"+contacts] = {}
  remplacer(data, 'conversation.json')
  theme = dic_themes[read('preferences.json')[g_user]['theme']]
  return render_template("accueil.html",conversation=afficher_contacts(),fond = read('preferences.json')[g_user]['clarte'],princ_1=theme['princ'][0],princ_2=theme['princ'][1],princ_3=theme['princ'][2],b_input=theme['input'],ombre=theme['ombre'],usersforauto=lstoption_users())

@app.route("/deconnexion",methods = ["POST"])# redirection vers accueil 
def deconnexion():
  return render_template("index.html")

@app.route('/retour',methods=["GET"])
def retour():
  global dic_themes
  theme = dic_themes[read('preferences.json')[g_user]['theme']]
  return render_template('accueil.html',conversation=afficher_contacts(),fond = read('preferences.json')[g_user]['clarte'],princ_1=theme['princ'][0],princ_2=theme['princ'][1],princ_3=theme['princ'][2],b_input=theme['input'],ombre=theme['ombre'],mess_g=theme['mess'][0],mess_d=theme['mess'][1],usersforauto=lstoption_users())



if __name__ == "__main__":
    app.run(host='127.0.0.1',debug=True)
