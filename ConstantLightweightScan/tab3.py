import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sqlite3
import requests
import dns.resolver
from bs4 import BeautifulSoup
from datetime import date
import re
import clipboard
from createDB import SubdomainDatabase


def create_tab3(tab_control):
    db = None

    def choose_database():
        global db
        
        # Öffne ein Dateiauswahldialogfeld
        db_file = filedialog.askopenfilename(filetypes=[("SQLite Database Files", "*.db *.sqlite")])
        
        if db_file:
            # Verbinde zur ausgewählten Datenbank oder erstelle eine neue, falls sie nicht existiert
            db = SubdomainDatabase(db_file)

            # Hier können Sie die Verbindung verwenden, z.B. Abfragen ausführen
            print("Verbindung zur Datenbank hergestellt:", db_file)    

    # Funktion, die beim Klicken des Ausführungsbuttons aufgerufen wird
    def execute_function():
        selected_checkboxes = [name for name, var in checkbox_vars.items() if var.get()]
        print("Ausgewählte Checkboxen:", selected_checkboxes)
        
        if "VirusTotal" in selected_checkboxes:
            entry_text = virus_total_entry.get()
            print("Inhalt des VirusTotal-Eingabefelds:", entry_text)

    def toggle_virus_total_frame():
        if checkbox_vars["VirusTotal"].get():
            virus_total_frame.grid()
        else:
            virus_total_frame.grid_remove()

    def vt_subdomains(key, dom):
        api_key = key
        domain = dom

        headers = {
            "x-apikey": api_key
        }

        url = f"https://www.virustotal.com/api/v3/domains/{domain}/subdomains"
        all_subdomains = []

        while url:
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json()
                subdomains_data = data.get('data', [])
                subdomains = [item['id'] for item in subdomains_data]
                all_subdomains.extend(subdomains)
                url = data.get('links', {}).get('next', None)
            else:
                url = None

        return all_subdomains

    def transform_subdomains(subdomains):
        transformed_subdomains = []
        for subdomain in subdomains:
            subdomain_elements = subdomain.split('\n')
            transformed_subdomains.extend(subdomain_elements)
        return transformed_subdomains
    
    def crt_subdomains(dom):
        url = f"https://crt.sh/?q=%.{dom}&output=json"
        response = requests.get(url)
        crtsh_results = response.json()
        crtsh_subdomains = list(set([result['name_value'] for result in crtsh_results]))
        crtsh_subdomains = list(set(crtsh_subdomains))
        transformed_subdomains=transform_subdomains(crtsh_subdomains)
        return transformed_subdomains

    def get_records(domain, record_type='NS'):
        try:
            answers = dns.resolver.resolve(domain, record_type)
            subdomains = [str(ns) for ns in answers]
            return subdomains
        except Exception as e:
            return []

    def rapipddns_subdomains(dom):
        base_url = f"https://rapiddns.io/subdomain/{dom}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
        
        response = requests.get(base_url, headers=headers)
        subdomains = []
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            rows = soup.select("table.table tr")
            
            for row in rows[1:]:
                columns = row.find_all("td")
                if len(columns) >= 2:
                    subdomain = columns[0].get_text(strip=True)
                    subdomains.append(subdomain)
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
        
        return subdomains
    
    def remove_numbers(domain_list):
        cleaned_list = [re.sub(r'^\d+|\s', '', domain) for domain in domain_list]
        return cleaned_list

    def search_subdomains(vt_key, domain, checkbox_vars):
        global db
        processed_subdomains = set()

        if checkbox_vars["VirusTotal"].get():
            vt_subdomains_res = vt_subdomains(vt_key, domain)
            for subdomain in vt_subdomains_res:
                if (subdomain, "VirusTotal") not in processed_subdomains:
                    db.cursor.execute('INSERT INTO Subdomains (name, keywords, quelle, datum) VALUES (?, ?, ?, ?)', (subdomain, '', "VirusTotal", date.today()))
                    db.connection.commit()
                    processed_subdomains.add((subdomain, "VirusTotal"))

        if checkbox_vars["CRT"].get():
            crt_subdomains_res = crt_subdomains(domain)
            for subdomain in crt_subdomains_res:
                if (subdomain, "CRT") not in processed_subdomains:
                    db.cursor.execute('INSERT INTO Subdomains (name, keywords, quelle, datum) VALUES (?, ?, ?, ?)', (subdomain, '', "CRT", date.today()))
                    db.connection.commit()
                    processed_subdomains.add((subdomain, "CRT"))

        if checkbox_vars["DNSRecords"].get():
            dns_records_subdomains = get_records(domain)
            mx_records = remove_numbers(get_records(domain, 'MX'))
            dns_records_subdomains.extend(remove_numbers(mx_records))
            for subdomain in dns_records_subdomains:
                if (subdomain, "DNSRecords") not in processed_subdomains:
                    db.cursor.execute('INSERT INTO Subdomains (name, keywords, quelle, datum) VALUES (?, ?, ?, ?)', (subdomain, '', "DNSRecords", date.today()))
                    db.connection.commit()
                    processed_subdomains.add((subdomain, "DNSRecords"))

        if checkbox_vars["RapIDDNS"].get():
            rapiddns_subdomains = rapipddns_subdomains(domain)
            for subdomain in rapiddns_subdomains:
                if (subdomain, "RapIDDNS") not in processed_subdomains:
                    db.cursor.execute('INSERT INTO Subdomains (name, keywords, quelle, datum) VALUES (?, ?, ?, ?)', (subdomain, '', "RapIDDNS", date.today()))
                    db.connection.commit()
                    processed_subdomains.add((subdomain, "RapIDDNS"))

        return db

    def display_subdomains(subdomains):
        for item in subdomains_tree.get_children():
            subdomains_tree.delete(item)
        
        for subdomain_info in subdomains:
            subdomain_name, subdomain_source = subdomain_info
            subdomains_tree.insert("", "end", values=(subdomain_name, subdomain_source, "", ""))

    def search_subs_click():
        global db
        vt_key = virus_total_entry.get()
        dom = domain_entry.get()
        db = search_subdomains(vt_key, dom, checkbox_vars)
        subdomains = db.get_all_subdomains() 
        print(subdomains)
        display_subdomains(subdomains)
        messagebox.showinfo("Information", f"Found Subdomains and saved.")

    def copy_table_content():
        selected_items = subdomains_tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "No rows selected.")
            return
        
        copied_content = ""
        for item in selected_items:
            values = subdomains_tree.item(item, "values")
            copied_content += "\t".join(values) + "\n"
        
        clipboard.copy(copied_content)
        messagebox.showinfo("Information", "Selected rows copied to clipboard.")

    def select_all_rows():
        subdomains_tree.selection_set(subdomains_tree.get_children())

    def display_subdomains_ip_first(subdomains, db_instance):
        for item in subdomains_tree.get_children():
            subdomains_tree.delete(item)
        
        for subdomain_info in subdomains:
            subdomain_name, subdomain_source = subdomain_info
            ip_addresses = db_instance.get_ip_addresses_for_subdomain(subdomain_name)
            subdomains_tree.insert("", "end", values=(subdomain_name, subdomain_source, ", ".join(ip_addresses), ""))

    def search_IPs_click():
        global db
        db.find_ips()
        subdomains = db.get_subdomains()
        display_subdomains_ip_first(subdomains, db)
        messagebox.showinfo("Information", f"Found IPs and saved.")

    tab3 = ttk.Frame(tab_control)
    tab_control.add(tab3, text="Search Subdomain results")

     # Erstelle einen Kasten (Rahmen) für die Subdomain-Eingabe
    db_frame = ttk.LabelFrame(tab3, text="DB wahl")
    db_frame.grid(row=6, column=0, columnspan=4, padx=5, pady=5, sticky="ew")

        # Button zum Hinzufügen der Subdomain innerhalb des Rahmens
    choos_db_button = ttk.Button(db_frame, text="Add Subdomain", command=choose_database)
    choos_db_button.grid(row=1, column=4, columnspan=3, padx=5, pady=5)

    # Erstelle ein LabelFrame für die Checkboxen
    checkbox_frame = ttk.LabelFrame(tab3, text="Plattform to search")
    checkbox_frame.grid(row=7, column=0, columnspan=4, padx=5, pady=5, sticky="ew")

    # Checkbox-Variablen
    checkbox_vars = {
        "VirusTotal": tk.BooleanVar(),
        "CRT": tk.BooleanVar(),
        "DNSRecords": tk.BooleanVar(),
        "RapIDDNS": tk.BooleanVar()
    }

    # Checkboxen erstellen
    checkbox_labels = ["VirusTotal", "CRT", "DNSRecords", "RapIDDNS"]
    checkboxes = {}

    for label in checkbox_labels:
        checkboxes[label] = tk.Checkbutton(checkbox_frame, text=label, variable=checkbox_vars[label], command=toggle_virus_total_frame)

    # Checkboxen in der GUI platzieren
    for label, checkbox in checkboxes.items():
        checkbox.grid()

    virus_total_frame = ttk.LabelFrame(tab3, text="VirusTotal Eingabefeld:")
    virus_total_frame.grid(row=8, column=0, columnspan=4, padx=5, pady=5, sticky="ew")
    virus_total_entry = tk.Entry(virus_total_frame)
    # Das VirusTotal Frame initial ausblenden
    virus_total_frame.grid_remove()
    virus_total_entry.grid(row=0, column=0, padx=5, pady=5)

    # Ausführungsbutton erstellen
    execute_button = tk.Button(tab3, text="Ausführen", command=execute_function)
    execute_button.grid(row=10, column=0, columnspan=2, padx=5, pady=5)

    domain_frame = ttk.LabelFrame(tab3, text="Domain Eingabefeld:")
    domain_frame.grid(row=11, column=0, columnspan=4, padx=5, pady=5, sticky="ew")
    domain_label = ttk.Label(domain_frame, text="Domain Name:")
    domain_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
    domain_entry = ttk.Entry(domain_frame, width=50)
    domain_entry.grid(row=2, column=1, columnspan=3, sticky=tk.W, padx=5, pady=5)

    search_subs_button = ttk.Button(domain_frame, text="Search Subdomains", command=search_subs_click)
    search_subs_button.grid(row=3, column=1, padx=5, pady=5)

    search_ips_button = ttk.Button(tab3, text="Search IPs from Subdomain", command=search_IPs_click)
    search_ips_button.grid(row=3, column=2, padx=5, pady=5)

     # Erstelle einen Kasten (Rahmen) für die Subdomain-Eingabe
    result_frame = ttk.LabelFrame(tab3, text="Show Results")
    result_frame.grid(row=13, column=0, columnspan=4, padx=5, pady=5, sticky="ew")
    

    subdomains_tree = ttk.Treeview(result_frame, columns=("Subdomain", "Quelle", "IPs"), show="headings")
    subdomains_tree.heading("Subdomain", text="Subdomain")
    subdomains_tree.heading("Quelle", text="Quelle")
    subdomains_tree.heading("IPs", text="IPs")
    subdomains_tree.grid(row=5, column=0, columnspan=4, padx=5, pady=5, sticky="ew")

    select_all_button = ttk.Button(result_frame, text="Select All Rows", command=select_all_rows)
    select_all_button.grid(row=6, column=0, padx=5, pady=5)

    copy_button = ttk.Button(result_frame, text="Copy Selected Rows", command=copy_table_content)
    copy_button.grid(row=6, column=1, columnspan=4, padx=5, pady=5)

    result_frame.columnconfigure(0, weight=1)
    result_frame.columnconfigure(1, weight=1)
    result_frame.columnconfigure(2, weight=1)
    result_frame.columnconfigure(3, weight=1)


    return tab3
