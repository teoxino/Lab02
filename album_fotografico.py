def carica_da_file(file_path):
    album = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            prima_riga = True
            for riga in f:
                riga = riga.strip()
                if not riga:
                    continue
                # skip prima riga
                if prima_riga:
                    prima_riga = False
                    continue

                dati = [campo.strip() for campo in riga.split(",")]
                codice = dati[0]
                titolo = dati[1]
                autore = dati[2]
                mese = int(dati[3])
                anno = int(dati[4])

                foto = {
                    "codice": codice,
                    "titolo": titolo,
                    "autore": autore,
                    "mese": mese,
                    "anno": anno,
                }

                # l anno esiste gia?
                anno_trovato = False
                for gruppo in album:
                    if gruppo[0] == anno:
                        gruppo[1].append(foto)
                        anno_trovato = True
                        break

                if not anno_trovato:
                    album.append([anno, [foto]])
        return album

    except FileNotFoundError:
        return None


def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    if not (1 <= mese <= 12):
        return None

    # Controllo che non debba esistere gia l albumm
    for gruppo in album:
        for foto in gruppo[1]:
            if foto["codice"] == codice:
                return None

    try:
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(f"\n{codice},{titolo},{autore},{mese},{anno}")
    except (FileNotFoundError, OSError):
        return None

    nuova_foto = {
        "codice": codice,
        "titolo": titolo,
        "autore": autore,
        "mese": mese,
        "anno": anno,
    }

    anno_trovato = False
    for gruppo in album:
        if gruppo[0] == anno:
            gruppo[1].append(nuova_foto)
            anno_trovato = True
            break

    #   creaiamo anno senon c'è
    if not anno_trovato:
        album.append([anno, [nuova_foto]])

    return nuova_foto


def cerca_foto(album , codice):

    for gruppo in album:
        for foto in gruppo[1]:
            if foto["codice"] == codice:
                return f"{foto['codice']}, {foto['titolo']}, {foto['autore']}, {foto['mese']}, {foto['anno']}"
    return None


def elenco_foto_anno_per_titolo(album, anno):

    for gruppo in album:
        if gruppo[0] == anno:
            titoli = [foto["titolo"] for foto in gruppo[1]]
            titoli.sort()
            return titoli
    return None


def main():
    album = []
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
