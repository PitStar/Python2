'''

Сахно Данило
Високорівневе програмування
Лабораторна робота №2

'''

import csv # Імпортруємо модуль, який має методи для формування списку з рядків файлу


# Клас для роботи з файлом
class Netflix:
   def __init__(self, path): # Конструктор класу
      self.path = path
   def readFile(self): # Функція зчитування файлу
      self.mainList = []
      try:
         with open(self.path, mode = 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
               self.mainList.append(row)
      except (BaseException): # Якщо помилка зчитування, то повідомаляємо про це і зупиняємо роботу скрипта
         raise BaseException('The file ' + self.path + ' was not found')
      self.mainList.pop(0) # Видаляємо перший рядок з назвами стовпчиків
      return
   def getMovies(self, rating): # Тільки серіали та фільми з рейтингом більшим ніж визачений в якості параметра функції
      result = []
      result = [row for row in self.mainList if len(row[13]) > 0] # Треба відібрати ті рядки, де рейтниг вказано
      result = [row[:5] for row in result if (float(row[13]) > rating) and ((row[8] == 'tvSeries') or (row[8] == 'movie'))] # Кінцева обробка з поверненням перших 5 стовпчиків
      return result
   def getMoviesLazy(self): # Генераторна функція
      result = [row for row in self.mainList if ((((row[8] == 'movie') or (row[8]) == 'tvShow') and (row[10] == 'English')) or ((row[8] == 'movie') or (row[8] == 'tvSeries') and (  int(row[5] if len(row[5]) > 0 else 0 ) > 2015 )))]
      for row in result:
         yield row
   def getStatistics1(self):# Функція, яка повертає середній рейтниг та тільки фільми для дорослих
      adults = len([row for row in self.mainList if row[16] == '1'])
      votes = [float(row[13] if len(row[13])> 0 else 0) for row in self.mainList if float(row[14] if len(row[14]) > 0 else 0) > 1000]
      sum_votes = 0
      for vote in votes:
         sum_votes += vote
      avg = sum_votes / len(votes)
      return adults, avg
   def getStatistics2(self):# Генераторна функція, яка повертнає назви фільмів, рейтинг яких вище середнього і які мають більше 10 епізодів
      rates = [row[13] for row in self.mainList if len(row[13]) > 0]
      sum_rates = 0
      for rate in rates:
         sum_rates += float(rate)
      avg = sum_rates / len(rates)

      titles_ = [row for row in self.mainList if (((len(row[1]) > 0) and (row[8] == 'tvSeries') and ((int(row[6]) if len(row[6]) > 0 else 0) > 10)) and (len(row[13]) > 0))]
      titles = [row[1] for row in titles_ if float(row[13]) > avg]
      for row in titles:
         yield row


# Клас - обгортка, який реалізує ітераційну поведінку
class Cast:
   def __init__(self, dataset): # Конструктор класу, в який ми передаємо список даних
      self.dataset = dataset
      self.size = len(dataset) # Відразу порахуємо розмір списку
   def __iter__(self): # Ініціалізація ітератора
      self.i = 0
      return self
   def __next__(self): # Метод, який відповідає за покрокове повернення рядків
      if self.i == self.size: # Якщо кількість кроків дорівнює розміру, то зупиняємо 
         raise StopIteration
      while self.i < self.size: # Цей цикл потрібно щоб оминати ті рядки, які не відповідають нашим умовам
         row = self.dataset[self.i]
         self.i += 1
         if (len(row[17]) > 50): # Умова виконується і тому повертаємо рядок і виходимо з методу
            return row[17]
         else:
            if (self.i == self.size -1): # На випадок, якщо останній рядок також не відповідає нашим умовам
               raise StopIteration




netflix = Netflix('./netflix_list.csv')
netflix.readFile()
cast = Cast(netflix.mainList)
castlist = iter(cast)
movies = [row for row in castlist]
for movie in movies[:10]: # Повертаємо перші 10 рядків
   print(movie)
rates = netflix.getStatistics2()
print(next(rates))
