import tkinter as tk
from tkinter import ttk, filedialog
import os
import sqlite3
from createDB import SubdomainDatabase
from datetime import date

def create_tab1(tab_control):

    tab1 = ttk.Frame(tab_control)
    tab_control.add(tab1, text="Inser Subdomains and Values")

    #db = SubdomainDatabase()
    db = None
    
    # Funktion zum Erstellen einer neuen Datenbank oder Verbindung zu einer vorhandenen Datenbank
    def choose_database():
        global db
        
        # Öffne ein Dateiauswahldialogfeld
        db_file = filedialog.askopenfilename(filetypes=[("SQLite Database Files", "*.db *.sqlite")])
        
        if db_file:
            # Verbinde zur ausgewählten Datenbank oder erstelle eine neue, falls sie nicht existiert
            db = sqlite3.connect(db_file)

            # Hier können Sie die Verbindung verwenden, z.B. Abfragen ausführen
            print("Verbindung zur Datenbank hergestellt:", db_file)
        

    def add_subdomain():
        global db
        subdomain_name = subdomain_only_name_entry.get()
        subdomain_quelle = subdomain_quelle_entry.get()
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


    # Erstelle einen Kasten (Rahmen) für die Subdomain-Eingabe
    db_frame = ttk.LabelFrame(tab1, text="DB")
    db_frame.grid(row=6, column=0, columnspan=4, padx=5, pady=5, sticky="ew")

    # Button zum Hinzufügen der Subdomain innerhalb des Rahmens
    choos_db_button = ttk.Button(db_frame, text="Choos Database", command=choose_database)
    choos_db_button.grid(row=1, column=4, columnspan=3, padx=5, pady=5)

    # Erstelle einen Kasten (Rahmen) für die Subdomain-Eingabe
    subdomain_frame = ttk.LabelFrame(tab1, text="Subdomain Eingabe")
    subdomain_frame.grid(row=8, column=0, columnspan=4, padx=5, pady=5, sticky="ew")

    # Label und Entry-Feld für den Subdomain-Namen innerhalb des Rahmens
    subdomain_only_name_label = ttk.Label(subdomain_frame, text="Subdomain Name:", width=50)
    subdomain_only_name_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
    subdomain_only_name_entry = ttk.Entry(subdomain_frame, width=50)
    subdomain_only_name_entry.grid(row=0, column=1, columnspan=3, sticky=tk.W, padx=5, pady=5)

    # Label und Entry-Feld für die Subdomain-Quelle innerhalb des Rahmens
    subdomain_quelle_label = ttk.Label(subdomain_frame, text="Subdomain Quelle:", width=50)
    subdomain_quelle_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
    subdomain_quelle_entry = ttk.Entry(subdomain_frame, width=50)
    subdomain_quelle_entry.grid(row=1, column=1, columnspan=3, sticky=tk.W, padx=5, pady=5)

    # Button zum Hinzufügen der Subdomain innerhalb des Rahmens
    add_subdomain_button = ttk.Button(subdomain_frame, text="Add Subdomain", command=add_subdomain)
    add_subdomain_button.grid(row=1, column=4, columnspan=3, padx=5, pady=5)





    # Erstelle einen Kasten (Rahmen) für die IP-Adressen-Eingabe
    ip_address_frame = ttk.LabelFrame(tab1, text="IP-Adressen Eingabe")
    ip_address_frame.grid(row=12, column=0, columnspan=4, padx=5, pady=5, sticky="ew")

    # Label und Entry-Feld für den Subdomain-Namen innerhalb des Rahmens
    subdomain_name_label = ttk.Label(ip_address_frame, text="Subdomain Name:", width=50)
    subdomain_name_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
    subdomain_name_entry = ttk.Entry(ip_address_frame, width=50)
    subdomain_name_entry.grid(row=0, column=1, columnspan=3, sticky=tk.W, padx=5, pady=5)

    # Label und Entry-Feld für die IP-Adresse innerhalb des Rahmens
    ip_address_label = ttk.Label(ip_address_frame, text="IP Address:", width=50)
    ip_address_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
    ip_address_entry = ttk.Entry(ip_address_frame, width=50)
    ip_address_entry.grid(row=1, column=1, columnspan=3, sticky=tk.W, padx=5, pady=5)

    # Label und Entry-Feld für die Subdomain-Quelle innerhalb des Rahmens
    ip_quelle_label = ttk.Label(ip_address_frame, text="IP Quelle:", width=50)
    ip_quelle_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
    ip_quelle_entry = ttk.Entry(ip_address_frame, width=50)
    ip_quelle_entry.grid(row=2, column=1, columnspan=3, sticky=tk.W, padx=5, pady=5)

    # Button zum Hinzufügen der IP-Adresse innerhalb des Rahmens
    add_ip_button = ttk.Button(ip_address_frame, text="Add IP", command=add_ip)
    add_ip_button.grid(row=2, column=4, columnspan=3, padx=5, pady=5)




    # Erstelle einen Kasten (Rahmen) für die Ports-Eingabe
    ports_frame = ttk.LabelFrame(tab1, text="Ports Eingabe")
    ports_frame.grid(row=16, column=0, columnspan=4, padx=5, pady=5, sticky="ew")

    # Label und Entry-Feld für die IP-Adresse innerhalb des Rahmens
    ip_address_port_label = ttk.Label(ports_frame, text="IP Address:", width=50)
    ip_address_port_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
    ip_address_port_entry = ttk.Entry(ports_frame, width=50)
    ip_address_port_entry.grid(row=0, column=1, columnspan=3, sticky=tk.W, padx=5, pady=5)

    # Label und Entry-Feld für den Port innerhalb des Rahmens
    port_label = ttk.Label(ports_frame, text="Port:", width=50)
    port_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
    port_entry = ttk.Entry(ports_frame, width=50)
    port_entry.grid(row=1, column=1, columnspan=3, sticky=tk.W, padx=5, pady=5)

    # Label und Entry-Feld für die Subdomain-Quelle innerhalb des Rahmens
    port_quelle_label = ttk.Label(ports_frame, text="Port Quelle:", width=50)
    port_quelle_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
    port_quelle_entry = ttk.Entry(ports_frame, width=50)
    port_quelle_entry.grid(row=2, column=1, columnspan=3, sticky=tk.W, padx=5, pady=5)

    # Button zum Hinzufügen des Ports innerhalb des Rahmens
    add_port_button = ttk.Button(ports_frame, text="Add Port", command=add_port)
    add_port_button.grid(row=2, column=4, columnspan=3, padx=5, pady=5)




    # Erstelle einen Kasten (Rahmen) für die Services-Eingabe
    services_frame = ttk.LabelFrame(tab1, text="Services Eingabe")
    services_frame.grid(row=20, column=0, columnspan=4, padx=5, pady=5, sticky="ew")

    ip_address_port_service_label = ttk.Label(services_frame, text="IP Address:")
    ip_address_port_service_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
    ip_address_port_service_entry = ttk.Entry(services_frame, width=50)
    ip_address_port_service_entry.grid(row=0, column=1, columnspan=3, sticky=tk.W, padx=5, pady=5)

    # Label und Entry-Feld für den Port innerhalb des Rahmens
    port_service_label = ttk.Label(services_frame, text="Port:")
    port_service_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
    port_service_entry = ttk.Entry(services_frame, width=50)
    port_service_entry.grid(row=1, column=1, columnspan=3, sticky=tk.W, padx=5, pady=5)

    # Label und Entry-Feld für den Service innerhalb des Rahmens
    service_label = ttk.Label(services_frame, text="Service:", width=50)
    service_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
    service_entry = ttk.Entry(services_frame, width=50)
    service_entry.grid(row=2, column=1, columnspan=3, sticky=tk.W, padx=5, pady=5)

    # Label und Entry-Feld für die Version innerhalb des Rahmens
    service_version_label = ttk.Label(services_frame, text="Version:", width=50)
    service_version_label.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
    service_version_entry = ttk.Entry(services_frame, width=50)
    service_version_entry.grid(row=3, column=1, columnspan=3, sticky=tk.W, padx=5, pady=5)

    # Label und Entry-Feld für die Subdomain-Quelle innerhalb des Rahmens
    service_quelle_label = ttk.Label(services_frame, text="Service Quelle:", width=50)
    service_quelle_label.grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
    service_quelle_entry = ttk.Entry(services_frame, width=50)
    service_quelle_entry.grid(row=4, column=1, columnspan=3, sticky=tk.W, padx=5, pady=5)

    # Button zum Hinzufügen des Services innerhalb des Rahmens
    add_service_button = ttk.Button(services_frame, text="Add Service", command=add_service)
    add_service_button.grid(row=4, column=4, columnspan=3, padx=5, pady=5)

    return tab1