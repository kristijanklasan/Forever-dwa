#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: kristijan
"""

from flask import Flask, Response, jsonify, request, flash, render_template, current_app, redirect
from model import Filmovi, Drustvene_igre,Moja_lista, Izlazak
import sqlite3 
import os 
import secrets
from passlib.hash import sha256_crypt
from werkzeug.utils import secure_filename

db = sqlite3.connect("baza.db",check_same_thread=False)
app = Flask(__name__) 

cur = db.cursor()
global dataa

@app.route("/")
def home():
    return render_template('pocetna.html')

@app.route('/registracija',methods=["GET","POST"])
def registracija(): 
    if request.method == "POST":
        ime = request.form.get("ime")
        prezime = request.form.get("prezime")
        email = request.form.get("email")
        lozinka = request.form.get("lozinka")
        sig_lozinka = sha256_crypt.encrypt(str(lozinka))
		
        if ime != "" and prezime != "" and email != "" and lozinka != "":
            flash("Uspješno ste se registrirali!")
        
            db.execute("INSERT INTO Korisnik(ime, prezime, email, lozinka) VALUES (:ime, :prezime, :email, :lozinka)", {"ime":ime,"prezime":prezime,"email":email,"lozinka":sig_lozinka})
            db.commit()
            return render_template('restorani.html')
    return render_template('Registracija.html')

@app.route('/prijava', methods=["GET","POST"])
def prijava(): 
	if request.method == "POST":
		email = request.form.get("email")
		lozinka = request.form.get("lozinka")
		
		e_mail = db.execute("SELECT email FROM Korisnik WHERE email=:email",{"email":email}).fetchone()
		passw = db.execute("SELECT lozinka FROM Korisnik WHERE email=:email",{"email":email}).fetchone()
		
		cur.execute("SELECT ime,prezime FROM Korisnik WHERE email=:email",{"email":email})
		dataa= cur.fetchall()
		
		if e_mail is None:
			return render_template("Prijava.html")
		else: 
			for data in passw: 
				if sha256_crypt.verify(lozinka,data):
					return render_template("restorani.html",data=dataa)
		
	return render_template("Prijava.html")

@app.route('/odjava', methods=["GET"])
def odjava(): 
		return render_template("pocetna.html")
	
def allowed_image(filename): 
	if not "." in filename: 
		return False
	
	ext = filename.rsplit(".",1)[1]
	if ext.upper()in app.config["ALLOWED_IMAGE_EXTENSIONS"]: 
		return True
	else: 
		return False 
		
app.config["IMAGE_UPLOADS"]="static/styles/Slike/"
app.config["ALLOWED_IMAGE_EXTENSIONS"]= ["PNG","JPG","JPEG"]

@app.route("/kafic", methods=["GET","POST"])
def unos_kafica(): 
	if request.method == "POST":
		kategorija = request.form.get("kategorija")
		destinacija = request.form.get("destinacija")
		adresa = request.form.get("adresa")
		broj = request.form.get("broj")
		email = request.form.get("email")
		opis = request.form.get("opis")
		poster = request.form.get("poster")
		
		cur.execute("SELECT * FROM Izlazak")

		data = cur.fetchall()
		
		if request.files:
			slika = request.files["image"]
			
			if slika.filename == "": 
				return redirect(request.url)
			
			if not allowed_image(slika.filename): 
				
				return redirect(request.url)
				
			else: 
				filename = secure_filename(slika.filename)
				slika.save(os.path.join(app.config["IMAGE_UPLOADS"], slika.filename))
			
				if kategorija != "" and destinacija != "" and adresa != "" and broj != "" and email != "" and opis != "":
					db.execute("INSERT INTO Izlazak(kategorija, destinacija, adresa, broj, email, opis, poster, slika) VALUES (:kategorija, :destinacija, :adresa, :broj, :email, :opis, :poster, :slika)", {"kategorija":kategorija,"destinacija":destinacija,"adresa":adresa,"broj":broj,"email":email,"opis":opis,"poster":poster,"slika":slika.filename})
					db.commit()
			return render_template("kafici.html")
			
		destinacija= request.form.get("destinacija1") 
		
		
	return render_template("kafici.html")

@app.route("/prazna", methods=["GET","POST"])
def prazna(): 


	cur.execute("SELECT opis FROM Filmovi")

	data = cur.fetchall()
		
	return render_template("prazna.html",data=dataa)
	
@app.route("/pregled", methods=["GET","POST"])
def pregled(): 
	if request.method == "POST":
		naziv_ponude = request.form.get("destinacija2")
		datum = request.form.get("datum")
		
		if naziv_ponude != "":
		
			db.execute("INSERT INTO Moja_lista(naziv_ponude,datum) VALUES (:naziv_ponude,:datum)", {"naziv_ponude":naziv_ponude,"datum":datum})
			db.commit()
			
			return render_template("moja_lista.html")
		else: 
			return render_template("pregled.html")
	return render_template("pregled.html")

@app.route("/pregled_filma", methods=["GET","POST"])
def pregled_filma(): 
	if request.method == "POST":
		film2 = request.form.get("film2")
		datum = request.form.get("datum") 
		
		if film2 != "":
		
			db.execute("INSERT INTO Moja_lista(naziv_ponude,datum) VALUES (:naziv_ponude,:datum)", {"naziv_ponude":film2,"datum":datum})
			db.commit()
			
			return render_template("moja_lista.html")
		else: 
			return render_template("pregled.html")
	return render_template("pregled.html")
	
@app.route("/nocni_klubovi", methods=["GET","POST"])
def unos_kluba(): 
	if request.method == "POST":
		kategorija = request.form.get("kategorija")
		destinacija = request.form.get("destinacija")
		adresa = request.form.get("adresa")
		broj = request.form.get("broj")
		email = request.form.get("email")
		opis = request.form.get("opis")
		poster = request.form.get("poster")
		
		cur.execute("SELECT * FROM Izlazak")

		data = cur.fetchall()
		
		if request.files:
			image = request.files["image"]
			
			if image.filename == "": 
				return redirect(request.url)
			
			if not allowed_image(image.filename): 
				
				return redirect(request.url)
				
			else: 
				filename = secure_filename(image.filename)
				image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
			
				if kategorija != "" and destinacija != "" and adresa != "" and broj != "" and email != "" and opis != "":
					db.execute("INSERT INTO Izlazak(kategorija, destinacija, adresa, broj, email, opis, poster, slika) VALUES (:kategorija, :destinacija, :adresa, :broj, :email, :opis, :poster, :slika)", {"kategorija":kategorija,"destinacija":destinacija,"adresa":adresa,"broj":broj,"email":email,"opis":opis,"poster":poster,"slika":image.filename})
					db.commit()
			return render_template("nocni_klubovi.html")		
		
	return render_template("nocni_klubovi.html")
	
@app.route("/unos", methods=["GET","POST"])
def unos(): 
	if request.method == "POST":
		
		destinacija1 = request.form.get("destinacija1")
		
		cur.execute("SELECT * FROM Izlazak WHERE destinacija=:destinacija",{"destinacija":destinacija1})
		dataa= cur.fetchall()
	return render_template("pregled.html",data=dataa)	

@app.route("/izbrisi_film", methods=["GET","POST"])
def izbrisi_film(): 
	
	film = request.form.get("drugi")
		
	if film != "": 
		db.execute("DELETE FROM Filmovi WHERE originalni_naziv=:originalni_naziv",{"originalni_naziv":film})
		db.commit()
		cur.execute("DELETE FROM Filmovi WHERE originalni_naziv=:originalni_naziv",{"originalni_naziv":film})
		dataa= cur.fetchall()
		return render_template("akcija.html",data=dataa)
		
	return render_template("pregled.html",data=dataa)

@app.route("/izbrisi_ponudu", methods=["GET","POST"])
def izbrisi_ponudu(): 
	
	ponuda = request.form.get("drugi")
		
	if ponuda != "": 
		db.execute("DELETE FROM Izlazak WHERE destinacija=:destinacija",{"destinacija":ponuda})
		db.commit()
		cur.execute("DELETE FROM Izlazak WHERE destinacija=:destinacija",{"destinacija":ponuda})
		dataa= cur.fetchall()
		return render_template("restorani.html",data=dataa)
		
	return render_template("restorani.html",data=dataa)
	
@app.route("/unos_filma", methods=["GET","POST"])
def unos_filma(): 
	if request.method == "POST":
		
		film = request.form.get("originalni_naziv")
		
		cur.execute("SELECT * FROM Filmovi WHERE originalni_naziv=:originalni_naziv",{"originalni_naziv":film})
		dataa= cur.fetchall()
		
	return render_template("pregled_filmova.html",data=dataa)


@app.route("/restorani", methods=["GET","POST"])
def unos_restorana(): 
	cur.execute("SELECT opis FROM Filmovi")

	data = cur.fetchall()
	if request.method == "POST":
		kategorija = request.form.get("kategorija")
		destinacija = request.form.get("destinacija")
		adresa = request.form.get("adresa")
		broj = request.form.get("broj")
		email = request.form.get("email")
		opis = request.form.get("opis")
		destinacija1 = request.form.get("destinacija1")
		poster = request.form.get("poster")
		
		if request.files:
			image = request.files["image"]
			
			if image.filename == "": 
				return redirect(request.url)
			
			if not allowed_image(image.filename): 
				
				return redirect(request.url)
				
			else: 
				filename = secure_filename(image.filename)
				image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
			
				if kategorija != "" and destinacija != "" and adresa != "" and broj != "" and email != "" and opis != "":
					db.execute("INSERT INTO Izlazak(kategorija, destinacija, adresa, broj, email, opis, poster, slika) VALUES (:kategorija, :destinacija, :adresa, :broj, :email, :opis, :poster, :slika)", {"kategorija":kategorija,"destinacija":destinacija,"adresa":adresa,"broj":broj,"email":email,"opis":opis,"poster":poster,"slika":image.filename})
					db.commit()
			return render_template("restorani.html")
			
	return render_template("restorani.html")
	
@app.route("/slasticarna", methods=["GET","POST"])
def unos_slasticarne(): 
	if request.method == "POST":
		kategorija = request.form.get("kategorija")
		destinacija = request.form.get("destinacija")
		adresa = request.form.get("adresa")
		broj = request.form.get("broj")
		email = request.form.get("email")
		opis = request.form.get("opis")
		poster = request.form.get("poster")
		
		if request.files:
			image = request.files["image"]
			
			if image.filename == "": 
				return redirect(request.url)
			
			if not allowed_image(image.filename): 
				
				return redirect(request.url)
				
			else: 
				filename = secure_filename(image.filename)
				image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
			
				if kategorija != "" and destinacija != "" and adresa != "" and broj != "" and email != "" and opis != "":
					db.execute("INSERT INTO Izlazak(kategorija, destinacija, adresa, broj, email, opis, poster, slika) VALUES (:kategorija, :destinacija, :adresa, :broj, :email, :opis, :poster, :slika)", {"kategorija":kategorija,"destinacija":destinacija,"adresa":adresa,"broj":broj,"email":email,"opis":opis,"poster":poster,"slika":image.filename})
					db.commit()
			return render_template("slasticarna.html")
			
	return render_template("slasticarna.html")

@app.route("/akcija", methods=["GET","POST"])
def unos_akcijskog_filma(): 
	if request.method == "POST":
		kategorija_filma = request.form.get("kategorija")
		originalni_film = request.form.get("originalni_film")
		godina = request.form.get("godina")
		redatelj = request.form.get("redatelj")
		opis_filma = request.form.get("opis_filma")
		trailer = request.form.get("trailer")
		poster = request.form.get("poster")
		
		if request.files:
			image = request.files["image"]
			
			if image.filename == "": 
				return redirect(request.url)
			
			if not allowed_image(image.filename): 
				
				return redirect(request.url)
				
			else: 
				filename = secure_filename(image.filename)
				image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
			
				if kategorija_filma != "" and originalni_film != "" and godina != "" and redatelj != "" and opis_filma != "":
					db.execute("INSERT INTO Filmovi(naziv_kategorije,originalni_naziv,godina_izdavanja,redatelj,opis,trailer,poster,slika) VALUES (:naziv_kategorije,:originalni_naziv,:godina_izdavanja,:redatelj,:opis,:trailer,:poster,:slika)", {"naziv_kategorije":kategorija_filma,"originalni_naziv":originalni_film,"godina_izdavanja":godina,"redatelj":redatelj,"opis":opis_filma,"trailer":trailer,"poster":poster,"slika":image.filename})
					db.commit()
			return render_template("akcija.html")
			
	return render_template("akcija.html")
	
@app.route("/drama", methods=["GET","POST"])
def unos_drame(): 
	if request.method == "POST":
		kategorija_filma = request.form.get("kategorija")
		originalni_film = request.form.get("originalni_film")
		godina = request.form.get("godina")
		redatelj = request.form.get("redatelj")
		opis_filma = request.form.get("opis_filma")
		trailer = request.form.get("trailer")
		poster = request.form.get("poster")
		
		if request.files:
			image = request.files["image"]
			
			if image.filename == "": 
				return redirect(request.url)
			
			if not allowed_image(image.filename): 
				
				return redirect(request.url)
				
			else: 
				filename = secure_filename(image.filename)
				image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
			
				if kategorija_filma != "" and originalni_film != "" and godina != "" and redatelj != "" and opis_filma != "":
					db.execute("INSERT INTO Filmovi(naziv_kategorije,originalni_naziv,godina_izdavanja,redatelj,opis,trailer,poster,slika) VALUES (:naziv_kategorije,:originalni_naziv,:godina_izdavanja,:redatelj,:opis,:trailer,:poster,:slika)", {"naziv_kategorije":kategorija_filma,"originalni_naziv":originalni_film,"godina_izdavanja":godina,"redatelj":redatelj,"opis":opis_filma,"trailer":trailer,"poster":poster,"slika":image.filename})
					db.commit()
			return render_template("drama.html")
			
	return render_template("drama.html")

@app.route("/horor", methods=["GET","POST"])
def unos_horora(): 
	if request.method == "POST":
		kategorija_filma = request.form.get("kategorija")
		originalni_film = request.form.get("originalni_film")
		godina = request.form.get("godina")
		redatelj = request.form.get("redatelj")
		opis_filma = request.form.get("opis_filma")
		trailer = request.form.get("trailer")
		poster = request.form.get("poster")
		
		if request.files:
			image = request.files["image"]
			
			if image.filename == "": 
				return redirect(request.url)
			
			if not allowed_image(image.filename): 
				
				return redirect(request.url)
				
			else: 
				filename = secure_filename(image.filename)
				image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
			
				if kategorija_filma != "" and originalni_film != "" and godina != "" and redatelj != "" and opis_filma != "":
					db.execute("INSERT INTO Filmovi(naziv_kategorije,originalni_naziv,godina_izdavanja,redatelj,opis,trailer,poster,slika) VALUES (:naziv_kategorije,:originalni_naziv,:godina_izdavanja,:redatelj,:opis,:trailer,:poster,:slika)", {"naziv_kategorije":kategorija_filma,"originalni_naziv":originalni_film,"godina_izdavanja":godina,"redatelj":redatelj,"opis":opis_filma,"trailer":trailer,"poster":poster,"slika":image.filename})
					db.commit()
			return render_template("horor.html")
			
	return render_template("horor.html")
	
@app.route("/komedija", methods=["GET","POST"])
def unos_komedija(): 
	if request.method == "POST":
		kategorija_filma = request.form.get("kategorija")
		originalni_film = request.form.get("originalni_film")
		godina = request.form.get("godina")
		redatelj = request.form.get("redatelj")
		opis_filma = request.form.get("opis_filma")
		trailer = request.form.get("trailer")
		poster = request.form.get("poster")
		
		if request.files:
			image = request.files["image"]
			
			if image.filename == "": 
				return redirect(request.url)
			
			if not allowed_image(image.filename): 
				
				return redirect(request.url)
				
			else: 
				filename = secure_filename(image.filename)
				image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
			
				if kategorija_filma != "" and originalni_film != "" and godina != "" and redatelj != "" and opis_filma != "":
					db.execute("INSERT INTO Filmovi(naziv_kategorije,originalni_naziv,godina_izdavanja,redatelj,opis,trailer,poster,slika) VALUES (:naziv_kategorije,:originalni_naziv,:godina_izdavanja,:redatelj,:opis,:trailer,:poster,:slika)", {"naziv_kategorije":kategorija_filma,"originalni_naziv":originalni_film,"godina_izdavanja":godina,"redatelj":redatelj,"opis":opis_filma,"trailer":trailer,"poster":poster,"slika":image.filename})
					db.commit()
			return render_template("komedija.html")
			
	return render_template("komedija.html")

@app.route("/triler", methods=["GET","POST"])
def unos_trilera(): 
	if request.method == "POST":
		kategorija_filma = request.form.get("kategorija")
		originalni_film = request.form.get("originalni_film")
		godina = request.form.get("godina")
		redatelj = request.form.get("redatelj")
		opis_filma = request.form.get("opis_filma")
		trailer = request.form.get("trailer")
		poster = request.form.get("poster")
		
		if request.files:
			image = request.files["image"]
			
			if image.filename == "": 
				return redirect(request.url)
			
			if not allowed_image(image.filename): 
				
				return redirect(request.url)
				
			else: 
				filename = secure_filename(image.filename)
				image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
			
				if kategorija_filma != "" and originalni_film != "" and godina != "" and redatelj != "" and opis_filma != "":
					db.execute("INSERT INTO Filmovi(naziv_kategorije,originalni_naziv,godina_izdavanja,redatelj,opis,trailer,poster,slika) VALUES (:naziv_kategorije,:originalni_naziv,:godina_izdavanja,:redatelj,:opis,:trailer,:poster,:slika)", {"naziv_kategorije":kategorija_filma,"originalni_naziv":originalni_film,"godina_izdavanja":godina,"redatelj":redatelj,"opis":opis_filma,"trailer":trailer,"poster":poster,"slika":image.filename})
					db.commit()
			return render_template("triler.html")
			
	return render_template("triler.html")

@app.route("/kartaske", methods=["GET","POST"])
def unos_kigara(): 
	if request.method == "POST":
		kategorija = request.form.get("kategorija")
		naziv = request.form.get("naziv")
		broj = request.form.get("broj")
		opis = request.form.get("opis")
		link = request.form.get("link")
		poster = request.form.get("poster")
		
		if request.files:
			image = request.files["image"]
			
			if image.filename == "": 
				return redirect(request.url)
			
			if not allowed_image(image.filename): 
				
				return redirect(request.url)
				
			else: 
				filename = secure_filename(image.filename)
				image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
			
				if kategorija != "" and naziv != "" and broj != "" and link != "":
					db.execute("INSERT INTO Drustvene_igre(kategorija,naziv,broj,opis,link,poster,slika) VALUES (:kategorija,:naziv,:broj,:opis,:link,:poster,:slika)", {"kategorija":kategorija,"naziv":naziv,"broj":broj,"opis":opis,"link":link,"poster":poster,"slika":image.filename})
					db.commit()
			return render_template("kartaske.html")
	return render_template("kartaske.html")

@app.route("/ploca", methods=["GET","POST"])
def unos_pigara(): 
	if request.method == "POST":
		kategorija = request.form.get("kategorija")
		naziv = request.form.get("naziv")
		broj = request.form.get("broj")
		opis = request.form.get("opis")
		link = request.form.get("link")
		poster = request.form.get("poster")
		
		if request.files:
			image = request.files["image"]
			
			if image.filename == "": 
				return redirect(request.url)
			
			if not allowed_image(image.filename): 
				
				return redirect(request.url)
				
			else: 
				filename = secure_filename(image.filename)
				image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
			
				if kategorija != "" and naziv != "" and broj != "" and link != "":
					db.execute("INSERT INTO Drustvene_igre(kategorija,naziv,broj,opis,link,poster,slika) VALUES (:kategorija,:naziv,:broj,:opis,:link,:poster,:slika)", {"kategorija":kategorija,"naziv":naziv,"broj":broj,"opis":opis,"link":link,"poster":poster,"slika":image.filename})
					db.commit()
			return render_template("igre.html")
	return render_template("igre.html")

@app.route("/pregled_drustvenih", methods=["GET","POST"])
def pregled_drustvenih(): 
	if request.method == "POST":
		
		drustvene = request.form.get("drustvene")
		
		cur.execute("SELECT * FROM Drustvene_igre WHERE naziv=:naziv",{"naziv":drustvene})
		dataa= cur.fetchall()
		
	return render_template("pregled_drustvenih_igara.html",data=dataa)

@app.route("/izbrisi_igru", methods=["GET","POST"])
def izbrisi_igru(): 
	
	igra = request.form.get("izbrisi")
		
	if igra != "": 
		db.execute("DELETE FROM Drustvene_igre WHERE naziv=:naziv",{"naziv":igra})
		db.commit()
	
		return render_template("kartaske.html")
		
	return render_template("kartaske.html")

@app.route("/lista_drustvena", methods=["GET","POST"])
def lista_drustvena(): 
	if request.method == "POST":
		naziv = request.form.get("naziv")
		datum = request.form.get("datum") 
		
		if naziv != "":
		
			db.execute("INSERT INTO Moja_lista(naziv_ponude,datum) VALUES (:naziv_ponude,:datum)", {"naziv_ponude":naziv,"datum":datum})
			db.commit()
			
			return render_template("moja_lista.html")
		else: 
			return render_template("pregled_drustvenih_igara.html")
			
	return render_template("pregled_drustvenih_igara.html")
	
@app.route("/moja_lista", methods=["GET","POST"])
def moja_lista():
	if request.method == "POST":
	
		naziv_ponude = request.form.get("naziv_ponude")
		datum = request.form.get("datum")

		if datum != "": 
			cur.execute("SELECT * FROM Moja_lista WHERE datum=:datum",{"datum":datum})
			dataa = cur.fetchall()
			return render_template("moja_lista.html",data=dataa)
			
	return render_template("moja_lista.html")

@app.route("/moja_lista_brisi", methods=["GET","POST"])
def moja_lista_brisi():
	if request.method == "POST":
	
		naziv_ponude = request.form.get("naziv_ponude")
		datum = request.form.get("datumm")
		brisi = request.form.get("brisi")	

		if datum != "": 
			cur.execute("SELECT * FROM Moja_lista WHERE datum=:datum",{"datum":datum})
			dataa = cur.fetchall()
		
			cur.execute("DELETE FROM Moja_lista WHERE naziv_ponude=:naziv_ponude AND datum=:datum",{"naziv_ponude":brisi,"datum":datum})
			data = cur.fetchall()
			return render_template("moja_lista.html",data=dataa)
	return render_template("moja_lista.html")	

@app.route("/update", methods=["GET","POST"])
def update(): 
	if request.method == "POST": 
		destinacija = request.form.get("destinacija")
		adresa = request.form.get("adresa")
		broj = request.form.get("broj")
		email = request.form.get("email")
		opis = request.form.get("opis")
		poster = request.form.get("poster")
		
		id = request.form.get("id")
		
		db.execute("UPDATE Izlazak SET destinacija=:destinacija,adresa =:adresa,broj=:broj,email=:email,opis=:opis,poster=:poster WHERE id=:id",(destinacija,adresa,broj,email,opis,poster,id))
		db.commit()
	return render_template("restorani.html")
	
@app.route("/update_film", methods=["GET","POST"])
def update_film(): 
	if request.method == "POST": 
		naziv = request.form.get("naziv")
		godina = request.form.get("godina")
		redatelj = request.form.get("redatelj")
		opis = request.form.get("opis")
		trailer = request.form.get("trailer")
		poster = request.form.get("poster")
		id = request.form.get("id")
		
		db.execute("UPDATE Filmovi SET originalni_naziv =:originalni_naziv,godina_izdavanja=:godina_izdavanja,redatelj=:redatelj,opis=:opis,trailer=:trailer,poster=:poster WHERE id=:id",(naziv,godina,redatelj,opis,trailer,poster,id))
		db.commit()
	return render_template("akcija.html")

@app.route("/update_drustvene", methods=["GET","POST"])
def update_drustvene(): 
	if request.method == "POST": 
		naziv = request.form.get("naziv")
		broj = request.form.get("broj")
		opis = request.form.get("opis")
		link = request.form.get("link")
		poster = request.form.get("poster")
		id = request.form.get("id")
		
		db.execute("UPDATE Drustvene_igre SET naziv =:naziv,broj=:broj,opis=:opis,link=:link,poster=:poster WHERE id=:id",(naziv,broj,opis,link,poster,id))
		db.commit()
	return render_template("kartaske.html")
	
if __name__=="__main__": 
    app.secret_key=os.urandom(12)
    app.run(debug=True,host='0.0.0.0',port=8000)
	