import sqlite3

import sqlite3

# 读取文件内容到列表
stephen_king_adaptations_list = []
with open('stephen_king_adaptations.txt', 'r') as file:
    stephen_king_adaptations_list = file.readlines()

# 建立SQLite数据库连接
conn = sqlite3.connect('stephen_king_adaptations.db')
cursor = conn.cursor()

# 创建表
cursor.execute('''CREATE TABLE IF NOT EXISTS stephen_king_adaptations_table
                  (movieID INTEGER PRIMARY KEY,
                   movieName TEXT,
                   movieYear INTEGER,
                   imdbRating REAL)''')

# 插入数据
for movie in stephen_king_adaptations_list:
    movie_details = movie.split(',')
    cursor.execute('''INSERT INTO stephen_king_adaptations_table 
                      (movieName, movieYear, imdbRating) 
                      VALUES (?, ?, ?)''', (movie_details[0], movie_details[1], movie_details[2]))

conn.commit()

# 用户交互
while True:
    print("Options:")
    print("1. Search by movie name")
    print("2. Search by movie year")
    print("3. Search by movie rating")
    print("4. STOP")

    option = input("Enter an option: ")

    if option == "1":
        movie_name = input("Enter the movie name: ")
        cursor.execute('''SELECT * FROM stephen_king_adaptations_table 
                          WHERE movieName LIKE ?''', (f'%{movie_name}%',))
        result = cursor.fetchall()
        if result:
            for movie in result:
                print("Movie ID:", movie[0])
                print("Movie Name:", movie[1])
                print("Movie Year:", movie[2])
                print("IMDB Rating:", movie[3])
        else:
            print("No such movie exists in our database")

    elif option == "2":
        movie_year = input("Enter the movie year: ")
        cursor.execute('''SELECT * FROM stephen_king_adaptations_table 
                          WHERE movieYear = ?''', (movie_year,))
        result = cursor.fetchall()
        if result:
            for movie in result:
                print("Movie ID:", movie[0])
                print("Movie Name:", movie[1])
                print("Movie Year:", movie[2])
                print("IMDB Rating:", movie[3])
        else:
            print("No movies were found for that year in our database")

    elif option == "3":
        movie_rating = float(input("Enter the minimum movie rating: "))
        cursor.execute('''SELECT * FROM stephen_king_adaptations_table 
                          WHERE imdbRating >= ?''', (movie_rating,))
        result = cursor.fetchall()
        if result:
            for movie in result:
                print("Movie ID:", movie[0])
                print("Movie Name:", movie[1])
                print("Movie Year:", movie[2])
                print("IMDB Rating:", movie[3])
        else:
            print("No movies at or above that rating were found in the database")

    elif option == "4":
        break

# 关闭数据库连接
conn.close()
