#program do obliczania przemieszczen danego obiektu wrac z analizą
#bazujacy na modelu roznicowym
import pprint
import math
import numpy as np

#PRZYKLAD danych, które należy wkleić!!!
'''Dla pomiaru aktualnego

A0;601;0.95239;4
1;2;0.18719;1
2;3;-0.27623;1
3;4;0.19082;1
4;5;-0.00107;1
5;6;-0.00859;1
6;1;-0.09210;1
3;A0;0.56071;2
Dla pomiaru pierwotnego

A0;601;0.95240;4
1;2;0.15066;1
2;3;-0.27571;1
3;4;0.23454;1
4;5;-0.03175;1
5;6;0.01191;1
6;1;-0.08969;1
3;A0;0.56068;2'''


print('Podaj plik .csv ze znakiem rozdzielającym ";" dla pomiaru pierwotnego tj. OD DO dH l.stanowisk[n]. Wszystko w metrach.')
lista_pierwotne = []
lista_wtorne = []

#pobieranie danych zadanych przez uzytkownika
print('Podaj wartosci dla ciagu pierwotnego i wcisnij ENTER')
while True:
    pierwotne = input()
    if pierwotne: #and wtorne:
        lista_pierwotne.append(pierwotne)
    else:
        break
print('Podaj wartosci dla ciagu wtornego i wcisnij ENTER')
while True:
    wtorne = input()
    if wtorne:
        lista_wtorne.append(wtorne)
    else:
        break
text1 = '\n'.join(lista_pierwotne)
text2 = '\n'.join(lista_wtorne)
linie1=text1.split('\n')
linie2=text2.split('\n')

print('Podaj pierwszy punkt stały i wcisnij ENTER')
staly1=input()
print('Podaj drugi punkt stały i wcisnij ENTER - jesli go nie ma, pomiń ENTEREM.')
staly2=input()

#sformatowanie danych uzytkownika z formatu csv do listy
pierwotne_cala=[]
wtorne_cala=[]
for x in linie1:
    x=x.split(';')
    pierwotne_cala.append(x)
for y in linie2:
    y=y.split(';')
    wtorne_cala.append(y)

#stworzenie macierzy L i macierzy wagowej P
macierz_L=[]
macierz_P=[]
for dhx,dhy in zip(wtorne_cala,pierwotne_cala):
    macierz_L.append(float(dhx[2])-float(dhy[2]))
    macierz_P.append(1/(float(dhx[3])+float(dhy[3])))
macierz_L.append(0) #------------------------------------------------------
macierz_L=np.array(macierz_L)
macierz_P = np.array(macierz_P)
macierz_P_diag=np.zeros((len(pierwotne_cala),len(pierwotne_cala)))
macierz_P=np.fill_diagonal(macierz_P_diag,macierz_P)

#pozyskanie numerow punktow bez powtorek
numeracja_punktow=[]
roznice_wysokosci=[]
for numery in pierwotne_cala:
    numeracja_punktow.append(numery[0])
    numeracja_punktow.append(numery[1])
    roznice_wysokosci.append([numery[0],numery[1]])
numeracja_punktow_sort = [i for n, i in enumerate(numeracja_punktow) if i not in numeracja_punktow[:n]]

#generowanie macierzy A
macierz_A=[]
macierz_A=np.zeros((len(pierwotne_cala),len(numeracja_punktow_sort)))
macierz_A=macierz_A.tolist()

#pobieranie indeksow do macierzy A
i=-1
for roznice in roznice_wysokosci:
    i+=1
    nr1=numeracja_punktow_sort.index(roznice[0])
    nr2=numeracja_punktow_sort.index(roznice[1])
    macierz_A[i][nr1]=-1
    macierz_A[i][nr2]=1

#numpy convert to array
macierz_A=np.array(macierz_A)

#dodawanie wierszy
r,c=macierz_A.shape
newrow=[]
newrow_c=[]
for dudu in range(r):
    newrow.append(0)
macierz_A=np.vstack((macierz_A,newrow))
macierz_P_diag=np.vstack((macierz_P_diag,newrow))

#rozmiar macierzy A po dodaniu wierszy
rows, cols = macierz_A.shape
n = rows
u = cols

#dodanie punktow stalych
if staly1 in numeracja_punktow_sort:
    indeksik=numeracja_punktow_sort.index(staly1)
for dada in range(r+1):
    newrow_c.append(0)
macierz_P_diag=np.c_[macierz_P_diag,newrow_c]
macierz_P_diag[r][r]=1000
nowy_wiersz=[]
nowy_wiersz_c=[]
wagowa_wiersz=[]
wagowa_wiersz_c=[]
r2,c2=macierz_A.shape
r3,c3=macierz_P_diag.shape
macierz_A[n-1][indeksik]=1

#robota dla drugiego dodanego stalego
if staly2 in numeracja_punktow_sort:
    indeksik2=numeracja_punktow_sort.index(staly2)
    for dudi in range(c2):
        nowy_wiersz.append(0)
    for dadi in range(r2+1):
        nowy_wiersz_c.append(0)
    for piri in range(c3):
        wagowa_wiersz.append(0)
    for puru in range(c3+1):
        wagowa_wiersz_c.append(0)
    macierz_A=np.vstack((macierz_A,nowy_wiersz))
    macierz_P_diag = np.vstack((macierz_P_diag, wagowa_wiersz))
    macierz_P_diag=np.c_[macierz_P_diag,wagowa_wiersz_c]
    macierz_P_diag[c3][c3]=1000
    macierz_A[r2][indeksik2]=1
    macierz_L=np.append(macierz_L,0)
else:
    print('')

#obliczenie macierzy x
macierz_x=np.linalg.inv(np.transpose(macierz_A)@(macierz_P_diag@macierz_A))@(np.transpose(macierz_A)@(macierz_P_diag@macierz_L))
r4,c4=macierz_A.shape

#obliczenie poprawek, m0, bledow H i bledow dH
V=(macierz_A@macierz_x)-macierz_L
m0=math.sqrt((np.transpose(V)@macierz_P_diag@V)/(r4-c4))
mac_cov_H=m0**2*np.linalg.inv(np.transpose(macierz_A)@(macierz_P_diag@macierz_A))
mac_cov_dH=macierz_A@mac_cov_H@np.transpose(macierz_A)
bledy_H=np.sqrt(mac_cov_H.diagonal())
bledy_dH=np.sqrt(mac_cov_dH.diagonal())
wyrownane=macierz_L-V

#generowanie raportu
numeracja_punktow_sort_stale=[]
for numer in numeracja_punktow_sort:
    numeracja_punktow_sort_stale.append(str(numer))
numeracja_punktow_sort_stale.append(str(staly1))
numeracja_punktow_sort_stale.append(str(staly2))
plik_txt=open('wyrownanie.txt','w')
plik_txt.write('Raport z wyrównania przemieszczeń metodą różnicową'+'\n')
plik_txt.write('Autor: Szymek Ślęczka'+'\n'*5)
plik_txt.write('Numeracja punktów wraz z punktami stałymi'+'\n'+str(numeracja_punktow_sort_stale)+'\n'*2)
plik_txt.close()
plik_txt=open('wyrownanie.txt','a')
np.savetxt(plik_txt,macierz_A,fmt = '%.6f',header='macierz A',footer='\n'*2)
np.savetxt(plik_txt,macierz_P_diag,fmt = '%.6f',header='macierz wagowa P',footer='\n'*2)
np.savetxt(plik_txt,macierz_L,fmt = '%.6f',header='macierz L',footer='\n'*2)
np.savetxt(plik_txt,wyrownane,fmt = '%.6f',header='Przemieszczenia wyrównane',footer='\n'*2)
np.savetxt(plik_txt,bledy_H,fmt = '%.6f',header='Błędy wyrównanych przemieszczeń',footer='\n'*2)
np.savetxt(plik_txt,bledy_dH,fmt = '%.6f',header='Błędy wyrównanych przewyższeń',footer='\n'*2)
plik_txt.close()
plik_txt=open('wyrownanie.txt','a')
plik_txt.write('m0='+'%.8s' % str(m0*1000)+'\n'*2)
plik_txt.write('Punkt stały nr 1: '+str(staly1)+'\n')
plik_txt.write('Punkt stały nr 2: '+str(staly2)+'\n')
plik_txt.close()

#wypisanie wszystkiego - test
'''pprint.pprint(pierwotne_cala)
pprint.pprint(wtorne_cala)
print(numeracja_punktow_sort)
pprint.pprint(macierz_A)
print(macierz_L)
print(macierz_P_diag)
print(macierz_x)
print(V)
print(m0*1000)
print(bledy_H)
print(bledy_dH)
print(wyrownane)'''
