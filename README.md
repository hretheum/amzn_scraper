# projekt zaliczeniowy

minimalna wersja python: 3.11
autor: eryk orłowski eof@offline.pl

## co robi apka

Celem apki jest cykliczne pobieranie ofert z serwisu amazon.pl (web scrapping) i zapisywanie ich do baz danych.
Zapisane oferty mogą być przeglądane i modyfikowane przez interfejs www,
za pomocą którego mozliwe jest takze dodawanie nowych kryteriów przeszukiwania amazon.pl.

Aplikacja składa się z dwóch części i wspólnej bazy danych:

1. scraper w katalogu /amzn
2. aplikacja www

Obie aplikacje mogą być uruchamiane lokalnie bądź na odpowiednim serwerze www.
Scraper moze być uruchamiany cyklicznie w sposób zautomatyzowany.

## Konfiguracja podstawowa

Skonfiguruj wartości w pliku .env bąd∂ź odpowiednim środowisku serwera:

- MYSQL_URL=adres hosta
- MYSQL_USER=username
- MYSQL_PASSWD=hasło
- MYSQL_DATABASE=nazwa ISTNIEJĄCEJ bazy danych
- SCRAPER_API_KEY=klucz do api scraper
- SECRET_KEY=twój secret key

## Jak uruchomić lokalnie

uruchom po kolei w terminalu:

python /www/project/models.py
powysze tworzy odpowiednią strukturę w bazie danych

python /www/project/app-init.py
dodaje usera aplikacji

uruchomienie aplikacji Flask:
w katalogu /www uruchom polecenie flask --app project run

Po zalogowaniu do www dodaj kwerendę dla serwisu amazon.pl

Aby ręcznie uruchomić scraper, w terminalu w katalogu /amzn uruchom:
scrapy crawl amazon

Po pomyślnym wykonaniu scrappingu uzyskujesz dostęp do wyników w interfejsie www.
