from django.db import models
from django.db.models import ForeignKey
import random
from faker import Faker
from amadeus import Client, ResponseError
from django.utils import timezone

default_value = timezone.now()


amadeus = Client(
    client_id='RKx4s0hwYBfPWsEUx3JP3AAFxIuK4WRA',
    client_secret='pxrndHEwRQXNdTA9'
)
fake = Faker() 

# Create your models here.
class Utilisateur(models.Model):
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    adresse = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    mot_de_passe = models.CharField(max_length=50)
    telephone = models.CharField(max_length=20)


def generer_numero():
    prefixe = random.choice(['70', '76', '77', '78'])
    numeros = ''.join(random.choice('0123456789') for _ in range(7))
    numero_telephone =prefixe + numeros
    return numero_telephone

# for i in range(20):
#     try :
#         utilisateur = Utilisateur()
#         utilisateur.nom = fake.name().split(' ')[1]
#         utilisateur.prenom = fake.name().split(' ')[0]
#         utilisateur.adresse = " ".join(fake.address().split(' ')[0:3])
#         utilisateur.email = fake.email()
#         utilisateur.telephone = generer_numero()
#         utilisateur.mot_de_passe='passer'
#         utilisateur.save()
#     except Exception as e:
#         print(str(e))


class Compagnie(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    nom = models.CharField(max_length=255)

#INSERTION DES DONNÉES DANS LA TABLE COMPAGNIE
# try:
#     #requete pour avoir les compagnies
#     response =amadeus.reference_data.airlines.get()
#     print(response.data)
#     for item in response.data:
#         iata_code = item['iataCode']
#         business_name = item['businessName']
        
#         compagnie = Compagnie(code=iata_code, nom=business_name)
#         compagnie.save()
# except ResponseError as error:
#     print(error)

class Aeroport(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    nom = models.CharField(max_length=255)
    ville = models.CharField(max_length=255)
    code_ville = models.CharField(max_length=255)
    pays = models.CharField(max_length=255)
    code_pays = models.CharField(max_length=255)

#INSERTION DES DONNÉES DANS LA TABLE AEROPORTS
# for i in ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']:
#     try:
#         #requete pour avoir les aeroports dont le code commence par i
#         response =amadeus.reference_data.locations.get(
#         keyword=i,
#         subType='AIRPORT' )
#         for item in response.data:
#             iataCode=item['iataCode']
#             name=item['name']
#             city=item['address']['cityName']
#             code_city=item['address']['cityCode']
#             country=item['address']['countryName']
#             code_country=item['address']['countryCode']
#             aeroport = Aeroport(code=iataCode,nom=name,ville=city,code_ville=code_city,pays=country,code_pays=code_country)
#             aeroport.save()

#     except ResponseError as error:
#         print(error)

class Vol(models.Model):
    compagnie = models.ForeignKey(Compagnie, to_field='code', on_delete=models.CASCADE, related_name='compagnie')
    aeroport_depart = models.ForeignKey(Aeroport, to_field='code', on_delete=models.CASCADE, related_name='vols_depart')
    aeroport_arrivee = models.ForeignKey(Aeroport, to_field='code', on_delete=models.CASCADE, related_name='vols_arrivee')
    date_depart = models.DateTimeField()
    date_arrivee = models.DateTimeField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    nombre_place = models.IntegerField()
    image=models.CharField(max_length=255,null=True)
    

#INSERTION DES DONNÉES DANS LA TABLE VOLS
# try:
#     response =amadeus.shopping.flight_offers_search.get(
#         originLocationCode='MAD',
#         destinationLocationCode='ADQ',
#         departureDate='2023-06-01',
#         adults=1,
#         max=20)
#     for item in response.data:
#         v_compagnie=Compagnie.objects.get(code=item['itineraries'][0]['segments'][0]['carrierCode'])
#         v_aeroport_depart=Aeroport.objects.get(code=item['itineraries'][0]['segments'][0]['departure']['iataCode'])
#         v_aeroport_arrivee=Aeroport.objects.get(code=item['itineraries'][0]['segments'][0]['arrival']['iataCode'])
#         v_date_depart=item['itineraries'][0]['segments'][0]['departure']['at']
#         v_date_arrivee=item['itineraries'][0]['segments'][0]['departure']['at']
#         v_prix=item['price']['total']
#         v_nombre_place=item['numberOfBookableSeats']
#         vol = Vol(date_depart=v_date_depart,date_arrivee=v_date_arrivee,prix=v_prix,nombre_place=v_nombre_place)
#         vol.compagnie=v_compagnie
#         vol.aeroport_depart=v_aeroport_depart
#         vol.aeroport_arrivee=v_aeroport_arrivee
#         vol.save()
# except ResponseError as error:
#     print(error)

class Hotel(models.Model):
    id_hotel = models.CharField(max_length=10, primary_key=True)
    nom = models.CharField(max_length=255)
    code_pays = models.CharField(max_length=255)
    ville=models.CharField(max_length=255)
    photo= models.CharField(max_length=255)

#INSERTION DES DONNÉES DANS LA TABLE HOTEL
# for i in ['DKR','CSK','XLS','ZIG']: #Code ville de Dakar, Cap Skiring, Saint-Louis, Ziguinchor
#     try:
#         response = amadeus.reference_data.locations.hotels.by_city.get(cityCode=i)
#         print(response.data)
#         for item in response.data:
#             h_id_hotel=item['hotelId']
#             h_nom=item['name']
#             h_code_pays=item['address']['countryCode']
#             hotel=Hotel(id_hotel=h_id_hotel,nom=h_nom,code_pays=h_code_pays)
#             hotel.save()
#     except ResponseError as error:
#         print(error)


class Chambre(models.Model):
    hotel = models.ForeignKey(Hotel, to_field='id_hotel', on_delete=models.CASCADE, related_name='hotel')
    type_chambre= models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    prix = models.IntegerField()
    nombre_place = models.IntegerField()
    photo= models.CharField(max_length=255)

def choix_aleatoire(liste_mots):
    choix = random.choice(liste_mots)
    return choix

#INSERTION DES DONNÉES DANS LA TABLE CHAMBRE
# list_hotel= ['FGDKRLDN','FGDKRLDN','IQDKRTER','RDDKR117','TYDKRRAC','TYDKRRHI','WKDKR563']
# list_type  = ['Chambre Simple', 'Chambre de Luxe', 'Suite Junior', 'Suite', 'Chambre Premium']
# list_description =['Vue sur l’océan','Vue sur la ville','Vue sur le jardin','Vue sur la mer']
# list_prix=[50000,90000,120000,990000,150000]
# list_nombre_place = [2,4,5,1]
# list_photo = ["c1.jpg","c2.jpg","c3.jpeg","c4.jpeg"]  
# for i in range(20):
#     hotel = Hotel.objects.get(id_hotel=choix_aleatoire(list_hotel))
#     chambre = Chambre(
#         hotel=hotel,
#         type_chambre=choix_aleatoire(list_type),
#         description=choix_aleatoire(list_description),
#         prix=choix_aleatoire(list_prix),
#         nombre_place=choix_aleatoire(list_nombre_place),
#         photo=choix_aleatoire(list_photo)
#     )
#     chambre.save()

class Voiture(models.Model):
    marque= models.CharField(max_length=255)
    modele= models.CharField(max_length=255)
    localisation = models.CharField(max_length=255)
    annee= models.IntegerField()
    type=models.CharField(max_length=255)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    nombre_place =  models.IntegerField()
    photo= models.CharField(max_length=255)
    disponible=models.BooleanField(default=True)

#INSERTION DES DONNÉES DANS LA TABLE VOITURE
# voitures = {
#     'Toyota': ['Camry', 'Corolla', 'RAV4', 'Prius'],
#     'Honda': ['Civic', 'Accord', 'CR-V', 'Pilot'],
#     'Ford': ['Mustang', 'F-150', 'Explorer', 'Focus'],
#     'Chevrolet': ['Cruze', 'Malibu', 'Equinox', 'Silverado'],
#     'BMW': ['3 Series', '5 Series', 'X3', 'X5'],
#     'Mercedes-Benz': ['C-Class', 'E-Class', 'GLC', 'GLE'],
#     'Volkswagen': ['Golf', 'Passat', 'Tiguan', 'Atlas'],
#     'Audi': ['A4', 'A6', 'Q5', 'Q7'],
#     'Hyundai': ['Elantra', 'Sonata', 'Tucson', 'Santa Fe'],
#     'Kia': ['Forte', 'Optima', 'Sportage', 'Sorento']
# }

# for i in range(20):
#     v_marque = random.choice(list(voitures.keys()))
#     v_modele = random.choice(voitures[v_marque])
#     v_localisation= random.choice(['Dakar', 'Thiès', 'Mbour', 'Saint-Louis'])
#     v_annee = random.randint(2007, 2022)
#     v_type = random.choice(['Manuelle','Automatique'])
#     v_prix = random.choice([25000,30000,50000,80000,100000])
#     v_nombre_place = random.randint(4, 7)
#     v_photo= "v1.jpg"
#     voiture=Voiture(marque=v_marque,modele=v_modele,localisation=v_localisation,annee=v_annee,type=v_type,prix=v_prix,nombre_place=v_nombre_place,photo=v_photo)
#     voiture.save()

class Reservation_Vol(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, to_field='id', on_delete=models.CASCADE, related_name='utilisateur')
    vol = models.ForeignKey(Vol, to_field='id', on_delete=models.CASCADE, related_name='vol')
    date = models.DateTimeField()

# utilisateur = Utilisateur.objects.get(id=1)
# vol = Vol.objects.get(id=1)
# reservation_vol = Reservation_Vol.objects.create(utilisateur=utilisateur, vol=vol, date=timezone.now())

class Reservations_Hotel(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, to_field='id', on_delete=models.CASCADE, related_name='utilisateur2')
    chambre = models.ForeignKey(Chambre, to_field='id', on_delete=models.CASCADE, related_name='chambre')
    date_reservation = models.DateTimeField()
    date_restitution = models.DateTimeField()
    paiement=models.BooleanField(default=False)


# utilisateur = Utilisateur.objects.get(id=1)
# chambre = Chambre.objects.get(id=1)
# reservations_hotel = Reservations_Hotel.objects.create(utilisateur=utilisateur, chambre=chambre, date_reservation =timezone.now(), date_restitution =timezone.now())

class Location_Voiture(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, to_field='id', on_delete=models.CASCADE, related_name='utilisateur3')
    voiture = models.ForeignKey(Voiture, to_field='id', on_delete=models.CASCADE, related_name='voiture')
    date_reservation = models.DateTimeField()
    date_restitution = models.DateTimeField()
    

# utilisateur = Utilisateur.objects.get(id=1)
# voiture = Voiture.objects.get(id=1)
# location_Voiture = Location_Voiture.objects.create(utilisateur=utilisateur, voiture=voiture, date_reservation =timezone.now(), date_restitution =timezone.now())