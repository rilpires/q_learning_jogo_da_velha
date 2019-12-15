from jogo_da_velha_rules import *
from learning_agent import *
import sys
import os

simbolo_humano = 'X'
simbolo_computador = 'O'

exploration_p = 0.2
computador = LearningAgent( actions=[str(x) for x in range(1,10)] , alpha=0.2 , discount_factor=0.9 )

i = 0
while True:
    i+=1
    S = [ ' ' , ' ' , ' ' ,' ' , ' ' , ' ' ,' ' , ' ' , ' ' ]

    primeira_jogada = True
    while True:

        jogada = None
        while not is_jogada_possivel(jogada,S):
            jogada = random.randint(1,9)
        apply_jogada(jogada,S,simbolo_humano)
        
        if( is_estado_final(S) ) : 
            break
        elif( primeira_jogada == False ):
            pontos = pontuacao(S)
            recompensa = pontos[simbolo_computador] - pontos[simbolo_humano]
            recompensa=0
            computador.feedback( S , recompensa )
        primeira_jogada = False


        jogada_computador = int( computador.estimate_next_play( S, exploration_p  ) )
        while not is_jogada_possivel(jogada_computador,S):
            # Ensina que fazer uma jogada impossivel é errado
            computador.feedback(S,-100) 
            jogada_computador = int( computador.estimate_next_play( S , exploration_p ) )
        apply_jogada(jogada_computador,S,simbolo_computador)
        if( is_estado_final(S) ) : 
            break


    simbolo_ganhador = is_estado_final(S)
    print("Vencedor: {} no episodio {}".format( simbolo_ganhador , i ))
    
    if( simbolo_ganhador == simbolo_computador ):
        computador.feedback( S , 100 )
        is_estado_final(S)
    elif( simbolo_ganhador == simbolo_humano ):
        computador.feedback( S , -100 )
    else:
        computador.feedback( S , 0 )

    if( i % 10000 == 0 ):
        print("Salvando aprendizado...")
        computador.save_params()



print("Salvando aprendizado...")
computador.save_params()