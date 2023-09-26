import tkinter as tk
from tkinter import ttk
import tkinter as tk
from tkinter import ttk
from tab2 import create_tab2
from tab1 import create_tab1
from tab3 import create_tab3




# Erstelle eine Instanz des Tkinter-Fensters
root = tk.Tk()
root.title("Subdomains")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = int(screen_width * 1.00)
window_height = int(screen_height * 1.00)
root.geometry(f"{window_width}x{window_height}")

# Erstelle eine Registerkarten-Komponente
tab_control = ttk.Notebook(root)

# Erstelle Tabs
#tab1 = ttk.Frame(tab_control)
#tab2 = ttk.Frame(tab_control)

tab1 = create_tab1(tab_control)
tab2 = create_tab2(tab_control)
tab3 = create_tab3(tab_control)

#tab_control.add(tab1, text="Inser Subdomains and Values")
#tab_control.add(tab2, text="Show specific results")

tab_control.pack(expand=1, fill="both")

root.update()

root.mainloop()
