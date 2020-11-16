# WFB_Django

## Aplikacja do Warhamera/T9A
### Changelog
1. Dodawanie do DB jednostek. <br>
2. Symulowanie walki. <br>
3. Wynikiem jest ilosc zadanych ran. <br>
4. Dodany CSS
5. ModelForm dla edycji i dodawania jednostek
6. Dodane brakujace modele.
7. Dodawanie uzytkownika

## Opis

Aplikacja bedzie dostepna dla zalogowanych i nie zalogowanych uzytkownikow.

Aplikacja bedzie sluzyla do prowadzenia rankingu wewnatrzklubowego, zliczanie punktow z bitew (Warhammer / The Ninth Age),
Druga funkcionalnosc to bedzie kalkulator do symulowania wyniku walki.
Uzytkownicy beda mogli przegladac ranking, dodawac wyniki i kozystac z kalkulatora.
Zalogowani beda mogli dodawac nowe jednostki do bazy w kalkulatorze.

### Widoki:
* main - strona glowna z wyswietlonym menu i 5 najlepszymi graczami w rankingu, mozliwosc dodania nowego uzytkownika <br>
* results - widok z pelnym rankingiem, mozliwosc sortowania i dodania nowego wyniku, szczegoly gracza <br>
* kalkulator - formularz obslugujacy sumulacje walki, podajemy dane wejsciowe i otrzymujemy wynik. <br>
* lista jednostek - lista wszsytkich jednostek utworzynych przez uzytkownikow <br>
* lista graczy - list wszsytkich graczy <br>
* dodawanie nowego gracza - dodaj nowego gracza do rankingu
* edycja gracza - edytuj dane uzytkownika

dla zalogowanych: <br>

* edycja jednsotki - formularz <br>
* dodawanie jednostki - formularz <br>


### Baza Danych:
User - <br>
* login(str), <br>
* password(str) (dane uzytkownika)<br>
* user_armies (relacja W:W przez UserArmies) <br>

UserArmies - <br>
* user - (forein key do User) <br>
* army - (forein key do Armys) <br>

GameResults - <br>
* game_rank(str), 3 mozliwosci choices=("master", "local", "home")
* battle_points(int), <br>
* objective(bool), <br>
* objective_type(foreinkey do Objectives), <br>
* user(foreinkey do User)<br>
* oponenet(str), imie przeciwnika <br>
* date(date), data dodania wyniku <br>

Army - <br>
* name(str), <br>
* description(text) [Definicja frakcji / rasy, jest 12]<br>

Units - <br>
* name(str), <br>
* off, str, ap, reflex (4 charakterystyki potrzebna do kalkulatora(int, int, int, int)), <br>
* army (relacja 1:wielu do modelu Army (kazda Armia moze miec wiele Jednostek)),<br>

Objectives - <br>
* name(int, choices(6 mozliwosci))<br>



