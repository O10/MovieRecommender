# MovieRecommender

Program podzielony na kilka skryptów tworzących pliki csv z danymi do późniejszej analizy. 
Dzięki temu nie ma potrzeby uruchamiania całego rekomendera za każdym razem

1. create_rating_table.py - tworzy tablicę użytkownicy x oceny 
2. create_movie_table.py - tworzy tablicę filmy x cechy
3. create_sim_table_rating.py - tworzy macierz podobieństw filmów na podstawie ocen
4. create_sim_table_rating.py - tworzy macierz podobieństw filmów na podstawie cech
5. create_matrix_feature.py - tworzy tablicę użytkownicy x cechy wysoko ocenianych filmów
6. create_user_rec - właściwy skrypt rekomendujący bazujący na plikach csv utworzonych przez poprzednie skrypty.
7. start.py - skrypt uruchamia po kolei wszystkie pliki `Użycie:


```
python start.py [nazwa pliku z bazą danych] #zalecane użycie mniejszej np data/test.csv 
```

Pełna baza do pobrania tutaj:
http://nbviewer.jupyter.org/urls/s3-eu-west-1.amazonaws.com/recsysrules2015/RecSysRules2015-Dataset.ipynb

wtedy
```
python start.py recrules-train.csv 
```
i można iść spać i sprawdzić rano :P