# -*- coding: utf-8 -*-
'''
Created on 12/11/2013

@author: Diego Queiroz
'''

from __future__ import print_function
import urllib2
import re
from bs4 import BeautifulSoup

# Professores credenciados no PCS
# https://uspdigital.usp.br/janus/componente/orientadoresInicial.jsf?action=2&codcpg=3&codare=3141
professores = {
    u'Anarosa Alves Franco Brandão': 'http://lattes.cnpq.br/7369959680190589',
    u'Andre Riyuiti Hirakawa': 'http://lattes.cnpq.br/5549402817673115',
    u'Anna Helena Reali Costa': 'http://lattes.cnpq.br/5116213374235632',
    u'Antonio Mauro Saraiva': 'http://lattes.cnpq.br/0725312844547101',
    u'Carlos Eduardo Cugnasca': 'http://lattes.cnpq.br/6040855194699192',
    u'Cíntia Borges Margi': 'http://lattes.cnpq.br/2144745030697697',
    u'Graca Bressan': 'http://lattes.cnpq.br/5596411109707542',
    u'Hae Yong Kim': 'http://lattes.cnpq.br/7240386704593891',
    u'Jaime Simao Sichman': 'http://lattes.cnpq.br/5539725123736590',
    u'Joao Batista Camargo Junior': 'http://lattes.cnpq.br/7606805059403041',
    u'Jorge Rady de Almeida Junior': 'http://lattes.cnpq.br/9258926153708205',
    u'Jose Sidnei Colombo Martini': 'http://lattes.cnpq.br/7431745973565600',
    u'Liria Matsumoto Sato': 'http://lattes.cnpq.br/9538024465319850',
    u'Marcos Antonio Simplicio Junior': 'http://lattes.cnpq.br/6874544707185541',
    u'Paulo Sergio Cugnasca': 'http://lattes.cnpq.br/9997641567631872',
    u'Paulo Sergio Licciardi Messeder Barreto': 'http://lattes.cnpq.br/7732462269737973',
    u'Pedro Luiz Pizzigatti Corrêa': 'http://lattes.cnpq.br/3640608958277159',
    u'Ricardo Luis de Azevedo da Rocha': 'http://lattes.cnpq.br/5660360751410581',
    u'Romero Tori': 'http://lattes.cnpq.br/8901320181295016',
    u'Tereza Cristina Melo de Brito Carvalho': 'http://lattes.cnpq.br/8587567074814594',
    u'Wilson Vicente Ruggiero': 'http://lattes.cnpq.br/8374340207133919',
}

def getHTML(link):
    fp = urllib2.urlopen(link)
    bs = 1024 * 8
    myhtml = ""
    while True:
        block = fp.read(bs)
        if block == "":
            break
        myhtml += block
    return myhtml

def checkLattes(lattes_url, tipo="Doutorado"):
    lattes_html = getHTML(lattes_url)
    soup = BeautifulSoup(lattes_html)

    # lista de todos os cursos do pesquisador
    cursos = soup.find_all('span', class_='ajaxCAPES')

    # posso ter mais de um doutorado, o que fazer?
    cursos_tipo = [ x for x in cursos
                   if tipo in x.previous_sibling ]

    # pelo menos um tem que estar correto :P
    correto = False
    for curso in cursos_tipo:
        codigo = curso['data-param']

        if '33002010045P3' in codigo:
            correto = True
            break

    return correto

if __name__ == '__main__':

    for prof in sorted(professores):
        prof_html = getHTML(professores[prof])

        prof_soup = BeautifulSoup(prof_html)

        # encontra a <div> onde estao os orientandos
        orient_tag = prof_soup.find('a', {'name':'Orientacoes'}).parent

        # retorna uma lista com todos os orientandos (mestrado/doutorado/ic/etc.)
        orient = orient_tag.find_all('div', class_='layout-cell layout-cell-11')

        # lista de PhD/master
        phd = [
            ( re.search(r'(.*?\s\w{2,})\.', me.get_text(), re.UNICODE).group(1),
            me.a['href'] if me.a else '' )
            for me in orient if
                u"Doutorado em" in me.get_text()
                and u"outra natureza" not in me.get_text()
                and ( u"Universidade de São Paulo" in me.get_text()
                      or u"USP" in me.get_text().upper()
                      or u"Escola Politécnica" in me.get_text()
                    )
        ]

        master = [
            ( re.search(r'(.*?\s\w{2,})\.', me.get_text(), re.UNICODE).group(1),
            me.a['href'] if me.a else '' )
            for me in orient if
                u"Mestrado em" in me.get_text()
                 and u"outra natureza" not in me.get_text()
                 and ( u"Universidade de São Paulo" in me.get_text()
                      or u"USP" in me.get_text().upper()
                      or u"Escola Politécnica" in me.get_text()
                    )
        ]

        for aluno,lattes in phd:
            if lattes:
                if checkLattes(lattes, "Doutorado"):
                    lattesOK = 'OK'
                else:
                    # Código incorreto
                    lattesOK = "ERRO"
            else:
                # Currículo não está vinculado com orientador
                lattesOK = 'INEXISTENTE'

            msg = ';'.join([prof,professores[prof],'Doutorado',aluno,lattes,lattesOK])
            print(msg.encode('utf-8'))

        for aluno,lattes in master:
            if lattes:
                if checkLattes(lattes, "Mestrado"):
                    lattesOK = 'OK'
                else:
                    # Código incorreto
                    lattesOK = "ERRO"
            else:
                # Currículo não está vinculado com orientador
                lattesOK = 'INEXISTENTE'

            msg = ';'.join([prof,professores[prof],'Mestrado',aluno,lattes,lattesOK])
            print(msg.encode('utf-8'))

