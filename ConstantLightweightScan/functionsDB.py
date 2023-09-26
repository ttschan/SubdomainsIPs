import tkinter as tk
from tkinter import ttk, filedialog
import os
import sqlite3
from createDB import SubdomainDatabase
from datetime import date

def choose_database():
        global db
        
        # Öffne ein Dateiauswahldialogfeld
        db_file = filedialog.askopenfilename(filetypes=[("SQLite Database Files", "*.db *.sqlite")])
        
        if db_file:
            # Verbinde zur ausgewählten Datenbank oder erstelle eine neue, falls sie nicht existiert
            db = sqlite3.connect(db_file) 

            # Hier können Sie die Verbindung verwenden, z.B. Abfragen ausführen
            print("Verbindung zur Datenbank hergestellt:", db_file)
        

        def add_subdomain(subdomain_name,subdomain_quelle):
            global db
            try:
                cursor = db.cursor()
                # SQL-Abfrage zum Einfügen von Daten
                query = "INSERT INTO Subdomains (name, keywords, quelle, datum) VALUES (?, ?, ?, ?)"
                cursor.execute(query, (subdomain_name, "", subdomain_quelle, date.today()))


                # Transaktion bestätigen
                db.commit()

                print(f"Subdomain '{subdomain_name}' wurde zur Datenbank hinzugefügt.")
            except Exception as e:
                print(f"Fehler beim Hinzufügen der Subdomain: {str(e)}")

        def find_subdomain_id_by_name(subdomain_name):
            global db
            try:
                cursor = db.cursor()
                query = "SELECT id FROM Subdomains WHERE name = ?"
                cursor.execute(query, (subdomain_name,))
                result = cursor.fetchone()

                if result:
                    return result[0]  # Die gefundene subdomain_id zurückgeben
                else:
                    return None  # Subdomain mit diesem Namen nicht gefunden
            except Exception as e:
                print(f"Fehler beim Suchen der Subdomain: {str(e)}")
                return None
            
        def add_ip():
            global db
            subdomain_name = subdomain_name_entry.get()
            ip_address = ip_address_entry.get()
            ip_quelle = ip_quelle_entry.get()
            try:
                subdomain_id = find_subdomain_id_by_name(subdomain_name)
                
                if subdomain_id is not None:
                    cursor = db.cursor()
                    query = "INSERT INTO IPAddresses (subdomain_id, ip_address, quelle, datum) VALUES (?, ?, ?, ?)"
                    cursor.execute(query, (subdomain_id, ip_address, ip_quelle, date.today()))
                    
                    # Transaktion bestätigen
                    db.commit()
                    
                    print(f"IP-Adresse '{ip_address}' wurde zur Datenbank für Subdomain '{subdomain_name}' hinzugefügt.")
                else:
                    print(f"Subdomain '{subdomain_name}' wurde nicht gefunden.")
            except Exception as e:
                print(f"Fehler beim Hinzufügen der IP-Adresse: {str(e)}")

        def find_ip_id_by_number(ip_address):
                global db
                try:
                    cursor = db.cursor()
                    query = "SELECT id FROM IPAddresses WHERE ip_address = ?"
                    cursor.execute(query, (ip_address,))
                    result = cursor.fetchone()

                    if result:
                        return result[0]  # Die gefundene subdomain_id zurückgeben
                    else:
                        return None  # Subdomain mit diesem Namen nicht gefunden
                except Exception as e:
                    print(f"Fehler beim Suchen der IP: {str(e)}")
                    return None
                
        def add_port():
            global db
            # Die Werte aus den Entry-Feldern abrufen
            ip_address = ip_address_port_entry.get()
            port = port_entry.get()
            port_quelle = port_quelle_entry.get()
            
            
            try:
                ip_id = find_ip_id_by_number(ip_address)
                print(ip_id)
                
                if ip_address is not None:
                    cursor = db.cursor()
                    query = "INSERT INTO OpenPorts (ip_id, port, quelle, datum) VALUES (?, ?, ?, ?)"
                    cursor.execute(query, (ip_id, port, port_quelle, date.today()))
                    
                    # Transaktion bestätigen
                    db.commit()
                    
                    print(f"Port '{port}' wurde zur Datenbank für IP-Adresse '{ip_address}' hinzugefügt.")
                else:
                    print(f"Adresse '{ip_address}' wurde nicht gefunden.")
            except Exception as e:
                print(f"Fehler beim Hinzufügen der IP-Adresse: {str(e)}")
                    
        def find_port_id_by_number(ip_id, port):
            global db
            try:
                cursor = db.cursor()
                query = "SELECT id FROM OpenPorts WHERE ip_id = ? AND port = ?"
                cursor.execute(query, (ip_id, port,))
                result = cursor.fetchone()

                if result:
                    return result[0]  # Die gefundene subdomain_id zurückgeben
                else:
                    return None  # Subdomain mit diesem Namen nicht gefunden
            except Exception as e:
                print(f"Fehler beim Suchen der Port_ID: {str(e)}")
                return None
                
        def add_service():
            global db
            # Die Werte aus den Entry-Feldern abrufen
            ip_address = ip_address_port_service_entry.get()
            port = port_service_entry.get()
            service = service_entry.get()
            version = service_version_entry.get()
            service_quelle= service_quelle_entry.get()
            
            
            try:
                ip_id = find_ip_id_by_number(ip_address)
                port_id = find_port_id_by_number(ip_id, port)
                print(ip_id, port_id)
                
                if ip_address is not None:
                    cursor = db.cursor()
                    query = "INSERT INTO services (ip_id, port_id, service, version, quelle, datum) VALUES (?, ?, ?, ?, ?, ?)"
                    cursor.execute(query, (ip_id, port_id, service, version, service_quelle, date.today()))
                    
                    # Transaktion bestätigen
                    db.commit()
                    
                    print(f"Service: '{service}' wurde zur Datenbank für port und IP '{port, ip_address}' hinzugefügt.")
                else:
                    print(f"Subdomain '{port, ip_address}' wurde nicht gefunden.")
            except Exception as e:
                print(f"Fehler beim Hinzufügen der IP-Adresse: {str(e)}")