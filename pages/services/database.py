#import pyodbc

#server = 'seuservidor' 
#database = 'seubancodedados' 
#username = 'usuario' 
#password = 'senha' 
#cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
#cursor = cnxn.cursor()

import sqlite3



with sqlite3.connect('crud_python.db', check_same_thread=False) as con:
	cursor = con.cursor()
	cursor.execute(
		"""
		CREATE TABLE IF NOT EXISTS Dados
		(
			id integer primary key autoincrement,
			DadosUnidade text not null,
			DadosFisico integer not null,
			DadosResultado text
		)
		""") 