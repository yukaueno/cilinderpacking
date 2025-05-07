# EMPACOTAMOS OS NIVEIS EM FORNOS

# -Definimos um forno
# -Colocamos os resultados nos arquivos (sao os perfis dos fornos)
# -Temos 4 tipos de metodo para empacotar os niveis em fornos
class Forno:
	def __init__(self):
		self.altura = None
		self.L = None
		self.W = None
		self.lista_niveis_colocados = []

def coloca_forno_arquivo(lista_forno,H,arquivo):

	# Colocamos o arquivo na pasta "Resultados"
	f= open("Resultados/" + arquivo + "/result_oven.txt","w+")
	f.write("\\begin{tikzpicture}[scale=0.1]\r\n")

	# Altura do Forno
	aux_Y = 0
	
	for r in lista_forno:

		f.write("	\\begin{scope}[shift={(%f,0.000000)}]\r\n" % aux_Y)
		f.write("		\draw (0,0) rectangle (%f, %f);\r\n" % (r.L,H))

		# Altura do nivel
		aux_y = 0
		
		for a in r.lista_niveis_colocados:
			f.write("			\\begin{scope}[shift={(0.000000,%f)}]\r\n" % aux_y)
			f.write("				\draw (0,0) rectangle (%f, %f);\r\n" % (a.L,a.altura) )
    
			for b in a.lista_circulos_colocados:

				f.write("				\draw[fill=lightgray, opacity=0.3] (%f, 0) rectangle (%f,%f);\r\n" % (b.posicao_x-b.raio, b.raio*2+(b.posicao_x-b.raio), b.altura))

			aux_y = aux_y + a.altura
    
			f.write("			\end{scope}\r\n")

		aux_Y = aux_Y + r.L + 2
		f.write("	\end{scope}\r\n")

	f.write("\end{tikzpicture}\r\n")

	f.close() 

def coloca_forno_arquivo_detalhado(lista_forno,H,arquivo):

	f= open("Resultados/" + arquivo + "/result_oven_d.txt","w+")
  
	for r in lista_forno:
		f.write("\\begin{tikzpicture}[scale=0.1]\r\n")

		# Altura do Forno
		aux_Y = 0

		f.write("	\\begin{scope}[shift={(%f,0.000000)}]\r\n" % aux_Y)
		f.write("		\draw (0,0) rectangle (%f, %f);\r\n" % (r.L,H))

		# Altura do nivel
		aux_y = 0
		i = 1

		for a in r.lista_niveis_colocados:

			if a.lista_circulos_colocados != []:

				f.write("		\\begin{scope}[shift={(0.000000,%f)}]\r\n" % aux_y)
				f.write("			\draw (0,0) rectangle (%f, %f);\r\n" % (a.L,a.altura) )
				f.write("			\\node at (1.5,1.5) {%d};\r\n" %i)
				i = i + 1
				for b in a.lista_circulos_colocados:

					f.write("			\draw[fill=lightgray, opacity=0.3] (%f, 0) rectangle (%f,%f);\r\n" % (b.posicao_x-b.raio, b.raio*2+(b.posicao_x-b.raio), b.altura))

				aux_y = aux_y + a.altura
				f.write("		\end{scope}\r\n")

		aux_Y = aux_Y + r.L + 2
		f.write("	\end{scope}\r\n")
		f.write("\end{tikzpicture}\r\n")

	f.close() 


# Coloca no forno os niveis e gera o arquivo tikz do resultado

# Coloca os níveis e quando fica cheio aloca os outros sem verificar se cabe nos outros recipientes usados
def coloca_forno(lista_nivel,H,L,W,arquivo):

	lista_forno = []  

	forno = Forno()
	forno.altura = H
	forno.L = L
	forno.W = W
	lista_forno.append(forno)

	for nivel in lista_nivel:
		if(nivel.altura <= forno.altura):
			forno.lista_niveis_colocados.append(nivel)
			forno.altura = forno.altura - nivel.altura
		else:
			# E depois comecammos colocando o resto na outra fornada
			forno = Forno()
			forno.altura = H
			forno.L = L
			forno.W = W 
			lista_forno.append(forno)
      
			if(nivel.altura <= forno.altura):
				forno.lista_niveis_colocados.append(nivel)
				forno.altura = forno.altura - nivel.altura
			else:
				print("Algo errado, o nivel eh maior que o forno")

	coloca_forno_arquivo(lista_forno,H,arquivo)
	coloca_forno_arquivo_detalhado(lista_forno,H,arquivo)
	return lista_forno

# First fit
def coloca_forno_f(lista_nivel,H,L,W,arquivo):

	lista_forno = []  

	forno = Forno()
	forno.altura = H
	forno.L = L
	forno.W = W
	lista_forno.append(forno)
	m = 1  # Numero de forno que temos na lista_forno

	for nivel in lista_nivel:
		i = 1
		# Percorre em cada forno ate encontrar em algum que cabe o nivel que queremos colocar, caso nao encontre, colocamos um novo forno na lista
		# Inicializamos o Aloc como False: nao encontramos um forno que podemos colocar o nivel ainda
		Aloc = False
		while i <= m and Aloc == False:
			if(nivel.altura <= lista_forno[i-1].altura):
				Aloc = True
			else:
				i = i + 1
				# E depois comecammos colocando o resto na outra fornada
      
		if Aloc == False:
			m = m + 1
			forno = Forno()
			forno.altura = H
			forno.L = L
			forno.W = W 
			lista_forno.append(forno)
      
			if(nivel.altura <= forno.altura):
				forno.lista_niveis_colocados.append(nivel)
				forno.altura = forno.altura - nivel.altura
			else:
				print("Algo errado, o nivel eh maior que o forno")
    
		else:
			lista_forno[i-1].lista_niveis_colocados.append(nivel)
			lista_forno[i-1].altura = lista_forno[i-1].altura - nivel.altura

	coloca_forno_arquivo(lista_forno,H,arquivo)
	coloca_forno_arquivo_detalhado(lista_forno,H,arquivo)
  
	return lista_forno
	
# Best fit
def coloca_forno_b(lista_nivel,H,L,W,arquivo):

	lista_forno = []  

	forno = Forno()
	forno.altura = H
	forno.L = L
	forno.W = W
	lista_forno.append(forno)
	m = 1  # Numero de forno que temos na lista_forno

	for nivel in lista_nivel:
		i = 1
		# Percorre em cada forno ate encontrar em algum que cabe o nivel que queremos colocar, caso nao encontre, colocamos um novo forno na lista
		# Inicializamos o Aloc como False: nao encontramos um forno que podemos colocar o nivel ainda
		Aloc = False
		while i <= m and Aloc == False:
			if(nivel.altura <= lista_forno[i-1].altura):
				Aloc = True
			else:
				i = i + 1
				# E depois comecammos colocando o resto na outra fornada
      
		if Aloc == False:
			m = m + 1
			forno = Forno()
			forno.altura = H
			forno.L = L
			forno.W = W 
			lista_forno.append(forno)
      
			if(nivel.altura <= forno.altura):
				forno.lista_niveis_colocados.append(nivel)
				forno.altura = forno.altura - nivel.altura
			else:
				print("Algo errado, o nivel eh maior que o forno")
    
		else:
			lista_forno[i-1].lista_niveis_colocados.append(nivel)
			lista_forno[i-1].altura = lista_forno[i-1].altura - nivel.altura
		
		# Ordenando os fornos pelo espaço disponivel de forma crescente
		lista_forno = sorted(lista_forno, key=lambda forno: forno.altura)
		
	coloca_forno_arquivo(lista_forno,H,arquivo)
	coloca_forno_arquivo_detalhado(lista_forno,H,arquivo)
  
	return lista_forno

# Worst fit
def coloca_forno_w(lista_nivel,H,L,W,arquivo):

	lista_forno = []  

	forno = Forno()
	forno.altura = H
	forno.L = L
	forno.W = W
	lista_forno.append(forno)
	m = 1  # Numero de forno que temos na lista_forno

	for nivel in lista_nivel:
		i = 1
		# Percorre em cada forno ate encontrar em algum que cabe o nivel que queremos colocar, caso nao encontre, colocamos um novo forno na lista
		# Inicializamos o Aloc como False: nao encontramos um forno que podemos colocar o nivel ainda
		Aloc = False
		while i <= m and Aloc == False:
			if(nivel.altura <= lista_forno[i-1].altura):
				Aloc = True
			else:
				i = i + 1
				# E depois comecammos colocando o resto na outra fornada
      
		if Aloc == False:
			m = m + 1
			forno = Forno()
			forno.altura = H
			forno.L = L
			forno.W = W 
			lista_forno.append(forno)
      
			if(nivel.altura <= forno.altura):
				forno.lista_niveis_colocados.append(nivel)
				forno.altura = forno.altura - nivel.altura
			else:
				print("Algo errado, o nivel eh maior que o forno")
    
		else:
			lista_forno[i-1].lista_niveis_colocados.append(nivel)
			lista_forno[i-1].altura = lista_forno[i-1].altura - nivel.altura
		
		# Ordenando os fornos pelo espaço disponivel de forma decrescente
		lista_forno = sorted(lista_forno, key=lambda forno: forno.altura, reverse=True)
		
	coloca_forno_arquivo(lista_forno,H,arquivo)
	coloca_forno_arquivo_detalhado(lista_forno,H,arquivo)
  
	return lista_forno
