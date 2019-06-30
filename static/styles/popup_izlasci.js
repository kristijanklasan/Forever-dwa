function klikni(element){
	document.getElementById('trazilica').value = element.getAttribute('naziv-slike');
	trazi.click();
} 

function otvori() {
	document.getElementById("forma").style.display = "block";
}

function zatvori() {
	document.getElementById("forma").style.display = "none";
}

