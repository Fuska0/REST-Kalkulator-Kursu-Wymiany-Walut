## Kalkulator Kursu Wymiany Walut

### Opis
Celem tego zadania jest stworzenie prostego serwisu webowego realizującego funkcjonalność kalkulatora kursu wymiany walut. Serwis ten opiera się na wykorzystaniu otwartych serwisów udostępniających REST API. 

### Funkcje Serwisu
1. Udostępnienie klientowi statycznej strony HTML z formularzem do zebrania parametrów żądania.
2. Odebranie zapytania od klienta.
3. Odpytanie publicznych serwisów (różne endpointy) o dane potrzebne do skonstruowania odpowiedzi.
4. Obróbka otrzymanych odpowiedzi, na przykład wyciągnięcie średniej, znalezienie ekstremów, porównanie wartości z różnych serwisów, itp.
5. Wygenerowanie i wysłanie odpowiedzi do klienta w postaci statycznej strony HTML z wynikami.

### Wybrana Funkcjonalność
Serwis umożliwia klientowi obliczenie kursu wymiany walut. Klient podaje dwie waluty oraz kwotę, a serwis zwraca statyczną stronę z wynikami. 

### Implementacja
Serwis został zaimplementowany przy użyciu biblioteki FastAPI w języku Python.
- Wykorzystuje kilka zapytań do publicznych serwisów:
    - Kursy walut z Exchange Rate API.
    - Kursy walut z CoinAPI.
- Wylicza statystyki dla otrzymanych kursów, takie jak minimalny, maksymalny i średni kurs wymiany.
- Przelicza kwotę na podstawie średniego kursu wymiany.

### Uruchomienie
1. Uruchomienie serwisu wymaga instalacji FastAPI oraz uvicorn:
    ```bash
    pip install fastapi uvicorn
    ```
2. Skopiuj kod serwisu do pliku Python.
3. Uruchomienie serwisu:
    ```bash
    uvicorn nazwa_pliku:app --reload
    ```
4. Serwis będzie dostępny pod adresem `http://localhost:8000/`.

### Endpointy API
1. `GET /calculate-exchange-rate` - Oblicza kurs wymiany walut z Exchange Rate API.
2. `GET /calculate-coin-api-rate` - Oblicza kurs wymiany walut z CoinAPI.
3. `POST /calculate-all-rates` - Oblicza wszystkie kursy wymiany na podstawie formularza.

### Formularz
Klient może wypełnić formularz podając:
- Walutę źródłową.
- Walutę docelową.
- Kwotę do przeliczenia.

### Odpowiedź Serwisu
Serwis generuje stronę HTML z wynikami, zawierającą:
- Kursy w poszczególnych serwisach.
- Minimalny, maksymalny i średni kurs wymiany.
- Przeliczoną kwotę na podstawie średniego kursu.

### Błędy
W przypadku błędów, serwis zwraca odpowiedni komunikat na stronie HTML, informując użytkownika o problemie.

### Uwagi
- Projekt realizuje funkcję kalkulatora kursu wymiany walut, wykorzystując publiczne API.
- Implementuje prosty interfejs w formie formularza HTML.
- Serwis jest uruchomiony na własnym serwerze aplikacyjnym zgodnie z wymaganiami.
