



const loginButton = document.querySelector('#login');
if (loginButton) {
    loginButton.onclick = () => {
        document.querySelector('.login-form-container').classList.toggle('active');
    }
}



document.querySelector('#close-login-form').onclick = () => {
    document.querySelector('.login-form-container').classList.remove('active');
}

window.onscroll = () => {

    if (window.scrollY > 0) {
        document.querySelector('.header').classList.add('active');
    } else {
        document.querySelector('.header').classList.remove('active');
    }


}

window.onload = () => {

    if (window.scrollY > 0) {
        document.querySelector('.header').classList.add('active');
    } else {
        document.querySelector('.header').classList.remove('active');
    }

}

var buttons1 = document.querySelectorAll(".zone_produits button[data-product-id]");
buttons1.forEach(function(button1) {
  button1.addEventListener("click", function() {
    var productId = this.dataset.productId;
    console.log("ID du produit: " + productId);
    // Traitez l'ID du produit ici
  });
});


// Ajout d'un gestionnaire d'événement sur les boutons "commander"
const buttons = document.querySelectorAll('.commander');
buttons.forEach((button) => {
  button.addEventListener('click', () => {
    const id_product = button.getAttribute('data-product-id');
    const quantity = 1; 
    const id_customer = "{{ current_user.idcustomer }}"; 
    
    fetch('/commander', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        id_product: id_product,
        quantity: quantity,
        id_customer: id_customer
      })
    })
    .then((response) => {
      if (!response.ok) {
        throw new Error('Une erreur est survenue lors de la commande.');
      }
      // Si la commande a été effectuée avec succès, on recharge la page pour afficher un message de confirmation
     // window.location.reload();
    })
    .catch((error) => {
      console.error(error);
      alert(error.message);
    });
  });
});