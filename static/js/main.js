// var container = document.getElementById('container')
// var slider = document.getElementById('slider');
// var slides = document.getElementsByClassName('slide').length;
// var buttons = document.getElementsByClassName('btn');


// var currentPosition = 0;
// var currentMargin = 0;
// var slidesPerPage = 0;
// var slidesCount = slides - slidesPerPage;
// var containerWidth = container.offsetWidth;
// var prevKeyActive = false;
// var nextKeyActive = true;

// window.addEventListener("resize", checkWidth);

// function checkWidth() {
//     containerWidth = container.offsetWidth;
//     setParams(containerWidth);
// }

// function setParams(w) {
//     if (w < 551) {
//         slidesPerPage = 1;
//     } else {
//         if (w < 901) {
//             slidesPerPage = 2;
//         } else {
//             if (w < 1101) {
//                 slidesPerPage = 3;
//             } else {
//                 slidesPerPage = 4;
//             }
//         }
//     }
//     slidesCount = slides - slidesPerPage;
//     if (currentPosition > slidesCount) {
//         currentPosition -= slidesPerPage;
//     };
//     currentMargin = - currentPosition * (100 / slidesPerPage);
//     slider.style.marginLeft = currentMargin + '%';
//     if (currentPosition > 0) {
//         buttons[0].classList.remove('inactive');
//     }
//     if (currentPosition < slidesCount) {
//         buttons[1].classList.remove('inactive');
//     }
//     if (currentPosition >= slidesCount) {
//         buttons[1].classList.add('inactive');
//     }
// }

// setParams();

// function slideRight() {
//     if (currentPosition != 0) {
//         slider.style.marginLeft = currentMargin + (100 / slidesPerPage) + '%';
//         currentMargin += (100 / slidesPerPage);
//         currentPosition--;
//     };
//     if (currentPosition === 0) {
//         buttons[0].classList.add('inactive');
//     }
//     if (currentPosition < slidesCount) {
//         buttons[1].classList.remove('inactive');
//     }
// };

// function slideLeft() {
//     if (currentPosition != slidesCount) {
//         slider.style.marginLeft = currentMargin - (100 / slidesPerPage) + '%';
//         currentMargin -= (100 / slidesPerPage);
//         currentPosition++;
//     };
//     if (currentPosition == slidesCount) {
//         buttons[1].classList.add('inactive');
//     }
//     if (currentPosition > 0) {
//         buttons[0].classList.remove('inactive');
//     }
// // };

var chambre_selectionner;
var mes_boutons = document.querySelectorAll('.btn_res')
mes_boutons.forEach(function(button) {
    button.addEventListener('click', function() {
      // Récupérer les informations spécifiques à ce bouton à partir de l'attribut 'data-info'
      chambre_selectionner = this.getAttribute('data-info');
      // Utiliser les informations spécifiques selon vos besoins
     
    });
  });

var confirmation = document.querySelector('.confirmer')
confirmation?.addEventListener('click',()=>{
    var chambre = document.getElementById('id_chambre')
    chambre.value =chambre_selectionner
})

const validation = (values) => {
  const errors = {};
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/i;
  const regex2 = /^7[7,8,6,0,5]\d{7}$/;
  if (!values.nom) {
    errors.nom = "Veuillez saisir votre nom!";
  }
  else if(values.nom.length<2){
    errors.nom = "Le nom doit avoir minimum 2 caractéres";
  }
  if (!values.prenom) {
    errors.prenom = "Veuillez saisir votre prenom!";
  }
  else if(values.prenom.length<3){
    errors.prenom = "Le prenom doit avoir minimum 2 caractéres";
  }

  if (!values.email) {
    errors.email = "Veuillez saisir votre adresse mail!";
  } else if (!regex.test(values.email)) {
    errors.email = "Format du mail invalide !";
  }
  if (!values.adresse) {
    errors.adresse = "Veuillez saisir votre adresse!";
  }
  else if(values.adresse.length<2){
    errors.adresse = "L'adresse doit avoir minimum 2 caractéres";
  }
  if (!values.telephone) {
    errors.telephone = "Veuillez saisir votre numero";
  }else if (!regex2.test(values.telephone.split(" ").join(""))) {
    errors.telephone = "Format du numero de telephone invalide!"}

  if (!values.mot_de_passe) {
    errors.mot_de_passe = "Veuillez saisir le mot de passe";
  } else if (values.mot_de_passe.length < 4) {
    errors.mot_de_passe = "Le mot de passe doit être supérieure à 4 caractères";
  } else if (values.mot_de_passe.length > 20) {
    errors.mot_de_passe = "Le mot de passe doit être inférieur à 20 caractères";
  }
  if (!values.mot_de_passe2) {
    errors.mot_de_passe2 = "Veuillez confirmer le mot de passe";
  } else if (values.mot_de_passe2 !== values.mot_de_passe) {
    errors.mot_de_passe2 = "Mots de passe incompatibles !";
  }
  return errors;
}; 


// Formulaire d'inscription validation
var form_inscription = document.getElementById('form_inscription');
form_inscription?.addEventListener('submit', function(event) {
  event.preventDefault(); // Empêcher le comportement par défaut du formulaire (rechargement de la page)
  valeurs={
    "nom": document.getElementById('nom').value,
    "prenom": document.getElementById('prenom').value,
    "email" : document.getElementById('email').value,
    "telephone" : document.getElementById('telephone').value,
    "adresse": document.getElementById('adresse').value,
    "mot_de_passe" : document.getElementById('mot_de_passe').value,
    "mot_de_passe2" : document.getElementById('mot_de_passe2').value,
  }
  var liste_erreur=validation(valeurs);
  console.log(liste_erreur)
  if( Object.keys(liste_erreur).length === 0){
    form_inscription.submit();
  }
  else {
    
    if(liste_erreur?.nom){
      document.getElementById('erreurnom').innerHTML=liste_erreur?.nom
    }
    else{
      document.getElementById('erreurnom').innerHTML=''
    }
    if(liste_erreur.prenom){
      document.getElementById('erreurprenom').innerHTML=liste_erreur.prenom
    }
    else{
      document.getElementById('erreurprenom').innerHTML=''
    }
   
   if(liste_erreur?.email){
    document.getElementById('erreuremail').innerHTML=liste_erreur?.email
   }
   else{
    document.getElementById('erreuremail').innerHTML=''
   }
    if(liste_erreur?.telephone){
      document.getElementById('erreurtelephone').innerHTML=liste_erreur?.telephone
    }else{
      document.getElementById('erreurtelephone').innerHTML=''
    }
     
     if(liste_erreur?.adresse){
      document.getElementById('erreuradresse').innerHTML=liste_erreur?.adresse
     }else{
      document.getElementById('erreuradresse').innerHTML=''
     }
     
     if(liste_erreur?.mot_de_passe){
      document.getElementById('erreurmotdepasse').innerHTML=liste_erreur?.mot_de_passe
     }else{
      document.getElementById('erreurmotdepasse').innerHTML=''
     }
   
    if(liste_erreur?.mot_de_passe2){
      document.getElementById('erreurmotdepasse2').innerHTML=liste_erreur?.mot_de_passe2
    }
    else{
      document.getElementById('erreurmotdepasse2').innerHTML=''
    }

  }

});

const validationDate = (values) => {
  const erreurs = {}
  var arrivee = new Date(values?.arrivee);
  var depart = new Date(values.depart);
  var dateActuelle = new Date();
   if (arrivee<dateActuelle) {
    erreurs.arrivee = "La date de reservation doit être ultérieur à la date d'aujourd'hui !";
  }
  if (depart<dateActuelle) {
    erreurs.depart= "La date de restitution doit être ultérieur à la date d'aujourd'hui !";
  }
  if (arrivee>depart) {
    erreurs.dates = "La date de départ ne doit pas preceder la date d'arrivee";
  }
  return erreurs;

}
//Controle recherche hotel
var form_hotel = document.getElementById('form_hotel');
form_hotel?.addEventListener('submit', function(event) {
  event.preventDefault(); 
  dates={
    "depart": document.getElementById('depart').value,
    "arrivee": document.getElementById('arrivee').value,
  }
  var liste_erreur=validationDate(dates);
  console.log(liste_erreur)
  if( Object.keys(liste_erreur).length === 0){
    document.getElementById('erreurHotel').innerHTML=''
    form_hotel.submit();
  }
  else{
    document.getElementById('erreurHotel').innerHTML=''
    Object.entries(liste_erreur).forEach(function([cle, valeur]) {
      document.getElementById('erreurHotel').innerHTML+="** "+valeur+"<br>"
    });
   
    
  }
});

var info_reservation=document.getElementById('info_reservation')
var date_arrivee=document.getElementById('date_arrivee');
var date_depart=document.getElementById('date_depart');
function FormaterDate(date) {
  var datesplit = date.split(',');
  var format= datesplit[0]+" "+datesplit[1]
  var dateObj = new Date(format);
  return dateObj;
}
function nombreJoursEntreDates(date1, date2) {
  var unJour = 24 * 60 * 60 * 1000; // Nombre de millisecondes dans une journée
  var date1Arrondie = new Date(date1.getFullYear(), date1.getMonth(), date1.getDate());
  var date2Arrondie = new Date(date2.getFullYear(), date2.getMonth(), date2.getDate());

  var differenceJours = Math.round(Math.abs((date1Arrondie - date2Arrondie) / unJour));

  return differenceJours;
}
if(date_arrivee?.value){
  var montantTotal=document.getElementById('montantTotal');
  var Total=document.getElementById('Total');
  console.log(date_arrivee.value.split(','))
  var diff =nombreJoursEntreDates(FormaterDate(date_arrivee.value),FormaterDate(date_depart.value))
  console.log(montantTotal)
  Total.textContent= parseInt(montantTotal.value)*diff
}



// Récupérer l'élément <form> par son id
var form = document.getElementById('myForm');

// Écouter l'événement "submit" du formulaire
form?.addEventListener('submit', function(event) {
  event.preventDefault(); // Empêcher le comportement par défaut du formulaire (rechargement de la page)

  // Envoyer la requête de soumission du formulaire
  var formData = new FormData(form); // Créer un objet FormData pour collecter les données du formulaire
  var url = form.action; // Récupérer l'URL de traitement du formulaire
  var method = form.method; // Récupérer la méthode d'envoi du formulaire (POST dans cet exemple)

  // Effectuer la requête AJAX pour envoyer les données du formulaire
  form.submit();
});

var boutons = document.querySelectorAll('.accordion-button')
boutons.forEach(function(button) {
  button.addEventListener('click', function() {
    button.firstElementChild.checked=true
    
    // Utiliser les informations spécifiques selon vos besoins
   
  });
});

var supprimer = document.querySelectorAll('.supprimer')
supprimer.forEach(function(button) {
    button.addEventListener('click', function() {
      document.getElementById('id_reservation').value=button.value
      document.getElementById('id_reservation2').value=button.value
      document.getElementById('id_reservation3').value=button.value
      console.log(document.getElementById('id_reservation2'))
     
    });
  });