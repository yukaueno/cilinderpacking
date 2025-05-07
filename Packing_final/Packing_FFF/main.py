# Empacotamento de cilindros que considera a FAIXA

import packingcircle
import packingretangule
import ast
import sys
import time
from itertools import accumulate, chain, repeat, tee

# Le os dados
def le_dados():

	with open("Instancias/" + sys.argv[1], "rt") as fin:
		with open("arquivo_novo.txt", "wt") as fout:
			for line in fin:
				fout.write(line.replace(';', ','))

	lista = []

	f= open("arquivo_novo.txt","r")

	data = f.readlines()
 
	for line in data:
		lista.append(line.rstrip('\n'))

	f.close()
	return lista

# Retirado de http://wordaligned.org/articles/slicing-a-list-evenly-with-python
def chunk(xs, n):
    assert n > 0
    L = len(xs)
    s, r = divmod(L, n)
    widths = chain(repeat(s+1, r), repeat(s, n-r))
    offsets = accumulate(chain((0,), widths))
    b, e = tee(offsets)
    next(e)
    return [xs[s] for s in map(slice, b, e)]

if __name__ == '__main__':

	# Contando tempo de execucao
	start_time = time.time()

	# Pegando os dados do arquivo
	lista = le_dados()

	# Tamanho do Nivel
	L = ast.literal_eval(lista[1])
	W = ast.literal_eval(lista[2])
	H = ast.literal_eval(lista[3])
	
	num_forno = None
	num_nivel = None
	
	lista_raio = ast.literal_eval(lista[4])
	lista_altura_circulos = ast.literal_eval(lista[5])

 
	# Ordenando a lista pela altura decrescente
	lista_cilindro = sorted(zip(lista_raio, lista_altura_circulos), key=lambda cilindro: [cilindro[1],cilindro[0]], reverse=True)

	f = open("Solucoes/" + sys.argv[1][:-4]+".txt", "a")
	f.write("x,f,n\n")
	
	maximo = max(lista_altura_circulos)
	minimo = min(lista_altura_circulos)

	n = maximo - minimo

	#p = [0.0001,0.0005,0.001]
	#p = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
	#p = [0.1,0.125,0.15,0.175,0.2,0.225,0.25,0.275,0.3,0.325,0.35,0.375,0.4,0.425,0.45,0.475,0.5,0.525,0.55,0.575,0.6,0.625,0.65,0.675,0.7,0.725,0.75,0.775,0.8,0.825,0.85,0.875,0.9,0.925,0.95,0.975,1]
	#p = [0.001,0.002,0.003,0.004,0.005,0.006,0.007,0.008,0.009,0.01,0.011,0.012,0.013,0.014,0.015,0.016,0.017,0.018,0.019,0.02]
	p = [0.01,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1]
	
	lista_ordenacao = []
	
	for perc in p:
		x = n * perc
		
		lista_aux_total = []
		
		faixa = x

		lista_cilindro_aux = sorted(
			zip(lista_raio, lista_altura_circulos),
			key=lambda cilindro: [cilindro[1], cilindro[0]], reverse=True)

		max_v = maximo
		while len(lista_cilindro_aux) != 0:
			
			lista_aux = []
			for item in lista_cilindro_aux:
				if item[1] >= max_v - faixa:
					lista_aux.append(item)
					
			for item in lista_aux:
				lista_cilindro_aux.remove(item)

			faixa = faixa + x

			# Ordenando por raio a faixa de cilindros escolhido
			lista_aux = sorted(lista_aux,key=lambda cilindro: cilindro[0],reverse=True)
			lista_aux_total.append(lista_aux)
		
		lista_aux_total = [x for x in lista_aux_total if x != []]
		
		existe = False
		
		for lista in lista_ordenacao:
			if lista == lista_aux_total:
				existe = True
			
		if existe == False:
			lista_ordenacao.append(lista_aux_total)
			lista_aux_total = [col for row in lista_aux_total for col in row]
			
			lista_nivel = packingcircle.empacota_circulos_m(L,W,lista_aux_total, sys.argv[1][:-4])
			# Vamos calcular o numero de fornadas necessarias
			lista_forno = packingretangule.coloca_forno_f(lista_nivel, H, L, W,sys.argv[1][:-4])
			
			if  num_nivel == None or num_nivel > len(lista_nivel):
				num_nivel = len(lista_nivel)
      
			if  num_forno == None or num_forno > len(lista_forno):
				num_forno = len(lista_forno)
				num_nivel1 = num_nivel
				aux = perc	

			f.write("%f,%d\n" % (perc,len(lista_forno)) )
				
	f.close()
	
	f = open("time.txt", "a")
	f.write("%s   &      %d &       %f\n" %(sys.argv[1][:-4],num_forno,time.time()-start_time))
	f.close()
	
	print(sys.argv[1],"forno", num_forno," com ", num_nivel1, " niveis", "dividimos em" , aux, " e o tempo de execucao eh ",(time.time() - start_time),"\n")

	# Empacotamos os cilindros da ordem obtida por aux
	x = n * aux
		
	lista_aux_total = []
		
	faixa = x

	lista_cilindro_aux = sorted(zip(lista_raio, lista_altura_circulos),key=lambda cilindro: [cilindro[1], cilindro[0]], reverse=True)

	max_v = maximo

	while len(lista_cilindro_aux) != 0:
			
		lista_aux = []
		for item in lista_cilindro_aux:
			if item[1] >= max_v - faixa:
				lista_aux.append(item)
					
		for item in lista_aux:
			lista_cilindro_aux.remove(item)

		faixa = faixa + x

		# Ordenando por raio a faixa de cilindros escolhido
		lista_aux = sorted(lista_aux,key=lambda cilindro: cilindro[0],reverse=True)
		lista_aux_total.append(lista_aux)
		
	lista_aux_total = [x for x in lista_aux_total if x != []]
	
	lista_aux_total = [col for row in lista_aux_total for col in row]
			
	lista_nivel = packingcircle.empacota_circulos_m(L,W,lista_aux_total, sys.argv[1][:-4])
	# Vamos calcular o numero de fornadas necessarias
	lista_forno = packingretangule.coloca_forno_f(lista_nivel, H, L, W,sys.argv[1][:-4])
	
