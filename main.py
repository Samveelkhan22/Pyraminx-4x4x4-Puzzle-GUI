from gui import PyraminxGUI
import tkinter as tk

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = PyraminxGUI(root)
        print("GUI initialized successfully.")
        root.mainloop()
    except Exception as e:
        print(f"An error occurred: {e}")
