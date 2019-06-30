#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 15:48:40 2019

@author: kristijan
"""

from pony import orm 
import os 

db =orm.Database()

db.bind(provider='sqlite',filename='baza.db',create_db=True)

class Korisnik(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    ime = orm.Required(str)
    prezime = orm.Required(str)
    email = orm.Required(str)
    lozinka = orm.Required(str)

class Filmovi(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    naziv_kategorije = orm.Required(str)
    originalni_naziv = orm.Required(str)
    godina_izdavanja = orm.Required(int)
    redatelj = orm.Required(str)
    opis = orm.Required(str)
    trailer = orm.Required(str)
    poster = orm.Required(str)
    slika = orm.Required(str) 

class Izlazak(db.Entity): 
    id = orm.PrimaryKey(int, auto=True)
    kategorija = orm.Required(str)
    destinacija = orm.Required(str)
    adresa = orm.Required(str)
    broj = orm.Required(int)
    email = orm.Required(str)
    opis = orm.Required(str)
    poster = orm.Required(str)
    slika = orm.Required(str)

class Drustvene_igre(db.Entity): 
    id = orm.PrimaryKey(int, auto=True)
    kategorija = orm.Required(str)
    naziv = orm.Required(str)
    broj = orm.Required(int)
    opis = orm.Required(str)
    link = orm.Required(str)
    poster = orm.Required(str)
    slika = orm.Required(str)

class Moja_lista(db.Entity): 
    id = orm.PrimaryKey(int, auto=True)
    naziv_ponude  = orm.Required(str)
    datum = orm.Required(str)
    
db.generate_mapping(check_tables=True,create_tables=True)
    



