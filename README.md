# Data-Assignment
This Python project uses Pandas to process and merge data from three CSV files (Facebook, Google, and Website) about companies. The program combines information from these files, improving the visibility and accuracy of data for company names, categories, addresses, and phone numbers.

# Raspunsuri la intrebari:

## Ce coloană am folosit pentru a face join-ul?

Am ales din cele trei CSV-uri coloana care conținea numele firmei. Am uniformizat această coloană prin normalizarea și convertirea numelor la același format în toate CSV-urile, apoi am folosit-o ca punct de referință pentru a face join-ul între seturile de date.

## Cum am rezolvat conflictele de date după join?

Am întâlnit conflicte în numerele de telefon și am decis să păstrez numărul care apare de cele mai multe ori în seturile de date. În ceea ce privește adresele, am prioritizat CSV-ul care conținea datele de la Google, deoarece mi s-a părut cel mai bine structurat. Dacă adresa din Google lipsea, am ales adresa din CSV-ul cu datele de la Facebook, iar în cazul în care nici aici nu erau informații, am construit o adresă din coloanele disponibile în datele provenite din website.

Un alt conflict a apărut la coloana cu categoriile. În acest caz, am combinat toate categoriile disponibile, unind categoriile similare și separându-le pe cele diferite prin caracterul |, creând astfel un set complet de categorii pentru fiecare firmă.

## Cum am tratat datele foarte similare?

Date similare au apărut în coloana company_name. Am unit firmele care aveau același număr de telefon, iar în cazurile în care numele firmei diferă ușor, am păstrat numele cel mai lung, care conținea fie numele complet al firmei, fie elemente comune din toate celelalte nume sau fragmente de nume. Astfel, am redus duplicările și am creat un set unitar de date pentru fiecare companie.


## Importuri și Biblioteci:

import pandas as pd: Importă biblioteca Pandas pentru manipularea și analiza datelor în DataFrame-uri.
import re: Importă biblioteca re pentru manipularea expresiilor regulate, utilizată pentru curățarea și normalizarea textului.
from collections import Counter: Importă Counter din collections pentru numărarea frecvenței elementelor într-o listă.

### 1. load_and_rename_csv:
  Încarcă un fișier CSV și redenumește coloanele conform unui dicționar de mapare specificat. Acest lucru ajută la uniformizarea denumirilor coloanelor între diferite surse de date.

### 2. normalize_company_name:
  Normalizează numele companiilor dintr-un DataFrame, aplicând titluri, eliminând caracterele speciale și sufixele comune, pentru a obține un format uniform.

### 3. get_most_complex_name:
  Selectează cel mai complex nume de companie dintr-o listă, bazându-se pe numărul de cuvinte, pentru a asigura o denumire completă și descriptivă.

### 4. combine_categories:
  Combină categoriile dintr-un șir de text, eliminând duplicările și separând valorile unice cu ' | '. Acest lucru ajută la consolidarea categoriilor multiple într-un format uniform.

### 5. normalize_phone_number:
  Normalizează numerele de telefon, eliminând caracterele non-digitale pentru a obține un format uniform de număr de telefon.

### 6. is_valid_phone_number:
  Verifică validitatea unui număr de telefon folosind o expresie regulată, asigurându-se că respectă formatul așteptat.

### 7. prioritize_phone_numbers:
  Prioritizează numerele de telefon dintr-o listă, alegându-l pe cel mai frecvent întâlnit, pentru a rezolva conflictele între mai multe numere de telefon.

### 8. normalize_address:
  Normalizează adresele prin convertirea la minuscule, eliminarea caracterelor nepermise și uniformizarea separatoarelor, pentru a asigura un format consistent.

### 9. combine_and_prioritize_address:
  Combină adresele din surse multiple (Google, Facebook, Website) și prioritizesază componentele adreselor, înlocuind valorile lipsă cu mesaje standardizate și returnând o adresă completă și uniformă.
  
### 10. combine_conflicting_values:
Combină valorile conflictuale într-o coloană, folosind un separator specificat pentru a aduna valorile unice și a rezolva conflictele între diferite surse de date.

### 11. combine_records:
Combină înregistrările dintr-un grup de date pe baza numelui companiei, combinând categoriile, adresele și numerele de telefon, și returnează un rezultat consolidat.

### 12. main:
Coordonează întregul flux de lucru al proiectului: încarcă datele din fișiere CSV, normalizează și curăță datele, combină sursele de date, validează și normalizează valorile, și salvează rezultatul final într-un nou fișier CSV.
