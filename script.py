# importere biblioteker
import os
import sqlite3
import time
# med colorama kan jeg legge til farger når jeg printer i konsollen
from colorama import Fore, Style

# oppretter en connection med database
dbConnection = sqlite3.connect("bqdatabase.db")
# lager en "cursor" som brukes for queries
cursor = dbConnection.cursor()

# global variabel for å sette innlogget bruker
loggedInUser = None

# printer en "logo" som alltid skal printes på toppen
def topTextLogo():
    # Style.RESET_ALL må brukes for å sette tekstfargen tilbake til hvit fordi med en gang jeg bruker en annen farge blir den satt som standard når jeg printer
    print(Style.RESET_ALL + "_ _ BURGER QUEEN SYSTEM __\n")

# hjem skjerm, navigasjonsalternativer som login, registrer bruker og avslutt
def homeScreen():
    # os.system("cls") fjerner all teksten i konsollen så det ser ryddig ut
    os.system("cls")
    topTextLogo()
    print("[1] Login\n[2] Registrer bruker\n[3] Avslutt")

    choice = input("\nValg: ")

    match choice:
        case "1":
            loginScreen()
        case "2":
            registerScreen()
        case "3":
            dbConnection.close()
            exit()
        case _:
            homeScreen()

# inloggingsskjerm, bruker skriver inn brukernavn og passord og koden bestemmer om brukeren får logget inn eller ikke
def loginScreen():
    # må bruke global loggedInUser for å si at vi bruker den globale variablen på toppen i stedet for å lage en ny tom variabel
    global loggedInUser
    os.system("cls")
    topTextLogo()
    
    username = input("Skriv inn ditt brukernavn: ")
    password = input("Skriv inn ditt passord: ")

    # query for å hente ut alle brukere med navn/brukernavn som er lik username
    userQuery = cursor.execute("SELECT id, name, password, employee FROM user WHERE name = ?", (username,))
    # henter ut ett resultat, fetchall trengs ikke fordi jeg forventer bare ett eller ingen resultater uansett
    userFound = userQuery.fetchone()

    # viser "Feil brukernavn eller passord!" på begge if statementene fordi det er ikke god praksis å gi spesifikk feedback som "feil passord" eller "feil brukernavn" i innloggingssystemer

    if (userFound == None):
        # Fore.RED gir teksten en rød farge. På alle linjene jeg bruker "Fore" endrer jeg bare tekstfargen til det jeg velger (rød, cyan, osv)
        print(Fore.RED + "Feil brukernavn eller passord!")
        time.sleep(2)
        homeScreen()
        return
    
    if (userFound[2] != password):
        print(Fore.RED + "Feil brukernavn eller passord!")
        time.sleep(2)
        homeScreen()

    loggedInUser = [userFound[0], userFound[1]]

    # 0 betyr false og 1 betyr true. hvis userFound[3] (employee) er False så blir de sendt til brukerskjermen, hvis den er True får de ansattskjermen
    if userFound[3] == 0:
        userScreen()
    else:
        employeeScreen()

# registreringsskjerm, bruker skriver inn brukernavn og passord og koden gir feedback.
def registerScreen():
    global loggedInUser
    os.system("cls")
    topTextLogo()
    
    username = input("Velg ett brukernavn: ")
    password = input("Velg ett passord: ")

    # brukernavn og passord må inneholde minst 3 bokstaver
    if (len(username) < 3 or len(password) < 3):
        print(Fore.YELLOW + "Brukernavnet og passordet ditt må inneholde minst 3 bokstaver!")
        time.sleep(2)
        homeScreen()
        return
    
    userQuery = cursor.execute("SELECT * FROM user WHERE name = ?", (username,))
    userFound = userQuery.fetchone()

    if (userFound != None):
        print(Fore.RED + "Dette brukernavnet er allerede i bruk!")
        time.sleep(2)
        homeScreen()
        return

    # opprete en ny bruker
    cursor.execute("INSERT INTO user (name, password, employee) VALUES(?, ?, ?)", (username, password, 0))
    # lagre endringene, trenger ikke commit funksjon for SELECT queries som ovenfor fordi vi endrer ingen data.
    dbConnection.commit()

    print(Fore.GREEN + "\nBruker registrert!\n")
    input(Style.RESET_ALL + "Trykk enter for å gå tilbake...")

# navigeringsskjerm for innlogget bruker som ikke er ansatt
def userScreen():
    global loggedInUser
    os.system("cls")
    topTextLogo()
    print(Fore.CYAN + f"Velkommen, {loggedInUser[1]}!")
    print(Style.RESET_ALL + "\n[1] Ny bestilling\n[2] Mine bestillinger\n[3] Logg ut")

    choice = input("\nValg: ")

    match choice:
        case "1":
            newOrderScreen()
        case "2":
            myOrdersScreen()
        case "3":
            loggedInUser = None
            homeScreen()
        case _:
            userScreen()

# ny bestillingskjerm der brukeren kan opprette en ny bestilling. bruker velger hvilken burger og antall
def newOrderScreen():
    global loggedInUser
    os.system("cls")
    topTextLogo()

    burgersQuery = cursor.execute("SELECT id, name, ingredients FROM burger")
    burgersFound = burgersQuery.fetchall()
    # looper gjennom alle burgere funnet og lager en ny liste med alle id'ene til burgerne
    burgerIDs = [int(burgerFound[0]) for burgerFound in burgersFound]

    questionText = "Hvilken burger vil du bestille?\n\n"
    
    # burgerFound er en array/liste og de tingene jeg hentet ut i querien er det i listen. 0 = id, name = 1, ingredients = 2
    # så burgerFound[1] er navnet på burgeren for eksempel
    for burgerFound in burgersFound:
        questionText += f"[{burgerFound[0]}] {burgerFound[1]}\n"

    print(questionText)

    choice = input("Valg: ")

    # sjekker om input ikke er numerisk (sjekker om det ikke er en tallverdi)
    if (choice.isnumeric() == False):
        newOrderScreen()
        return
    
    #gjør om input til en int
    choiceInt = int(choice)

    # sjekk om burgeren brukeren valgte eksisterer i burgerIDs som ble laget lengre opp
    if choiceInt in burgerIDs:
        amountChoice = input("Antall: ")

        if (amountChoice.isnumeric() == False or amountChoice[0] == "0"):
            newOrderScreen()
            return
        
        amountChoiceInt = int(amountChoice)

        # opprette ny bestilling
        cursor.execute("INSERT INTO burgerOrder (userID, burgerID, produced, amount) VALUES (?, ?, ?, ?)", (loggedInUser[0], choiceInt, 0, amountChoiceInt))

        # lage en liste over alle ingredienser. siden ingredienser i en burger lagres som "ingrediens, ingrediens, ..." bruker jeg .split(",")
        burgerFoundIngredients = burgersFound[choiceInt-1][2].split(",")

        # loope gjennom alle burger ingrediensene og trekke fra antall ingredienser i databasen
        for burgerFoundIngredient in burgerFoundIngredients:
            cursor.execute("UPDATE ingredient SET amount = amount - ? WHERE name = ?", (1 * amountChoiceInt, burgerFoundIngredient,))

        dbConnection.commit()
        
        print(Fore.GREEN + "\nTakk for din bestilling!")
        print(Style.RESET_ALL + f"\n- {amountChoice}x {burgersFound[choiceInt-1][1]}\n")
        
        input("Trykk enter for å gå tilbake...")
        userScreen()
    else:
        newOrderScreen()

# mine bestillinger skjerm, bruker kan se alle bestillingene sine.
def myOrdersScreen():
    global loggedInUser
    os.system("cls")
    topTextLogo()

    # hente ut bestillinger
    ordersQuery = cursor.execute("SELECT burgerOrder.id, burger.name, burgerOrder.produced, burgerOrder.amount FROM burgerOrder INNER JOIN burger ON burger.id = burgerOrder.burgerID WHERE burgerOrder.userID = ? ORDER BY burgerOrder.id ASC", (loggedInUser[0],))
    ordersFound = ordersQuery.fetchall()

    resultText = "Her er dine bestillinger:\n\n"

    # loope gjennom alle bestillinger og legge på resultat teksten
    for orderFound in ordersFound:
        resultText += f"#{orderFound[0]} {orderFound[3]}x {orderFound[1]} - {"Ikke ferdig" if orderFound[2] == 0 else "Ferdig"}\n"

    # hvis det er totalt 0 bestillinger legger den heller til en "feilmelding" for å vise at det er ingen bestillinger
    if len(ordersFound) == 0:
        resultText += "Du har ingen bestillinger enda.\n"

    print(resultText)

    input("Trykk enter for å gå tilbake...")

    userScreen()

# navigeringsskjerm for innlogget bruker, MEN for ansatte og ikke vanlige brukere
def employeeScreen():
    global loggedInUser
    os.system("cls")
    topTextLogo()
    print(Fore.MAGENTA + f"Velkommen, {loggedInUser[1]}!")
    print(Style.RESET_ALL + "\n__Ansatt Meny__\n\n[1] Alle bestillinger\n[2] Inventar\n[3] Logg ut")

    choice = input("\nValg: ")

    match choice:
        case "1":
            allOrdersScreen()
        case "2":
            inventoryScreen()
        case "3":
            loggedInUser = None
            homeScreen()
        case _:
            employeeScreen()

# alle bestillinger skjerm, ansatt kan se alle bestillinger som ikke er ferdig og enten skrive ordre id'en for å merke den som ferdig eller skriv 0 eller trykk enter for å gå tilbake
def allOrdersScreen():
    global loggedInUser
    os.system("cls")
    topTextLogo()

    ordersQuery = cursor.execute("SELECT burgerOrder.id, burgerOrder.amount, burger.name, user.name FROM burgerOrder INNER JOIN burger ON burgerOrder.burgerID = burger.id INNER JOIN user ON user.id = burgerOrder.userID WHERE burgerOrder.produced = 0")
    ordersFound = ordersQuery.fetchall()
    orderIDs = [int(orderFound[0]) for orderFound in ordersFound]

    resultText = "Alle bestillinger:\n\n"

    for orderFound in ordersFound:
        resultText += f"#{orderFound[0]} {orderFound[1]}x {orderFound[2]} - {orderFound[3]}\n"

    if len(ordersFound) == 0:
        resultText += "! INGEN BESTILLINGER !\n"

    print(resultText)

    choice = input("Skriv inn en bestillings ID for å markere den som ferdig eller skriv 0 eller trykk enter for å gå tilbake: ")

    # hvis input er tomt (100% at bruker har trykket enter) eller input er 0 så gå tilbake
    if (choice == "" or choice == "0"):
        employeeScreen()
        return

    if (choice.isnumeric() == False):
        allOrdersScreen()
        return
    
    choiceInt = int(choice)
    
    # hvis vi finner bestillingen vi valgte (choiceInt) i listen så fortsett
    if choiceInt in orderIDs:
        # oppdatere bestilling
        cursor.execute("UPDATE burgerOrder SET produced = 1 WHERE id = ? AND produced = 0", (choiceInt,))
        # lagre
        dbConnection.commit()

        allOrdersScreen()
    else:
        allOrdersScreen()

# inventar skjerm, ansatt kan se inventaret, altså hvor mye ingredienser de har igjen som brød osv
def inventoryScreen():
    global loggedInUser
    os.system("cls")
    topTextLogo()

    # hente ut ingredienser
    ingredientsQuery = cursor.execute("SELECT name, amount FROM ingredient")
    ingredientsFound = ingredientsQuery.fetchall()

    resultText = "Inventar:\n\n"

    # legge til i resultat teksten
    for ingredientFound in ingredientsFound:
        resultText += f"{ingredientFound[0]} - {ingredientFound[1]} igjen\n"

    print(resultText)

    input("Trykk enter for å gå tilbake...")

    employeeScreen()

# main funksjon som kjører hele tiden med mindre du velger avslutt i hjem skjermen
def main():
    while True:
        homeScreen()

# kjører main funksjon
main()