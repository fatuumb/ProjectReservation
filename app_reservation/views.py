from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
from .models import Utilisateur
import mysql.connector as sql
from datetime import datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.hashers import make_password,check_password

config = {
    'user': 'fatou',
    'password': 'SEYnabou16',
    'host': 'localhost',
    'database': 'bd_app'
}
# Établir une connexion à la base de données
conn = sql.connect(**config)
cursor = conn.cursor()
nom,prenom,email,telephone,adresse,mot_de_passe='','','','','',''
# Create your views here.
def index(request):

    return render(request, 'index.html',  {})
    
    

def connexion(request):
    if request.method=="POST":
        message=''
        email = request.POST.get('email')
        mot_de_passe = request.POST.get('mot_de_passe')
        if(email!='' and mot_de_passe!=''): 
            try:
                message=''
                conn = sql.connect(**config)
                cursor = conn.cursor()
                requete="select * from app_reservation_utilisateur where  email='{}' and  BINARY  mot_de_passe='{}'".format(email,mot_de_passe)
                cursor.execute(requete)
                res=cursor.fetchall()
                if res==[]:
                    message='Login ou mot de passe incorrect'
                    cursor.close()
                    conn.close()
                    return render(request, 'erreur.html', {})
                    
                else :
                    keys = ['id', 'nom', 'prenom', 'adresse', 'email', 'telephone']
                    result = dict(zip(keys, res[0]))
                    result['estConnecte'] = True
                    cursor.close()
                    conn.close()
                    # Stocker le dictionnaire dans la session
                    request.session['info_utilisateur'] = result
                    url_precedente = request.META.get('HTTP_REFERER')                                                                                                       #     return redirect('index')
                    return redirect('index')
                
            except Exception as e:
                print(str(e))  # Afficher l'erreur pour le débogage
                return render(request, 'erreur.html', {})
    else:
        context = {
        'variable': 'Contenu dynamique'
        }
        return render(request, 'connexion.html', context)


def inscription(request):
    if request.method=="POST":
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email_user = request.POST.get('email')
        telephone = request.POST.get('telephone')
        adresse = request.POST.get('adresse')
        mot_de_passe = request.POST.get('mot_de_passe')
        hash_mdp=make_password(mot_de_passe)
        print(hash_mdp)
        try:
            conn = sql.connect(**config)
            cursor = conn.cursor()
            requete="insert into app_reservation_utilisateur (id,nom,prenom,adresse,email,telephone,mot_de_passe) values (NULL,'{}','{}','{}','{}','{}','{}')".format(nom,prenom,adresse,email_user,telephone,mot_de_passe)
            cursor.execute(requete)
            conn.commit()
            subject = 'Bienvenue sur notre site'
            html_message = render_to_string('bienvenue.html', {'user_email': email_user})
            plain_message = strip_tags(html_message)
            email = EmailMultiAlternatives(subject, plain_message, to=[email_user])
            email.attach_alternative(html_message, "text/html")
            email.send()
            cursor.close()
            conn.close()
            return redirect('connexion')  
        except Exception as e:
            print(str(e)) 
            return render(request, 'erreur.html', {})
    else:
        context = {
        'variable': 'Contenu dynamique'
        }
        return render(request, 'inscription.html', context)


def resultat(request):
    if 'hotel_info' in request.session:

        if request.POST.get('lieu')!= request.session['hotel_info']['lieu'] and request.POST.get('lieu') :
            lieu = request.POST.get('lieu')
        else: 
            lieu = request.session['hotel_info']['lieu']

        if request.POST.get('date_reservation') != request.session['hotel_info']['arrivee'] and request.POST.get('date_reservation') :
            date_reservation  = request.POST.get('date_reservation')
        else: 
            date_reservation = request.session['hotel_info']['arrivee']

        if request.POST.get('date_restitution') != request.session['hotel_info']['depart'] and request.POST.get('date_restitution') :
            date_restitution  = request.POST.get('date_restitution')
        else: 
            date_restitution = request.session['hotel_info']['depart']

        if request.POST.get('nombre') != request.session['hotel_info']['nombre'] and request.POST.get('nombre') :
            nombre  = request.POST.get('nombre')
        else: 
            nombre = request.session['hotel_info']['nombre']
              
        
    else:
       
        lieu  = request.POST.get('lieu')
        date_reservation  = request.POST.get('date_reservation')
        date_restitution  = request.POST.get('date_restitution')
        nombre  = request.POST.get('nombre')
    
    try:
        message=''
        conn = sql.connect(**config)
        cursor = conn.cursor()
        requete="SELECT h.id_hotel, h.nom, h.code_pays,h.ville,h.photo, MIN(c.prix) AS prix FROM app_reservation_chambre c INNER JOIN app_reservation_hotel h ON c.hotel_id = h.id_hotel WHERE h.ville LIKE '%{}%' or h.nom LIKE '%{}%' GROUP BY h.id_hotel;' ".format(lieu,lieu)
        cursor.execute(requete)
        res=cursor.fetchall()
        if res==[]:
            request.session['hotel_info'] = {
                'lieu':lieu,
                'arrivee':date_reservation,
                'depart':date_restitution,
                'nombre':nombre
            }
            return render(request, 'resultat.html', {})
            
        else :
            resultats=[]
            keys = ['id', 'nom', 'code','ville','photo','prix']
            for i in res:
                result = dict(zip(keys, i))
                resultats.append(result)
            liste_hotels = {item['id']: {'nom': item['nom'], 'code': item['code'],'ville': item['ville'],'photo': item['photo'],'prix': item['prix']} for item in resultats}
            context = {'liste_hotels': liste_hotels}
            cursor.close()
            conn.close()
            # Stocker le dictionnaire dans la session
            request.session['hotel_info'] = {
                'lieu':lieu,
                'arrivee':date_reservation,
                'depart':date_restitution,
                'nombre':nombre
            }
            
            return render(request, 'resultat.html', context)
        
    except Exception as e:
        print(str(e))  
        return render(request, 'erreur.html', {})


def chambre(request):
    
    id_hotel  = request.POST.get('id_hotel')
    request.session['id_hotel']=request.POST.get('id_hotel')
    date_reservation = request.session['hotel_info']['arrivee']
    date_restitution  = request.session['hotel_info']['depart']
    print(date_restitution)
    try:
        conn = sql.connect(**config)
        cursor = conn.cursor()
        requete1="select * from app_reservation_hotel where id_hotel='{}' ".format(id_hotel)
        cursor.execute(requete1)
        res=cursor.fetchall()
        keys = ['id', 'nom', 'code','ville','photo']
        hotel = dict(zip(keys, res[0]))
       
        context = {
                'hotel': hotel,
                }
        requete2="SELECT * FROM app_reservation_chambre WHERE hotel_id = '{}' AND id NOT IN ( SELECT chambre_id FROM app_reservation_reservations_hotel WHERE date_reservation >= '{} 00:00:00.000000' AND date_restitution <= '{} 00:00:00.000000' ); ".format(id_hotel,date_reservation,date_restitution)
        cursor.execute(requete2)
        res=cursor.fetchall()
        if res==[]:
            return render(request, 'chambre.html', context)
            
        else :
            resultats=[]
            keys = ['id', 'type', 'description','prix','nombre','photo']
            for i in res:
                result = dict(zip(keys, i))
                resultats.append(result)
            liste_chambre = {item['id']: { 'type': item['type'],'description': item['description'],'prix': item['prix'],'nombre': item['nombre'],'photo': item['photo']} for item in resultats}
            context = {'hotel': hotel,'liste_chambre': liste_chambre}
            cursor.close()
            conn.close()
            return render(request, 'chambre.html', context)
        
    except Exception as e:
        print(str(e))  # Afficher l'erreur pour le débogage
        return render(request, 'erreur.html', {})


def deconnexion(request):
    # Supprimer la session
    request.session.flush()
    return redirect(index)

def reservation(request):
    id_chambre  = request.POST.get('id_chambre')
    if 'info_utilisateur' in request.session:
        info_utilisateur = request.session['info_utilisateur']
        if 'id' in info_utilisateur:
            id_user = info_utilisateur['id']
    if 'hotel_info' in request.session:
        arrivee = request.session['hotel_info']['arrivee']
        arrivee_datetime = datetime.strptime(arrivee, '%Y-%m-%d').replace(hour=0, minute=0, second=0)
        depart = request.session['hotel_info']['depart']
        depart_datetime = datetime.strptime(depart, '%Y-%m-%d').replace(hour=0, minute=0, second=0)
    try:
        message=''
        conn = sql.connect(**config)
        cursor = conn.cursor()
        requete="INSERT INTO app_reservation_reservations_hotel (id, date_reservation, date_restitution, chambre_id, utilisateur_id,paiement) VALUES (NULL, '{}', '{}', '{}', '{}',0);".format(arrivee_datetime,depart_datetime,int(id_chambre),int(id_user))
        cursor.execute(requete)
        # Valider les modifications
        conn.commit()
        cursor.execute("SELECT * FROM `app_reservation_reservations_hotel` ORDER BY id DESC LIMIT 1;")
        res=cursor.fetchall()
        keys = ['id', 'arrivee', 'depart', 'id_chambre']
        reservations = dict(zip(keys, res[0]))
        cursor.execute(" SELECT * FROM app_reservation_chambre WHERE id = '{}' ".format(reservations['id_chambre']))
        res=cursor.fetchall()
        keys = ['id', 'type', 'desc','prix', 'nombre']
        chambre = dict(zip(keys, res[0]))
        context = {
                'reservation': reservations,
                'chambre':chambre
                }
        cursor.close()
        conn.close()
        if 'info_utilisateur' in request.session:
            info_utilisateur = request.session['info_utilisateur']
            if 'email' in info_utilisateur:
                email_user = info_utilisateur['email']
                subject = 'Reservation de chambre'
                html_message = render_to_string('confirmation.html', {'user_email': email_user})
                plain_message = strip_tags(html_message)

                email = EmailMultiAlternatives(subject, plain_message, to=[email_user])
                email.attach_alternative(html_message, "text/html")
                email.send()
        return render(request, 'reservation.html', context)
    except Exception as e:
        print(str(e))  
        return render(request, 'erreur.html',{})


def paiement(request):
    id_reservation  = request.POST.get('id_reservation')
    type_reservation= request.POST.get('type_reservation')
    return render(request,'paiement.html',{'id_reservation' :id_reservation,'type_reservation' :type_reservation})


def mes_reservations(request):
    print(request.session['info_utilisateur'])
    if 'info_utilisateur' in request.session:
        info_utilisateur = request.session['info_utilisateur']

        if 'id' in info_utilisateur:
            id_user = info_utilisateur['id']
    try:
        liste_chambre,liste_voiture,liste_vol={},{},{}
        conn = sql.connect(**config)
        cursor = conn.cursor()
        #Recuperer les chambres
        cursor.execute("SELECT * FROM `app_reservation_reservations_hotel` where utilisateur_id ='{}' ".format(id_user))
        res=cursor.fetchall()
        if res!=[]:
            resultats=[]
            keys = ['id', 'arrivee', 'depart','user','chambre','paiement']
            for i in res:
                result = dict(zip(keys, i))
                resultats.append(result)
            liste_chambre = {item['id']: { 'arrivee': item['arrivee'],'depart': item['depart'],'paiement': item['paiement']} for item in resultats}
        #Recuperer les voitures
        cursor.execute("SELECT * FROM `app_reservation_location_voiture` where utilisateur_id ='{}' ".format(id_user))
        res=cursor.fetchall()
        print(res)
        if res!=[]:
            resultats=[]
            keys = ['id', 'arrivee', 'depart','user','voiture','paiement']
            for i in res:
                result = dict(zip(keys, i))
                resultats.append(result)
            liste_voiture = {item['id']: { 'arrivee': item['arrivee'],'depart': item['depart'],'paiement': item['paiement']} for item in resultats}
        #Recuperer les vols
        cursor.execute("SELECT * FROM `app_reservation_reservation_vol` where utilisateur_id ='{}' ".format(id_user))
        res=cursor.fetchall()
        if res!=[]:
            resultats=[]
            keys = ['id','user','vol','date','paiement']
            for i in res:
                result = dict(zip(keys, i))
                resultats.append(result)
            liste_vol = {item['id']: { 'vol': item['vol'],'date': item['date'],'paiement': item['paiement']} for item in resultats}
        context = {
            'chambre': liste_chambre,
            'voiture':liste_voiture,
            'vol':liste_vol
        }
        cursor.close()
        conn.close()
        return render(request,'mes_reservations.html',context)
    except Exception as e:
        print(str(e)) 
        return render(request,'erreur.html',{})
    

def annuler(request):
  
    id_reservation = request.POST.get('id_reservation')
    print(id_reservation)
    type_reservation= request.POST.get('type_reservation')
   
    try:
        conn = sql.connect(**config)
        cursor = conn.cursor()
        cursor.execute(" DELETE FROM `{}` WHERE `{}`.`id` = {} ".format(type_reservation,type_reservation, int(id_reservation)))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('mes_reservations')
    except Exception as e:
        print(str(e))  
        return render(request,'erreur.html',{})
    
def profil(request):

    return render(request,'profil.html',{})

def erreur(request):

    return render(request,'erreur.html',{})

def valider_paiement(request):
    id_reservation  = request.POST.get('id_reservation')
    type_reservation= request.POST.get('type_reservation')
    if 'info_utilisateur' in request.session:
        info_utilisateur = request.session['info_utilisateur']
        # if 'id' in info_utilisateur:
        #     id_user = info_utilisateur['id']
   
    try:
        print(id_reservation)
        conn = sql.connect(**config)
        cursor = conn.cursor()
        requete="UPDATE {} SET paiement = '1' WHERE {}.id = '{}';".format(type_reservation,type_reservation,id_reservation)
        cursor.execute(requete)
        # Valider les modifications
        conn.commit()
        cursor.close()
        conn.close()
        if 'info_utilisateur' in request.session:
            info_utilisateur = request.session['info_utilisateur']
            if 'email' in info_utilisateur:
                email_user = info_utilisateur['email']
                subject = 'Validation Paiement'
                html_message = render_to_string('validation.html', {'user_email': email_user})
                plain_message = strip_tags(html_message)
                email = EmailMultiAlternatives(subject, plain_message, to=[email_user])
                email.attach_alternative(html_message, "text/html")
                email.send()
        return redirect('mes_reservations')
    except Exception as e:
        print(str(e))  
        return render(request, 'erreur.html',{})



def car_list(request):
    if request.method =="POST":
        Lieulocation  = request.POST.get('Lieulocation')
        Datelocation  = request.POST.get('Datelocation')
        Retourlocation  = request.POST.get('Retourlocation')

        try:
            message=''
            conn = sql.connect(**config)
            cursor = conn.cursor()
            requete="select * from app_reservation_voiture where localisation LIKE '%{}%'  ".format(Lieulocation)
            cursor.execute(requete)
            res=cursor.fetchall()
            print(res)
            if res==[]:
                
                return render(request, 'car_list.html', {})
                
            else :
                resultats=[]
                keys = ['id', 'marque','modele','localisation','annee','type','prix', 'nombre_place','photo','disponible']
                for i in res:
                    result = dict(zip(keys, i))
                    resultats.append(result)
                liste_voiture= {item['id']: {'marque': item['marque'], 'modele': item['modele'],'localisation': item['localisation'],'annee': item['annee'],'type': item['type'],'prix': item['prix'],'nombre_place': item['nombre_place'],'photo': item['photo'],'disponible': item['disponible']} for item in resultats}
                inputs={
                    'lieu': Lieulocation,
                    'arrivee':Datelocation,
                    'depart':Retourlocation,  
                }
                request.session['voiture_info']={
                    'arrivee':Datelocation,
                    'depart':Retourlocation
                }
                context = {
                    'liste_voiture': liste_voiture,
                    'inputs':inputs
                    }
                cursor.close()
                conn.close()

                return render(request, 'car_list.html', context)
            
        except Exception as e:
            print(str(e)) 
            return render(request, 'erreur.html', {})



def voir_plus(request):
    id_voiture  = request.POST.get('id_voiture')
    print(id_voiture)
    try:
        message=''
        conn = sql.connect(**config)
        cursor = conn.cursor()
        requete="select * from app_reservation_voiture where id = {}  ".format(int(id_voiture))
        cursor.execute(requete)
        res=cursor.fetchall()
        print(res)
        if res==[]:
           
            return render(request, 'voir_plus.html', {})
            
        else :
            resultats=[]
            keys = ['id', 'marque','modele','localisation','annee','type','prix', 'nombre_place','photo','disponible']
            for i in res:
                result = dict(zip(keys, i))
                resultats.append(result)
            liste_voiture= {item['id']: {'marque': item['marque'], 'modele': item['modele'],'localisation': item['localisation'],'annee': item['annee'],'type': item['type'],'prix': item['prix'],'nombre_place': item['nombre_place'],'photo': item['photo'],'disponible': item['disponible']} for item in resultats}
            context = {'liste_voiture': liste_voiture}
            cursor.close()
            conn.close()
            
            return render(request, 'voir_plus.html', context)
        
    except Exception as e:
        print(str(e)) 
        return render(request, 'erreur.html', {})

   

def reservation_voiture(request):
    id_voiture  = request.POST.get('id_voiture')
    if 'info_utilisateur' in request.session:
        info_utilisateur = request.session['info_utilisateur']
        if 'id' in info_utilisateur:
            id_user = info_utilisateur['id']
    if 'voiture_info' in request.session:
        voiture_info = request.session['voiture_info']
        if 'arrivee' in voiture_info:
            arrivee = voiture_info['arrivee']
        if 'depart' in voiture_info:
            depart = voiture_info['depart']
    try:
        message=''
        conn = sql.connect(**config)
        cursor = conn.cursor()
        requete="INSERT INTO app_reservation_location_voiture (id, date_reservation, date_restitution,utilisateur_id,voiture_id, paiement) VALUES (NULL, '{}', '{}', '{}', '{}',0);".format(arrivee,depart,int(id_user),int(id_voiture))
        cursor.execute(requete)
    # Valider les modifications
        conn.commit()
        cursor.execute("SELECT * FROM `app_reservation_location_voiture` ORDER BY id DESC LIMIT 1;")
        res=cursor.fetchall()
        keys = ['id', 'arrivee', 'depart', 'id_user','id_voiture']
        reservations = dict(zip(keys, res[0]))
        cursor.execute(" SELECT * FROM app_reservation_voiture WHERE id = '{}' ".format(reservations['id_voiture']))
        res=cursor.fetchall()
        keys = ['id','marque','modele','localisation','annee', 'type', 'prix', 'nombre_place','photo']
        voiture = dict(zip(keys, res[0]))
        context = {
                'reservations': reservations,
                'voiture':voiture
                }
        cursor.close()
        conn.close()
        if 'info_utilisateur' in request.session:
            info_utilisateur = request.session['info_utilisateur']
            if 'email' in info_utilisateur:
                email_user = info_utilisateur['email']
                subject = 'Confirmation Réservation Voiture'
                html_message = render_to_string('confirmation.html', {'user_email': email_user})
                plain_message = strip_tags(html_message)
                email = EmailMultiAlternatives(subject, plain_message, to=[email_user])
                email.attach_alternative(html_message, "text/html")
                email.send()
        return render(request, 'reservation_voiture.html', context)
    except Exception as e:
        print(str(e))  
        return render(request, 'erreur.html', {})
    


def resultatvol(request):
    departure = request.POST.get('departure', '')
    arrival = request.POST.get('arrival', '')
    departure_time = request.POST.get('departure_time', '')
    arrival_time = request.POST.get('arrival_time', '')
    nombre_place = request.POST.get('nombre_place', '')
    prix = request.POST.get('prix', '')
    compagnie = request.POST.get('compagnie', '')
    image=request.POST.get('image','')
    print(departure,arrival,departure_time)
    try:
        conn = sql.connect(**config)
        cursor = conn.cursor()
        requete = "SELECT * FROM `app_reservation_vol` WHERE aeroport_depart_id = '{}' AND aeroport_arrivee_id = '{}' AND date_depart >= '{}';".format(departure, arrival, departure_time)
        cursor.execute(requete)
        res = cursor.fetchall()

        print(res)
        if res == []:
            return render(request, 'resultatvol.html', {})
        else:
            resultats = []
            keys = ['id', 'date_depart', 'date_arrivee', 'prix','nombre_place','aeroport_depart', 'aeroport_arrivee', 'compagnie','image']
            for row in res:
                result = dict(zip(keys, row))
                resultats.append(result)
            liste_vols = { result['id']:{ 
                    'date_depart': result['date_depart'],
                    'date_arrivee': result['date_arrivee'],
                    'aeroport_depart': result['aeroport_depart'],
                    'aeroport_arrivee': result['aeroport_arrivee'],
                    'nombre_place': result['nombre_place'],
                    'prix': result['prix'],
                    'image': result['image'],

                    'compagnie': result['compagnie']
                } for result in resultats
                }
          
            context = {'liste_vols': liste_vols}
            cursor.close()
            conn.close()

            return render(request, 'resultatvol.html', context)

    except Exception as e:
        print(str(e))  # Afficher l'erreur pour le débogage
       
        return render(request, 'erreur.html', {})
    

def reservation_vol(request):
    if request.method == 'POST':
        # Récupérer les informations de réservation depuis la requête POST
        if 'info_utilisateur' in request.session:
            info_utilisateur = request.session['info_utilisateur']
            if 'id' in info_utilisateur:
                id_user = info_utilisateur['id']  
    id_vol= request.POST.get('id_vol')
    date= datetime.now()
    date_forma=date.strftime("%Y-%m-%d %H:%M:%S")
    if id_user:

        print(id_vol)
        print(id_user)
        try:
            message=''
            conn = sql.connect(**config)
            cursor = conn.cursor()
            requete="INSERT INTO `app_reservation_reservation_vol` (`id`, `utilisateur`, `vol`, `date`) VALUES (NULL, '{}', '{}', '{}')".format(id_user,id_vol,date_forma);
            
            cursor.execute(requete)
            # Valider les modifications
            conn.commit()
           
            cursor.close()
            conn.close()
            
            return redirect('paiement')
        except Exception as e:
            print(str(e))  # Afficher l'erreur pour le débogage
            message='Erreur route'
            return render(request, 'flight/paiement.html', {'erreur_message': message})
        
        
    else:
        return redirect('flight/paiement.html')
    




