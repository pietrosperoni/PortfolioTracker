import sys
import db
import ui 

def main(db_file=None):
    if db_file is None or db_file == "":
        db_file = ui.ask_for_db_file()  # Function in ui.py to show file dialog
        if db_file is None or db_file == "":
            db_file = ui.ask_for_new_db_name()  # Function in ui.py to get a new DB name
            if db_file is None or db_file == "":
                print("No database file selected or created. Exiting application.")
                return
    db.create_tables(db_file)
    app = ui.PortfolioTrackerApp(db_file)  # Start the GUI application
    app.mainloop()  # This will run the tkinter event loop

    #ui.add_transaction_wizard(db_file)

if __name__ == "__main__":
    db_file_passed = sys.argv[1] if len(sys.argv) > 1 else None
    main(db_file_passed)
