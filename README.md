<div align="center">

# Python zadaci za pocetnike

**Ovaj repo sadrzi listu zadataka za vezbanje osnova Pythona: petlje, rad sa brojevima i nizovima (liste).**

</div>

---

## Uputstvo za izradu
- ✅ Svaki zadatak resavaj u posebnoj `.py` datoteci.
- ✅ Koristi jasna imena promenljivih i dodaj kratke komentare gde je potrebno.
- ✅ Testiraj program sa nekoliko razlicitih ulaza.

## Kratko uputstvo za koriscenje AI (ChatGPT i Codex)
> **Koristi AI kao pomocnika, ne kao zamenu.**

- 💡 Postavljaj konkretna pitanja (npr. "objasni kako radi Bubble Sort" ili "proveri moj kod").
- 💡 Zadrzi svoje resenje i pokusaj da razumes svaki red koda koji dobijes.
- 💡 Ako AI predlozi kompletno resenje, prvo pokusaj sam, pa uporedi i pitaj gde gresis.

## Kako da koristis Codex u Visual Studio Code
- 🧩 Instaliraj dodatak "OpenAI Codex" iz Extensions (Ctrl+Shift+X).
- 🔐 Prijavi se ili unesi API kljuc u podesavanjima dodatka.
- 📝 Otvori `.py` fajl i napisi kratak opis zadatka u komentaru ili u poruci Codex-u.
- 🧭 Koristi komande kao: "objasni mi ovaj kod", "nadji gresku", "predlozi poboljsanje".
- 🔍 Procitaj predlog, izmeni po potrebi, pa pokreni kod da vidis rezultat.
- ❓ Ako nesto nije jasno, trazi objasnjenje korak-po-korak.

---

## 🧩 Zadaci (TODO)

### Task 1: Suma cifara visecifrenog broja
- [ ] Uneti visecifreni broj
- [ ] Izracunati zbir njegovih cifara
- [ ] Koristiti `%` i `//` u petlji

**Uputstvo za resavanje:**
1. Koristiti `input()` za unos broja i konvertovati ga u `int`
2. Inicijalizovati sumu na 0
3. Koristiti `while` petlju dok je broj > 0:
   - Uzeti poslednju cifru pomocu `broj % 10`
   - Dodati cifru na sumu
   - Ukloniti poslednju cifru pomocu `broj // 10`
4. Prikazati konacnu sumu

---

### Task 2: Sume brojeva (3 podzadatka)
- [ ] Izracunati zbir brojeva od 1 do 10
- [ ] Izracunati zbir prvih 10 parnih brojeva
- [ ] Izracunati zbir prvih 10 neparnih brojeva

**Uputstvo za resavanje:**
1. Podzadatak 1: Koristiti `for` petlju od 1 do 10 i sabirati brojeve
2. Podzadatak 2: Koristiti `for` petlju i sabirati samo parne brojeve (2, 4, 6, ..., 20)
3. Podzadatak 3: Koristiti `for` petlju i sabirati samo neparne brojeve (1, 3, 5, ..., 19)
4. Prikazati sve tri sume

---

### Task 3: Sortiranje elemenata niza - rastuce
- [ ] Uneti 10 celih brojeva u listu
- [ ] Implementirati Bubble Sort (bez ugradjenih funkcija)
- [ ] Prikazati listu pre i posle sortiranja

**Uputstvo za resavanje:**
1. Napraviti praznu listu
2. Koristiti `for` petlju za unos 10 brojeva u listu
3. Sacuvati originalnu listu za prikaz (napraviti kopiju)
4. Implementirati Bubble Sort:
   - Spoljna `for` petlja: od 0 do len(lista)-1
   - Unutrasnja `for` petlja: od 0 do len(lista)-1-i
   - Ako je `lista[j] > lista[j+1]`, zameniti ih
5. Prikazati originalnu i sortiranu listu

---

### Task 4: Sortiranje elemenata niza - opadajuce
- [ ] Uneti 10 celih brojeva u listu
- [ ] Implementirati Bubble Sort (bez ugradjenih funkcija)
- [ ] Sortirati listu opadajuce i prikazati rezultat

**Uputstvo za resavanje:**
1. Isti postupak kao Task 3
2. Promeniti uslov u Bubble Sort algoritmu:
   - Ako je `lista[j] < lista[j+1]`, zameniti ih (obrnuto od rastuceg)
3. Prikazati originalnu i sortiranu listu (opadajuce)

---

### Task 5: Aritmeticka sredina niza
- [ ] Uneti brojeve u listu
- [ ] Izracunati zbir elemenata
- [ ] Podeliti zbir sa `len(lista)`

**Uputstvo za resavanje:**
1. Napraviti listu brojeva (uneti nekoliko brojeva)
2. Inicijalizovati sumu na 0
3. Koristiti `for` petlju za sabiranje svih elemenata
4. Izracunati sredinu: `suma / len(lista)`
5. Prikazati aritmeticku sredinu

---

### Task 6: Proizvod elemenata niza
- [ ] Inicijalizovati proizvod na 1
- [ ] U petlji mnoziti svaki element liste
- [ ] Prikazati konacan proizvod

**Uputstvo za resavanje:**
1. Napraviti listu brojeva
2. Inicijalizovati proizvod na 1 (ne 0!)
3. Koristiti `for` petlju i mnoziti svaki element sa proizvodom
4. Prikazati konacni proizvod svih elemenata

---

## Napomene
- 📌 Ako pokrenes Visual Studio Code tamo gde si vec radio, sve ce biti podeseno.
- 📂 Ako nesto nije u redu, u Visual Studio Code otvori folder `D:\Djole\Python\HelloWorld`.
- 🧭 Da vidis Codex u Visual Studio Code, klikni na ikonicu "OpenAI Codex" u levoj traci (Activity Bar).
