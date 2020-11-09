# WFB_Django

## Aplikacja do Warhamera/T9A
### Changelog
Dodawanie do DB jednostek. <br>
Symulowanie walki. <br>
Wynikiem jes tilosc zadanych ran. <br>

## Opis

Aplikacja bedzie dostepna dla zalogowanych i nie zalogowanych uzytkownikow.

Aplikacja bedzie sluzyla do prowadzenia rankingu wewnatrzklubowego, zliczanie punktow z bitew (Warhammer / The Ninth Age),
Druga funkcionalnosc to bedzie kalkulator do symulowania wyniku walki.
Uzytkownicy beda mogli przegladac ranking i kozystac z kalkulatora.
Zalogowani beda mogli dodawac nowe jednostki do bazy w kalkulatorze.

### Baza Danych:
User - <br>
login(str), <br>
password(str) (dane uzytkownika)<br>

GameResults - <br>
game_rank(str), 3 mozliwosci choices=("master", "local", "home")
battle_points(int), <br>
objective(bool), <br>
objective_type(foreinkey do Objectives), <br>
user(foreinkey do User)<br>
oponenet(str), imie przeciwnika

Army - <br>
name(str), <br>
description(text) [Definicja frakcji / rasy, jest 12]<br>

Units - <br>
name(str), <br>
off, str, ap, reflex (4 charakterystyki potrzebna do kalkulatora(int, int, int, int)), <br>
army (relacja 1:wielu do modelu Army (kazda Armia moze miec wiele Jednostek)),<br>

Objectives - <br>
name(str)



