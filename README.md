# 5. Warcaby

Repozytorium: https://github.com/janKozie1/warcaby

## Opis zadania
 - Okno z siatką przycisków 8x8 oraz przyciskiem do resetowania gry.
 - Przyciski reprezentują pola planszy do gry w warcaby. Pola puste - przyciski bez tekstu. Pola z pionkami gracza 1 - przycisk z tekstem "C". Pola z pionkami gracza 2 - przycisk z tekstem "B". Damki oznaczane są dodatkową literą d ("Cd", "Bd").
 - Nad planszą wyświetlana jest informacja "Tura gracza 1" lub "Tura gracza 2". Gracz wybiera pionka (tekst pola zmienia się z "C" na "[C]") lub z "B" na "[B]"), a potem pole na które chce wykonać ruch. Jeśli ruch jest dozwolony, pionek jest przestawiany, jeśli nie to, wyświetlany jest komunikat "ruch niedozwolony".
 - [Zasady jak w warcabach](https://pl.wikipedia.org/wiki/Warcaby) (dowolny wariant).
 - Gdy gra się kończy, wyświetlane jest okienko z napisem "Wygrał gracz 1" lub "Wygrał gracz 2", zależnie kto wygrał grę. Możliwe jest zresetowanie planszy bez zamykania głównego okna.
 - Program zostanie podzielony na dwie części: 
    1. Część odpowiadającą za logikę gry, walidację ruchów i determinowanie kolejnego stanu gry
    2. Część odpowiadającą za interakcję z użytkownikiem i wyświetlanie interfejsu.
 - Separacja tych części implikuje, że logika gry ma być niezależna od interfejsu
 - Program ma wykorzystać techniki programowania funkcyjnego. Wymagane jest aby przynajmniej pierwsza część programu (logika gry) została napisana w całości funkcyjnie. Druga część programu (interfejs użytkownika) może korzystać z klas/klasy.
 - Wymagane jest aby program używał poniższych technik z programowania funkcyjnego:
    - [Function composition](https://en.wikipedia.org/wiki/Function_composition_(computer_science))
    - [Currying](https://en.wikipedia.org/wiki/Currying) lub/i [partial application](https://en.wikipedia.org/wiki/Partial_application)
    - [Lazy evaluation](https://en.wikipedia.org/wiki/Lazy_evaluation)
    - [Higher order functions](https://en.wikipedia.org/wiki/Higher-order_function)
    - [Functors](https://en.wikipedia.org/wiki/Functor_(functional_programming))
      - Z naciskiem na funktor _Either_ do obsługi błędów / walidacji
 - Dozwolona jest typowa implementacja funktorów dla języków które nie mają ich wbudowanych (zazwyczaj na podstawie prostych klas)

## Testy
 1. Wykonanie po dwa ruchy przez każdego z graczy.
 2. Niepowodzenie błędnego ruchu pionkiem.
 3. Wykonanie bicia pojedynczego pionka.
 4. Wykonanie bicia przynajmniej dwóch pionków.
 5. Zamiana pionka w damkę.
 6. Bicie damką.
 7. Wygrana gracza grającego czarnymi pionkami.
 8. Rozpoczęcie nowej gry po zwycięstwie jednego z graczy. 

Wskazane jest przygotowanie specjalnych początkowych rozstawień pionków dla testów. 