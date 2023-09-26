import sqlite3
from tkinter import filedialog
from datetime import date
from getIPs import SubdomainSearch
import socket


class SubdomainDatabase:
    def __init__(self, db_file_path):
        self.db_name = db_file_path
        self.connection = sqlite3.connect(db_file_path)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Subdomains (
                id INTEGER PRIMARY KEY,
                name TEXT,
                keywords TEXT,
                quelle TEXT,
                datum DATE
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS IPAddresses (
                id INTEGER PRIMARY KEY,
                subdomain_id INTEGER,
                ip_address TEXT,
                quelle TEXT,
                datum DATE,
                FOREIGN KEY (subdomain_id) REFERENCES Subdomains (id)
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS OpenPorts (
                id INTEGER PRIMARY KEY,
                ip_id INTEGER,
                port INTEGER,
                quelle TEXT,
                datum DATE,
                FOREIGN KEY (ip_id) REFERENCES IPAddresses (id)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS services (
                id INTEGER PRIMARY KEY,
                ip_id INTEGER,
                port_id INTEGER,
                service string,
                version string,
                quelle TEXT,
                datum DATE,
                FOREIGN KEY (ip_id) REFERENCES IPAddresses (id),
                FOREIGN KEY (port_id) REFERENCES OpenPorts (id)
            )
        ''')
        
        self.connection.commit()

    def insert_subdomain(self, name, keywords='', quelle='', datum=''):
        try:
            self.cursor.execute('INSERT INTO Subdomains (name, keywords, quelle, datum) VALUES (?, ?, ?, ?)', (name, keywords, quelle, datum))
            self.connection.commit()
            # Die zuletzt eingefügte ID abrufen und zurückgeben
            subdomain_id = self.cursor.lastrowid
            return subdomain_id
        except sqlite3.Error as e:
            print("Fehler beim Einfügen in die Datenbank:", e)
            return None
    
    def insert_ip_address(self, subdomain_id, ip_address, quelle, datum):
        self.cursor.execute('INSERT INTO IPAddresses (subdomain_id, ip_address, quelle, datum) VALUES (?, ?, ?, ?)', (subdomain_id, ip_address, quelle, datum))
        self.connection.commit()
    
    def insert_open_port(self, ip_id, port, quelle, datum):
        self.cursor.execute('INSERT INTO OpenPorts (ip_id, port, quelle, datum) VALUES (?, ?, ?, ?)', (ip_id, port, quelle, datum))
        self.connection.commit()
    
    def insert_service(self, ip_id, port_id, service, version, quelle, datum):
        self.cursor.execute('INSERT INTO services (ip_id, port_id, service, version, quelle, datum) VALUES (?, ?, ?, ?, ?, ?)',
                            (ip_id, port_id, service, version, quelle, datum))
        self.connection.commit()

    def get_subdomain_id_by_name(self, name):
        self.cursor.execute('SELECT id FROM Subdomains WHERE name = ?', (name,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
        
    def get_ip_id_by_ip_address(self, ip_address):
        self.cursor.execute('SELECT id FROM IPAddresses WHERE ip_address = ?', (ip_address,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
        
    def get_port_id_by_port(self, port):
        query = "SELECT id FROM OpenPorts WHERE port = ?"
        self.cursor.execute(query, (port,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
        
    def get_all_subdomains(self):
        self.cursor.execute('SELECT name, quelle FROM Subdomains')
        subdomains = self.cursor.fetchall()
        return subdomains

    def get_ip_addresses_for_subdomain(self, subdomain_name):
        self.cursor.execute('SELECT ip_address FROM IPAddresses WHERE subdomain_id IN (SELECT DISTINCT id FROM Subdomains WHERE name = ?)', (subdomain_name,))
        ip_addresses = self.cursor.fetchall()
        ip_addresses = [ip[0] for ip in ip_addresses]
        return ip_addresses
    
    def get_subdomains(self):
        self.cursor.execute('SELECT DISTINCT name, quelle FROM Subdomains')  
        subdomains = self.cursor.fetchall()
        return subdomains
    
    def get_subdomain_id(self, subdomain_name):
        self.cursor.execute('SELECT id FROM Subdomains WHERE name = ?', (subdomain_name,))
        result = self.cursor.fetchone()
        if result:
            subdomain_id = result[0]
            return subdomain_id
        else:
            return None 
        
    def find_ips(self):
        subdomains = self.get_all_subdomains()
        for subdomain_info in subdomains:
            subdomain_name = subdomain_info[0]
            ip_addresses = SubdomainSearch.find_ip_addresses(subdomain_name)
            subdomain_id = self.get_subdomain_id(subdomain_name) 
            for ip_address in ip_addresses:
                ip_id = self.insert_ip_address(subdomain_id, ip_address, "", date.today())
        
        return self