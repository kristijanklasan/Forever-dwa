function promijeni_film(){
	
	var naziv1 = document.getElementById("naziv1");
	var naziv = document.getElementById("naziv");
	naziv.value=naziv1.value; 
	
	var godina1 = document.getElementById("godina1");
	var godina = document.getElementById("godina");
	godina.value=godina1.value; 
	
	var redatelj1 = document.getElementById("redatelj1");
	var redatelj = document.getElementById("redatelj");
	redatelj.value=redatelj1.value; 
	
	var opis1= document.getElementById("opis1");
	var opis= document.getElementById("opis");
	opis.value=opis1.value; 
	
	var trailer1 = document.getElementById("trailer1");
	var trailer = document.getElementById("trailer");
	trailer.value=trailer1.value; 
	
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