function promijeni_drustvene(){
	
	var naziv1= document.getElementById("naziv1");
	var naziv= document.getElementById("naziv");
	naziv.value=naziv1.value;
	
	var broj1= document.getElementById("broj1");
	var broj= document.getElementById("broj");
	broj.value=broj1.value; 
	
	var opis1= document.getElementById("opis1");
	var opis= document.getElementById("opis");
	opis.value=opis1.value; 
	
	var link1= document.getElementById("link1");
	var link= document.getElementById("link");
	link.value=link1.value; 
	
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