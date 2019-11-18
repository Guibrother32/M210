##########################################################################################################
#                                                                                                        #
#                                       Criado em: 14 Nov 2019                                           #
#                               Autores: Guilherme Costa e Gustavo Marins                                #
#                                   Discilplina: M210                                                    #
#                                   Professor: Yvo                                                       #
#                                                                                                        #
##########################################################################################################


import numpy as np

#Entrada do numero de linhas e colunas

print("Entre com o numero de linhas:")
ln = input()
linhas = int (ln)

print("Entre com o numero de colunas:")
cl = input()
colunas = int (cl)

s = []
k = 0
tDaMatriz = linhas * colunas
tabela = np.array(tDaMatriz)

for ln in range(0, linhas):
    for cln in range(0, colunas):
        print("Entre com os valores do PPl:")
        k = input()
        s.append(float(k))
        
tabela = s
tabela = np.reshape(tabela, (linhas, colunas))
spxPPL = tabela

# Exemplo para teste retirado em: https://www.youtube.com/watch?v=uendv1Khpcw
#  [3,6] [1 -10 -12 0 0 0 0 1 1 1 0 100 0 1 3 0 1 270]

# Lucro Total($) 1170.00
# Shadow Price($) 9.00
# Shadow Price($) 1.00
# Money($) 15.00
# Money($) 85.00
# [['1' '-5' '-7' '-8' '0' '0' '0']
 #['0.0' '1.0' '1.0' '2.0' '1.0' '0.0' '1190.0']
 #['0.0' '3.0' '4.5' '1.0' '0.0' '1.0' '4000.0']]





def simplexoSolver(spxPPL, linhas, colunas):
    negativer = [0, None] #primeira coluna
    for cln in range(colunas):
        if spxPPL[0, cln] < 0:
            if abs(spxPPL[0, cln]) > negativer[0]:
                negativer[0] = spxPPL[0, cln]
                negativer[1] = cln
    colunaDoPivot = negativer[1]

#----------------------------------------------------------------------------------------------------------------------#

    linhaDoPivot = [999, None]
    for linha in range(linhas):
        LD = spxPPL[linha, colunaDoPivot]

        if LD == 0:
            amount = 999

        else: amount = spxPPL[linha, colunas - 1] / LD

        if amount > 0:
            if amount < linhaDoPivot[0]:
                linhaDoPivot[0] = amount
                linhaDoPivot[1] = linha
    linhaDoPivot = linhaDoPivot[1]

    #o pivot é achado por:
    pivot = spxPPL[linhaDoPivot][colunaDoPivot]

#----------------------------------------------------------------------------------------------------------------------#

    #achando a NLP:
    spxPPL[linhaDoPivot, :] = np.divide(spxPPL[linhaDoPivot, :], pivot)
    for j in range(linhas):
        if j == linhaDoPivot:
            continue
        #achando as NL:
        spxPPL[j, :] = np.add(spxPPL[j, :], spxPPL[linhaDoPivot, :] * -(spxPPL[j, colunaDoPivot])) #calculo feito

# ----------------------------------------------------------------------------------------------------------------------#

    negatory = False
    for h in range(colunas):
        if spxPPL[0, h] < 0:
            negatory = True
            break

    if not negatory: return spxPPL
    else: return simplexoSolver(spxPPL, linhas, colunas)

linhas = np.size(spxPPL, 0)
colunas = np.size(spxPPL, 1)
colunaEND = colunas - 1
resposta = simplexoSolver(spxPPL, linhas, colunas)

lucro = resposta[0, colunaEND]
print("\n\n=======================================")
print("Lucro Total R$: {:.2f}".format(lucro))

aux=0;

for a in range(colunas - linhas, colunaEND):
    sombra = resposta[0, a]
    aux=aux+1;
    print("X"+str(aux)+"-> Preco Sombra R$: {:.2f}".format(sombra))

aux=0;
for b in range(1, linhas):
    money = resposta[b, colunaEND]
    aux=aux+1;
    print("Investimento"+"-> R$ {:.2f}".format(money))

print("=======================================")


#----------------------------------------------------------------------------------------------------------------------#






