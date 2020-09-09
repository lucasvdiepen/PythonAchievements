Python 3.8.5 (tags/v3.8.5:580fbb0, Jul 20 2020, 15:43:08) [MSC v.1926 32 bit (Intel)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> print('Mijn naam is Lucas')
Mijn naam is Lucas
>>> naam = 'Lucas'
>>> print(naam)
Lucas
>>> print(naam.upper())
LUCAS
>>> print(naam[0:2])
Lu
>>> print(naam[::-1])
sacuL
>>> leeftijd = 16
>>> print('Hallo ' + naam + ' ben je al ' + str(leeftijd) + ' jaar?')
Hallo Lucas ben je al 16 jaar?
>>> leeftijd = leeftijd + 1
>>> leeftijd
17
>>> leeftijd-=1
>>> leeftijd
16
>>> if leeftijd < 18:
	hoelang_tot18jaar = 18 - leeftijd
	print('Over ' + str(hoelang_tot18jaar) + ' jaar wordt je 18')
elif leeftijd > 18:
	hoelang_al18jaar = leeftijd - 18
	print('Het is alweer ' + str(hoelang_al18jaar) + ' jaar geleden dat je 18 werd ;-)')
else:
	print('Je bent precies ' + str(leeftijd) + ' jaar')

	
Over 2 jaar wordt je 18
>>> from random import randint
>>> randint(0, 1000)
857
>>> willekeurig_getal = randint(0, 1000)
>>> willekeurig_getal
713
>>> print('Willekeurig getal tussen 0 en 1000: ' + str(willekeurig_gettal))
Traceback (most recent call last):
  File "<pyshell#25>", line 1, in <module>
    print('Willekeurig getal tussen 0 en 1000: ' + str(willekeurig_gettal))
NameError: name 'willekeurig_gettal' is not defined
>>> print('Willekeurig getal tussen 0 en 1000: ' + str(willekeurig_getal))
Willekeurig getal tussen 0 en 1000: 713
>>> from datetime import datetime
>>> datum = datetime.now()
>>> print(datum)
2020-09-09 14:20:36.516087
>>> datum.strftime('%A %d %B %Y')
'Wednesday 09 September 2020'
>>> import locale
>>> locale.setlocale(locale.LC_TIME, 'nl_NL')
'nl_NL'
>>> locale.setlocale(locale.LC_TIME, 'it_IT')
'it_IT'
>>> datum.strftime('%A %d %B %Y')
'mercoledì 09 settembre 2020'
>>> 