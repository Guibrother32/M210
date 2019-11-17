##########################################################################################################
#                                                                                                        #
#                                       Criado em: 14 Nov 2019                                           #
#                               Autores: Guilherme Costa e Gustavo Marins                                #
#                                   Discilplina: M210 Professor: Yvo                                     #
#                                                                                                        #
##########################################################################################################
from numpy import matrix
from model.F import F

class Tabela(object):

    #definicoes primarias
    
    def princiapl(self, matrix, matrix2):
        
        A = matrix('50 80;');
        B = matrix('3 2;1 1;1 2');
        C = matrix('600;240;300');
        
        np.concatenate((A, B));
        np.concatenate((B, C));
        
        
        return None
    
    #Funcao principal, usa do metodo da File F.py para auxiliar com fracionarios.
    def __init__(self, FO,restricoes=None):

        #fase de preenchimento
        #linhas da tabela das restrições
        self.linhaR = []
        
        numVE = len(restricoes) + len([(c,t,tr) for (c,t,tr) in restricoes if t!='<='])
        
        #linha da função objetivo
        self.linhaFO = [1] + [c*(-1) for c in FO] + [0]*numVE + [0] 
        
        for i,(coef,tipo,termo) in enumerate(restricoes):
            colExtras = [0]*numVE
            
            if tipo == '<=':
                colExtras[i] = 1       
                
            elif tipo=='=':
                colExtras[i] = 1         
                self.linhaFO[1 + len(coef) + i] = F(0, F(1))
                      
            elif tipo=='>=':
                colExtras[i] = -1
                colExtras[i+1] = 1              
                self.linhaFO[1 + len(coef) + i + 1] = F(0, F(1))
            
            self.linhaR.append(self._converteParaF([0] + coef + colExtras + [termo]))
        
    def _converteParaF(self,lista):
        return [F(e) for e in lista]
       
    def printTabela(self):      
        tabela = [self.linhaFO] + self.linhaR    
        print('\n', matrix([[str(f) for f in l] for l in tabela]))
        
        #Pivotamento, elemento pivo é escolhido a partir da coluna mais negativa e a linha LD/elementos da coluna exceto o Z

    def _pivoteamento(self, pi, pj):
        #elemento pivo
        p = self.linhaR[pi][pj]     
        #divide a linha do pivo pelo elemento pivo       
        self.linhaR[pi] = [x/p for x in self.linhaR[pi]]     
        
        #para cada elemento da linha correspondente a funcao objetivo multiplica cada elemento da linha pivo
        tempLinha = [self.linhaFO[pj]* x for x in self.linhaR[pi]]  
        #subtrai cada elemendo da linha da funcao objetivo pelo fator calculado acima
        self.linhaFO = [self.linhaFO[i] - tempLinha[i] for i in range(len(tempLinha))]
        
        #para cara linha corresponte a restricao i repete o mesmo procedimento feito na linha fa F.O.
        for i,restricao in enumerate(self.linhaR):
            if i != pi: 
                tempLinha = [restricao[pj]* x for x in self.linhaR[pi]]         
                self.linhaR[i] = [restricao[i] - tempLinha[i] for i in range(len(tempLinha))]   
         
    
    #Encontra a coluna da variavel que entra na base 
     
    def elemento_Entra(self):
        menor_Coef = min(self.linhaFO[1:-1])
        
        if menor_Coef >= 0: 
            return None
        else:
            #retorna seu indice
            return self.linhaFO[0:-1].index(menor_Coef)
 
    
    #Encontra a linha da variavel que sai da base 
    
    def elemento_Sai(self, coluna_pivo):   
        termos = [r[-1] for r in self.linhaR]
        coef_var_entra = [r[coluna_pivo] for r in self.linhaR]
        
        razoes = []
        for i,termo in enumerate(termos):
            if coef_var_entra[i] == 0:
                razoes.append(F(1,1)) 
            else:
                razoes.append(termo/coef_var_entra[i])
                
        menorRazaoPositiva = min([r for r in razoes if r > 0])        
        #retorna seu indice
        return razoes.index(menorRazaoPositiva)
 
    @property
    def val_Otimo(self):
        if not self.solO_encontrada():
            self.executar()
        
        return self.linhaFO[-1]
    
    
    @property  
    def sol_Otima(self):
        if not self.solO_encontrada():
            self.executar() 
        
        dentro = self.varInBase
        fora = self.varOutBase
        
        solucao = []

        for val in dentro:
            for l in self.linhaR:
                if l[val] == F(1):
                    solucao.append((val,l[-1]))
                    break
        
        solucao += [(val,F(0)) for val in fora]

        return [(t[0],float(t[1])) for t in solucao]
    
    @property
    def varInBase(self):      
        dentroDaBase = [] 
        for c in range(1,len(self.linhaFO)-1):
            valoresColuna = [l[c] for l in self.linhaR]
            
            numDeZeros = len([z for z in valoresColuna if z==F(0)])
            numDeUms = len([u for u in valoresColuna if u==F(1)])
            
            if numDeUms == 1 and numDeZeros == len(self.linhaR) - 1 :
                dentroDaBase.append(c)

        return dentroDaBase
    
    @property
    def varOutBase(self):
        return [i for i in range(1,len(self.linhaFO)-1) if i not in self.varInBase]
        
        

             
 

    #pela funcao objetivo, solucao otima encontrada?
    def solO_encontrada(self):
        if min(self.linhaFO[1:-1]) >= 0: 
            return True
        else:
            return False
    
    #comeco do metodo Simplex
    def executar(self):
        self.printTabela()
        
        while not self.solO_encontrada():
            c = self.elemento_Entra()
            r = self.elemento_Sai(c)
            
            self._pivoteamento(r,c)
            
            print('\nColuna do pivo: %s\nLinha do pivo: %s'%(c+1,r))
            
            self.printTabela()
            

             
def getNomeDeVariavel(index):
    return 'x' + str(index)

def toStringComNomes(lista):
    if type(lista[0]) is type(0):
        return [getNomeDeVariavel(i) for i in lista]
    
    elif type(lista[0]) is type(()):
        return [(getNomeDeVariavel(l[0]),l[1]) for l in lista]

if __name__ == '__main__':
    
    #Como funciona a entrada da FO e restricoes?
    
    #1o passo FO, colocar o valor de cada argumento na primeira chave
    
    #2o passo Restricoes, caso seja nulo, colocar 0;

    #CHAPAS METALICAS
    t = Tabela([5,7,8],restricoes=[([1,1,2],"<=", 1190),([3,4.5,1],"<=", 4000)])
    
    #GOIABA
    #t = Tabela([5,7],restricoes=[([0.25,0.5],"<=", 50),([3,0],"<=", 250),([0,1.5],"<=", 100)])
    
    
    print("\nValor otimo: R$%s (%s)" % (float(t.val_Otimo),t.val_Otimo))

    print("\nSolução otima: %s" % (toStringComNomes(t.sol_Otima)))
    
    print("\nPreço Sombra: R$" % ())
    
    def printTabela2(self):      
        tabela = [self.linhaFO] + self.linhaR    
        print('\n', matrix([[str(f) for f in l] for l in tabela]))
        
