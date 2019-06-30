function promijeni(){
	
	var destinacija1= document.getElementById("destinacija1");
	var destinacija= document.getElementById("destinacija");
	destinacija.value=destinacija1.value;
	
	var adresa1= document.getElementById("adresa1");
	var adresa= document.getElementById("adresa");
	adresa.value=adresa1.value; 
	
	var broj1= document.getElementById("broj1");
	var broj= document.getElementById("broj");
	broj.value=broj1.value; 
	
	var email1= document.getElementById("email1");
	var email= document.getElementById("email");
	email.value=email1.value; 
	
	var opis1= document.getElementById("opis1");
	var opis= document.getElementById("opis");
	opis.value=opis1.value; 
	
	var poster1= document.getElementById("poster1");
	var poster= document.getElementById("poster");
	poster.value=poster1.value; 
	
	var id1= document.getElementById("id1");
	var id= document.getElementById("id");
	id.value=id1.value; 
}

function izbrisi(){
		alert("Uspješno ste izbrisali ponudu!"); 
		return true; 
}

function dodaj(){
		alert("Uspješno ste dodali ponudu na listu!");
		return true;
}