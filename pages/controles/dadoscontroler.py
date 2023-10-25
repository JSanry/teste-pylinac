import services.database as db

def incluir(dados):
	
	db.cursor.execute("""
		INSERT INTO Dados(DadosUnidade, DadosFisico, DadosResultado) 
		VALUES (?, ? ,?)""", (dados.unidade, dados.fisico, dados.resultado))
	db.con.commit()