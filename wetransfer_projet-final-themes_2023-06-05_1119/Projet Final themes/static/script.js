function CREER() {
    let cont = document.getElementById("contenu");
    cont.innerHTML = "<form class='connec' action = 'accueil' method = 'post'>\
               <input class='user' name = 'username' placeholder='UserName' type = 'text' maxlength = '12' required /> <br><br>\
                <div class='champmdp'><input class='pass' name = 'password' id='bonjour' placeholder='PassWord' type = 'password' minlength = '6' maxlength = '18' required /> <input type='checkbox' class='oeils' onclick='myFunction()'> </div> <br><br>\
                 <div class='champmdp'><input class='pass' name = 'confirm' id='aurevoir' placeholder='Confirm PassWord' type = 'password' required /><input type='checkbox' class='oeils' onclick='myFunctiondeux()'> </div> <br><br>\
                        <button class='inin' type = 'submit' name = 'valeur' value = 'CREER'>CREER</button>\
        </form>";
}

function CONNECTER() {
    let cont = document.getElementById("contenu");
    cont.innerHTML = "<form class='connec' action = 'accueil' method = 'post'>\
                <input class='user' name = 'username' placeholder='UserName' type = 'text' maxlength = '12' required /> <br><br>\
                <div class='champmdp'> <input class='pass' id='bonjour' name = 'password' placeholder='PassWord' type = 'password' minlength = '6' maxlength = '18' required />  <input class='oeils' type='checkbox' onclick='myFunction()'> </div> <br><br>\
                <button class='inin' type = 'submit' name = 'valeur' value = 'CONNECTER'>CONNECTER</button>\
        </form> <br><br>\
        <script> \
            const faitchier = document.querySelector('#contenu');\
            const togglePassword = document.querySelector('#togglePassword');\
            const password = document.querySelector('#bonjour');\
            togglePassword.addEventListener('click', function (e) {\
                // toggle the type attribute\
                const type = password.getAttribute('type') === 'password' ? 'text' : 'password';\
                password.setAttribute('type', type);\
                // toggle the eye slash icon<br><br>\
                this.classList.toggle('fa-eye-slash');\
            });\
        </script> ";

}

function valcreer() {
    var form_checkbox = document.getElementById('form_case');
    var checkbox = form_checkbox.getElementsByTagName('input');
    var liste_checkbox = ""
    for (let i=0;i<checkbox.length;i++){
        if (checkbox[i].checked == true){
            var liste_checkbox = liste_checkbox+checkbox[i].id+"@"

        }
    }
    liste_checkbox = liste_checkbox.slice(0, liste_checkbox.length - 1);
    window.location="/creergrp?newgrp="+liste_checkbox;
    console.log(liste_checkbox)

}




const onClick = (event) => {
console.log(event.target.id);
window.location="/convac?param="+event.target.id;
}

let test =  new XMLHttpRequest();
test.open("POST" ,"/pizza");
test.responseType = "json"
test.send()

test.onreadystatechange = function(){
    if (this.readyState == 4 && this.status == 200) {
        console.log("SUPERbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")
    }
    }
function myFunction() {
    var x = document.getElementById('bonjour')
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
 }
function  myFunctiondeux() {
    var y = document.getElementById("aurevoir")
    if (y.type === "password") {
    y.type = "text";
  } else {
    y.type = "password";
  }

}