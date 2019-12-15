from jogo_da_velha_rules import *
from learning_agent import *
import sys
import os

simbolo_humano = 'X'
simbolo_computador = 'O'

exploration_p = 0
computador = LearningAgent( actions=[str(x) for x in range(1,10)] , alpha=0.9 , discount_factor=0.9 )

sair_do_jogo = False
while not sair_do_jogo:

    S = [ ' ' , ' ' , ' ' ,' ' , ' ' , ' ' ,' ' , ' ' , ' ' ]

    primeira_jogada = True
    while True:
        printa_estado(S)

        jogada = None
        print("Digite sua jogada (1-9):")
        while True:
            inpt = input()
            jogada = ( int(inpt) if (len(inpt)==1 and inpt!=' ') else 5 )
            if is_jogada_possivel(jogada,S):
                break
            else:
                print("Essa jogada não é possível. Digite um número de 1 a 9 que represente uma casa vazia:")
        apply_jogada(jogada,S,simbolo_humano)
        
        if( is_estado_final(S) ) : 
            break
        elif( primeira_jogada == False ):
            pontos = pontuacao(S)
            recompensa = pontos[simbolo_computador] - pontos[simbolo_humano]
            recompensa=0
            computador.feedback( S , 5*recompensa )
        primeira_jogada = False

        jogada_computador = int( computador.estimate_next_play( S , exploration_p ) )
        while not is_jogada_possivel(jogada_computador,S):
            # Ensina que fazer uma jogada impossivel é errado
            computador.feedback(S,-10) 
            jogada_computador = int( computador.estimate_next_play( S , exploration_p) )
        apply_jogada(jogada_computador,S,simbolo_computador)
        
        if( is_estado_final(S) ) : 
            break
        

    print("Estado final:")
    printa_estado(S)
    simbolo_ganhador = is_estado_final(S)
    print("Vencedor: {}".format( simbolo_ganhador ))
    
    if( simbolo_ganhador == simbolo_computador ):
        computador.feedback( S , 100 )
        is_estado_final(S)
    elif( simbolo_ganhador == simbolo_humano ):
        computador.feedback( S , -100 )
    else:
        computador.feedback( S , 0 )

    print("Quer continuar jogando?(s/n)")
    resposta = input()
    sair_do_jogo = (resposta=='n')

print("Salvando aprendizado...")
computador.save_params()