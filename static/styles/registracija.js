var ime = document.forms["vform"]["ime"]; 
var prezime = document.forms["vform"]["prezime"]
var email = document.forms["vform"]["email"]; 
var lozinka = document.forms["vform"]["lozinka"]; 
	
var ime_error = document.getElementById("ime_error"); 
var prezime_error= document.getElementById("prezime_error"); 
var email_error = document.getElementById("email_error"); 
var lozinka_error = document.getElementById("lozinka_error"); 
	
ime.addEventListener("blur", imeVerify, true); 
prezime.addEventListener("blur", prezimeVerify, true); 
email.addEventListener("blur", emailVerify, true); 
lozinka.addEventListener("blur", lozinkaVerify, true); 

function Validacija(){
	
	if(ime.value == ""){
		ime.style.border = "1px solid red"; 
		ime_error.textContent = "Ime je potrebno unijeti!"; 
		ime.focus(); 
		return false; 
	}

	if(prezime.value == ""){
		prezime.style.border = "1px solid red"; 
		prezime_error.textContent = "Prezime je potrebno unijeti!"; 
		prezime.focus(); 
		return false; 
	}

	if(email.value == ""){
		email.style.border = "1px solid red"; 
		email_error.textContent = "E-mail je potrebno unijeti!"; 
		email.focus(); 
		return false; 
	}

	if(lozinka.value == ""){
		lozinka.style.border = "1px solid red"; 
		lozinka_error.textContent = "Lozinku je potrebno unijeti!"; 
		lozinka.focus(); 
		return false; 
	}
}