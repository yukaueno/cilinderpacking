# Empacotamento de cilindros que considera a QUANTIDADE

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
  
	# Colocando os raios e alturas numa lista separada
	lista_raio = ast.literal_eval(lista[4])
	lista_altura_circulos = ast.literal_eval(lista[5])

	# Ordenando a lista pela altura decrescente
	lista_cilindro = sorted(zip(lista_raio, lista_altura_circulos), key=lambda cilindro: [cilindro[1],cilindro[0]], reverse=True)
	#lista_cilindro = lista_cilindro[0:6]
	# Auxiliar para indicar qual divisão usou menos recipientes
	num_forno = None
	num_nivel = None
	aux = 1

	f = open("Solucoes/"+sys.argv[1][:-4]+".txt", "a")
	f.write("x,f,n\n")
	
	tam = len(lista_cilindro)
	
	lista_ordenacao = []
	
	# Calculando 10% de 7 a 12
	#tam = int(len(lista_cilindro)*0.025)
	#tam = [len(lista_cilindro)]
	if tam < 102:
		div = range(tam)
	
	if tam == 102:
		#div = [1,3,6,12,25,51,102]
		div = [1,2,3,6,12,25,51,102]
	if tam == 204:
		#div = [1,3,6,12,25,51,102,204]
		div = [1,2,3,6,12,25,51,102,204]
	if tam == 300:
		#div = [1,2,4,9,18,75,150,300]
		div = [1,2,4,9,18,75,150,300]
	if tam == 402:
		#div = [1,2,3,6,12,25,50,100,201,402]
		div = [1,2,3,6,12,25,50,100,201,402]
	if tam == 504:
		#div = [1,3,7,15,31,63,126,252,504]
		div = [1,2,3,7,15,31,63,126,252,504]
	if tam == 1002:
		#div = [1,3,7,15,31,62,125,250,501,1002]
		div = [1,2,3,7,15,31,62,125,250,501,1002]
	if tam == 2004:
		#div = [1,3,7,15,31,62,125,250,501,1002,2004]
		div = [1,2,3,7,15,31,62,125,250,501,1002,2004]
	if tam == 10002:
		#div = [1,2,4,9,19,39,78,156,312,625,1250,2500,5001,10002]
		div = [1,2,4,9,19,39,78,156,312,625,1250,2500,5001,10002]
	if tam == 20004:
		#div = [1,2,4,9,19,39,78,156,312,625,1250,2500,5001,10002,20004]
		div = [1,2,4,9,19,39,78,156,312,625,1250,2500,5001,10002,20004]
		
	for i in div:
		
		lista_n = chunk(lista_cilindro, i+1)
		lista_aux = []
    
		for pedaco in lista_n:
			pedaco = sorted(pedaco,key=lambda cilindro: cilindro[0],reverse=True)
			lista_aux.append(pedaco)
			
		lista_aux = [x for x in lista_aux if x != []]
		
		existe = False
		
		for lista in lista_ordenacao:
			if lista == lista_aux:
				existe = True
			
		if existe == False:
			lista_ordenacao.append(lista_aux)
			lista_aux = [col for row in lista_aux for col in row]
			
			lista_nivel = packingcircle.empacota_circulos_m(L,W,lista_aux, sys.argv[1][:-4])
			# Vamos calcular o numero de fornadas necessarias
			lista_forno = packingretangule.coloca_forno_b(lista_nivel, H, L, W,sys.argv[1][:-4])	
		

		#if  num_nivel == None or num_nivel > len(lista_nivel):
		#	num_nivel = len(lista_nivel)
      
		if  num_forno == None or num_forno > len(lista_forno):
			num_forno = len(lista_forno)
			num_nivel1 = len(lista_nivel)
			aux = i+1

		f.write("%d,%d,%d\n" % (i+1,len(lista_forno), len(lista_nivel)) )
    
	f.close()
	
	f = open("time.txt", "a")
	f.write("%s   &      %d &       %f\n" %(sys.argv[1][:-4],num_forno,time.time()-start_time))
	f.close()
	
	print(sys.argv[1],"forno", num_forno," com ", num_nivel1, " niveis", "dividimos em" , aux, " e o tempo de execucao eh ",(time.time() - start_time),"\n")
  
	# Empacotamos com o aux que usou menos recipientes 
	lista_n = chunk(lista_cilindro, aux)
	lista_aux = []

	for pedaco in lista_n:
		pedaco = sorted(pedaco,key=lambda cilindro: cilindro[0],reverse=True)
		lista_aux.append(pedaco)

	lista_aux = [col for row in lista_aux for col in row]
	lista_nivel = packingcircle.empacota_circulos_m(L,W,lista_aux, sys.argv[1][:-4])
	# Vamos calcular o numero de fornadas necessarias
	lista_forno = packingretangule.coloca_forno_b(lista_nivel, H, L, W,sys.argv[1][:-4])

