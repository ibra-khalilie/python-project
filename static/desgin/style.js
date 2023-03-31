



const loginButton = document.querySelector('#login');
if (loginButton) {
    loginButton.onclick = () => {
        document.querySelector('.login-form-container').classList.toggle('active');
    }
}



const closeLoginFormButton = document.querySelector('#close-login-form');
if (closeLoginFormButton) {
    closeLoginFormButton.onclick = () => {
        document.querySelector('.login-form-container').classList.remove('active');
    }
}

window.onscroll = () => {

    if (window.scrollY > 0) {
        document.querySelector('.header').classList.add('active');
    } else {
        const header = document.querySelector('.header')
        if (header) {
            header.classList.remove('active');
        }

    }


}

window.onload = () => {

    if (window.scrollY > 0) {
        document.querySelector('.header').classList.add('active');
    } else {
        const header = document.querySelector('.header')
        if (header) {
            header.classList.remove('active');
        }
    }

}

var buttons1 = document.querySelectorAll(".zone_produits button[data-product-id]");
buttons1.forEach(function (button1) {
    button1.addEventListener("click", function () {
        var productId = this.dataset.productId;
        console.log("ID du produit: " + productId);

    });
});



const buttons = document.querySelectorAll('.payer');
buttons.forEach((button) => {
    button.addEventListener('click', () => {

        const quantity = 1;

        fetch('/payer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                quantity: quantity,
            })
        })
            .then((response) => {
                alert("L'opération a été bien reussie");
                window.location.replace('/')

                if (!response.ok) {
                    throw new Error('Une erreur est survenue lors de la commande.');
                }
            })
            .catch((error) => {
                console.error(error);
                alert(error.message);
            });
    });
});


const panierItems = document.querySelector('#cart-items');
const commanderBtns = document.querySelectorAll('.commander');
const payerBtn = document.querySelector('#payerBtn');


commanderBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
        const productId = e.target.getAttribute('data-product-id');
        const productPrice = e.target.getAttribute('data-product-price');
        const productLibelle = e.target.getAttribute('data-product-libelle');
        const productImg = e.target.getAttribute('data-product-img');

        const product = {
            id: productId,
            name: productLibelle,
            image: productImg,
            price: productPrice,
            quantity: 1
        };
        addItemToCart(product);
    });
});

function addItemToCart(product) {
    const item = document.createElement('li');
    item.className = 'cart-item';
    item.setAttribute('data-product-id', product.id);
    item.innerHTML = `
                <img src="${product.image}" alt="${product.name}">
                <div class="cart-item-info">
                    <p>${product.name}</p>
                    <p>Prix: ${product.price}€</p>
                    <p>Quantité: ${product.quantity}</p>
                </div>
            `;
    panierItems?.appendChild(item);

    item.addEventListener('click', (e) => {

        alert(`Nom: ${product.name}, Prix: ${product.price}€`);
    });
}




payerBtn?.addEventListener('click', async () => {
    const cartItems = document.querySelectorAll('.cart-item');
    const cartData = [];

    cartItems.forEach(item => {
        const productId = item.getAttribute('data-product-id');
        const name = item.querySelector('.cart-item-info p:nth-child(1)').textContent;
        const price = parseFloat(item.querySelector('.cart-item-info p:nth-child(2)').textContent.replace('Prix: ', '').replace('€', ''));
        const quantity = parseInt(item.querySelector('.cart-item-info p:nth-child(3)').textContent.replace('Quantité: ', ''));

        cartData.push({ productId, name, price, quantity });
    });

    const response = await fetch('/process_cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(cartData)
    });

    if (response.ok) {
        const data = await response.json();
        window.location.href = data.url;
    } else {

    }
});


const cancel = document.querySelectorAll('.cancelBtn');
console.log(cancel)

cancel.forEach(btn => {
    btn.addEventListener('click', (e) => {
        if (!confirm("Voulez-vous vraiment annuler la commande ?")) {
            return
        }
        const id_product = e.target.getAttribute('data-id');

        fetch("/cancel-command", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                id_product: id_product
            })
        })
            .then(function (response) {
                if (response.ok) {
                    location.reload();
                } else {
                    throw new Error("Une erreur est survenue");
                }
            })
            .catch(function (error) {
                console.error(error);
            });
    });
});




