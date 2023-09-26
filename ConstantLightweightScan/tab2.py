import tkinter as tk
from tkinter import ttk
import os
import sqlite3

def create_tab2(tab_control):

    tab2 = ttk.Frame(tab_control)
    tab_control.add(tab2, text="Show specific results")

    database_folder = "database"
    database_files = [file for file in os.listdir(database_folder) if file.endswith((".db", ".sqlite"))]

    # Global variable to store the current database connection
    current_db_connection = None

    # Funktion zum Verbinden mit der Datenbank und Abfragen der Subdomain-Namen
    def query_subdomain_names():
        global current_db_connection
        # Frame zum Anzeigen der Listbox und des Buttons
        result_frame = ttk.LabelFrame(tab2, text="Ergebnisse")
        result_frame.grid(row=6, column=9, columnspan=4, padx=5, pady=5, sticky="ew")

        # Erstelle einen Treeview mit mehreren Spalten
        treeview_results = ttk.Treeview(result_frame, columns=("Name"), show="headings")
        treeview_results.pack()

        # Setze die Breite der Spalten
        treeview_results.column("Name", width=150)

            # Setze die Spaltentitel
        treeview_results.heading("Name", text="Name")
        # Stelle sicher, dass eine Datenbankverbindung vorhanden ist
        if current_db_connection is None:
            return

        # Erstelle einen Cursor für die Datenbank
        cursor = current_db_connection.cursor()

        # SQL-Abfrage, um alle Subdomain-Namen abzurufen
        query = "SELECT name FROM Subdomains"
        cursor.execute(query)
        subdomain_names = cursor.fetchall()

        # Lösche vorherige Anzeigen in der GUI, falls vorhanden
        for widget in treeview_results.winfo_children():
            widget.destroy()

        # Zeige die Subdomain-Namen in der Listbox an
        for name in subdomain_names:
            treeview_results.insert("", tk.END, values=name[0])
        
    def query_subdomain_names_sources():
        global current_db_connection

        # Frame zum Anzeigen der Listbox und des Buttons
        result_frame = ttk.LabelFrame(tab2, text="Ergebnisse")
        result_frame.grid(row=6, column=9, columnspan=4, padx=5, pady=5, sticky="ew")

        # Erstelle einen Treeview mit mehreren Spalten
        treeview_results = ttk.Treeview(result_frame, columns=("Name", "Quelle"), show="headings")
        treeview_results.pack()

        # Setze die Breite der Spalten
        treeview_results.column("Name", width=150)
        treeview_results.column("Quelle", width=150)

            # Setze die Spaltentitel
        treeview_results.heading("Name", text="Name")
        treeview_results.heading("Quelle", text="Quelle")

        if current_db_connection is None:
            return

        cursor = current_db_connection.cursor()
        query = "SELECT name, quelle FROM Subdomains"
        cursor.execute(query)
        subdomain_data = cursor.fetchall()

        # Lösche vorherige Anzeigen im Treeview, falls vorhanden
        for row in treeview_results.get_children():
            treeview_results.delete(row)

        # Füge die Daten im Treeview ein
        for data in subdomain_data:
            treeview_results.insert("", tk.END, values=data)

    def query_subdomain_ip_source():
        global current_db_connection

        # Frame zum Anzeigen der Listbox und des Buttons
        result_frame = ttk.LabelFrame(tab2, text="Ergebnisse")
        result_frame.grid(row=6, column=9, columnspan=4, padx=5, pady=5, sticky="ew")

        # Erstelle einen Treeview mit mehreren Spalten
        treeview_results = ttk.Treeview(result_frame, columns=("Name", "IP", "Quelle"), show="headings")
        treeview_results.pack()

        # Setze die Breite der Spalten
        treeview_results.column("Name", width=150)
        treeview_results.column("IP", width=150)
        treeview_results.column("Quelle", width=150)

        # Setze die Spaltentitel
        treeview_results.heading("Name", text="Name")
        treeview_results.heading("IP", text="IP")
        treeview_results.heading("Quelle", text="Quelle")

        if current_db_connection is None:
            return

        cursor = current_db_connection.cursor()
        
        # SQL-Abfrage, um Subdomain-Namen, IP-Adressen und Quellen aus den Tabellen abzurufen
        query = '''
            SELECT Subdomains.name, IPAddresses.ip_address, IPAddresses.quelle
            FROM Subdomains
            INNER JOIN IPAddresses ON Subdomains.id = IPAddresses.subdomain_id
        '''
        cursor.execute(query)
        subdomain_data = cursor.fetchall()

        # Lösche vorherige Anzeigen im Treeview, falls vorhanden
        for row in treeview_results.get_children():
            treeview_results.delete(row)

        # Füge die Daten im Treeview ein
        for data in subdomain_data:
            treeview_results.insert("", tk.END, values=data)

    def query_subdomain_ip_port_source():
        global current_db_connection

        # Frame zum Anzeigen der Listbox und des Buttons
        result_frame = ttk.LabelFrame(tab2, text="Ergebnisse")
        result_frame.grid(row=6, column=9, columnspan=4, padx=5, pady=5, sticky="ew")

        # Erstelle einen Treeview mit mehreren Spalten
        treeview_results = ttk.Treeview(result_frame, columns=("Name", "IP", "Port", "Quelle"), show="headings")
        treeview_results.pack()

        # Setze die Breite der Spalten
        treeview_results.column("Name", width=150)
        treeview_results.column("IP", width=150)
        treeview_results.column("Port", width=150)
        treeview_results.column("Quelle", width=150)

        # Setze die Spaltentitel
        treeview_results.heading("Name", text="Name")
        treeview_results.heading("IP", text="IP")
        treeview_results.heading("Port", text="Port")
        treeview_results.heading("Quelle", text="Quelle")

        if current_db_connection is None:
            return

        cursor = current_db_connection.cursor()
        
        # SQL-Abfrage, um Subdomain-Namen, IP-Adressen und Ports aus den Tabellen abzurufen
        query = '''
            SELECT Subdomains.name, IPAddresses.ip_address, OpenPorts.port, IPAddresses.quelle
            FROM Subdomains
            INNER JOIN IPAddresses ON Subdomains.id = IPAddresses.subdomain_id
            INNER JOIN OpenPorts ON IPAddresses.id = OpenPorts.ip_id
        '''
        cursor.execute(query)
        subdomain_data = cursor.fetchall()

        # Lösche vorherige Anzeigen im Treeview, falls vorhanden
        for row in treeview_results.get_children():
            treeview_results.delete(row)

        # Füge die Daten im Treeview ein
        for data in subdomain_data:
            treeview_results.insert("", tk.END, values=data)

    def query_subdomain_ip_port_service_source():
        global current_db_connection

        # Frame zum Anzeigen der Listbox und des Buttons
        result_frame = ttk.LabelFrame(tab2, text="Ergebnisse")
        result_frame.grid(row=6, column=9, columnspan=4, padx=5, pady=5, sticky="ew")

        # Erstelle einen Treeview mit mehreren Spalten
        treeview_results = ttk.Treeview(result_frame, columns=("Name", "IP", "Port", "Service", "Version", "Quelle"), show="headings")
        treeview_results.pack()

        # Setze die Breite der Spalten
        treeview_results.column("Name", width=150)
        treeview_results.column("IP", width=150)
        treeview_results.column("Port", width=150)
        treeview_results.column("Service", width=150)
        treeview_results.column("Version", width=150)
        treeview_results.column("Quelle", width=150)

        # Setze die Spaltentitel
        treeview_results.heading("Name", text="Name")
        treeview_results.heading("IP", text="IP")
        treeview_results.heading("Port", text="Port")
        treeview_results.heading("Service", text="Service")
        treeview_results.heading("Version", text="Version")
        treeview_results.heading("Quelle", text="Quelle")

        if current_db_connection is None:
            return

        cursor = current_db_connection.cursor()
        
        # SQL-Abfrage, um Subdomain-Namen, IP-Adressen und Ports aus den Tabellen abzurufen
        query = '''
            SELECT Subdomains.name, IPAddresses.ip_address, OpenPorts.port, services.service, services.version, IPAddresses.quelle
            FROM Subdomains
            INNER JOIN IPAddresses ON Subdomains.id = IPAddresses.subdomain_id
            INNER JOIN OpenPorts ON IPAddresses.id = OpenPorts.ip_id
            INNER JOIN services ON IPAddresses.id = services.ip_id
        '''
        cursor.execute(query)
        subdomain_data = cursor.fetchall()

        # Lösche vorherige Anzeigen im Treeview, falls vorhanden
        for row in treeview_results.get_children():
            treeview_results.delete(row)

        # Füge die Daten im Treeview ein
        for data in subdomain_data:
            treeview_results.insert("", tk.END, values=data)


    def refresh_database_list():
        # Hier aktualisieren Sie die Listbox mit den aktuellen Datenbankdateien
        listbox_dbs.delete(0, tk.END)  # Löscht alle Einträge in der Listbox
        for db_file in database_files:
            print(db_file)
            listbox_dbs.insert(tk.END, db_file)
            
    def select_database():
        global current_db_connection  # Definiere, dass du auf die globale Variable zugreifen möchtest

        # Hole den ausgewählten Eintrag aus der Listbox
        selected_item = listbox_dbs.get(listbox_dbs.curselection())

        # Verbinde mit der ausgewählten Datenbank und speichere die Verbindung global
        current_db_connection = sqlite3.connect('database/' + selected_item)

        # Erstelle einen Cursor für die Datenbank
        cursor = current_db_connection.cursor()
        


        # Erstelle einen Kasten (Rahmen) für die Subdomain-Eingabe
    database_frame = ttk.LabelFrame(tab2, text="Datenbank wählen")
    database_frame.grid(row=6, column=0, columnspan=4, padx=5, pady=5, sticky="ew")

    listbox_dbs = tk.Listbox(database_frame)
    listbox_dbs.pack()

    for db_file in database_files:
        listbox_dbs.insert(tk.END, db_file)

    # Refresh-Button hinzufügen
    refresh_button = tk.Button(database_frame, text="Refresh", command=refresh_database_list)
    refresh_button.pack()

    select_db_button = tk.Button(database_frame, text="Auswählen", command=select_database)
    select_db_button.pack()

    subdomain_frame = ttk.LabelFrame(tab2, text="Subdomainanzeige")
    subdomain_frame.grid(row=6, column=5, columnspan=4, padx=5, pady=5, sticky="ew")

    button_frame = ttk.LabelFrame(tab2, text="Subdomainanzeige")
    button_frame.grid(row=6, column=4, columnspan=4, padx=5, pady=5, sticky="ew")

    # Button zum Auslösen der Abfrage
    query_subs_button = ttk.Button(button_frame, text="Subdomains", command=query_subdomain_names, width=50)
    query_subs_button.pack()

    # Button zum Auslösen der Abfrage
    query_subs_source_button = ttk.Button(button_frame, text="Subdomains-Quellen", command=query_subdomain_names_sources, width=50)
    query_subs_source_button.pack()

    # Button zum Auslösen der Abfrage
    query_ips_button = ttk.Button(button_frame, text="Subdomains-IPs", command=query_subdomain_ip_source, width=50)
    query_ips_button.pack()

    # Button zum Auslösen der Abfrage
    query_ports_button = ttk.Button(button_frame, text="Subdomains-IP-Port", command=query_subdomain_ip_port_source, width=50)
    query_ports_button.pack()

    # Button zum Auslösen der Abfrage
    query_service_button = ttk.Button(button_frame, text="Subdomains-IP-Port-Service", command=query_subdomain_ip_port_service_source, width=50)
    query_service_button.pack()

    return tab2
