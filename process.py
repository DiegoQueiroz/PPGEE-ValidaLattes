# -*- coding: utf-8 -*-
'''
Created on 14/11/2013

@author: Diego
'''

from __future__ import print_function

if __name__ == '__main__':

    prof_anterior = ''

    while True:
        try:
            linha = raw_input()
        except EOFError:
            if prof_anterior != '':
                print('</table>')
            exit()

        campos = linha.split(';')

        # 0 -> Nome orientador
        # 1 -> Lattes orientador
        # 2 -> Nível
        # 3 -> Nome aluno
        # 4 -> Lattes aluno
        # 5 -> Status (OK, ERRO, INEXISTENTE)

        status = campos[5]
        if status == 'INEXISTENTE':
            status = 'Não vinculado'

        prof_atual = campos[0]

        if prof_atual <> prof_anterior:
            if prof_anterior != '':
                print('</table>')

            prof_anterior = prof_atual

            print('<h2>%s (<a href="%s" target="_blank">lattes</a>)</h2>' % (prof_atual, campos[1]))
            print('<table border="1" cellspacing="0">')
            print('\t<tr><th>Nível</th><th>Nome</th><th>Status</th></tr>')

        print('<tr><td>%s</td><td><a href="%s" target="_blank">%s</a></td><td>%s</td></tr>' % (campos[2], campos[4], campos[3], status))
