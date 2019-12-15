from jogo_da_velha_rules import *
from learning_agent import *
import sys
import os

simbolo_1 = 'X'
simbolo_2 = 'O'

exploration_p = 0.1
computador1 = LearningAgent( actions=[str(x) for x in range(1,10)] , alpha=0.8 , discount_factor=0.9 )
computador2 = LearningAgent( actions=[str(x) for x in range(1,10)] , alpha=0.8 , discount_factor=0.9 )

i = 0
while True:
    i+=1
    S = [ ' ' , ' ' , ' ' ,' ' , ' ' , ' ' ,' ' , ' ' , ' ' ]

    primeira_jogada = True
    while True:

        jogada_computador = int( computador1.estimate_next_play( S , exploration_p ) )
        while not is_jogada_possivel(jogada_computador,S):
            # Ensina que fazer uma jogada impossivel é errado
            computador1.feedback(S,-100) 
            jogada_computador = int( computador1.estimate_next_play( S , exploration_p ) )
        apply_jogada(jogada_computador,S,simbolo_1)

        
        if( is_estado_final(S) ) : 
            break
        elif( primeira_jogada == False ):
            pontos = pontuacao(S)
            recompensa = pontos[simbolo_2] - pontos[simbolo_1]
            recompensa=0
            computador2.feedback( S , 5*recompensa )


        jogada_computador = int( computador2.estimate_next_play( S, exploration_p  ) )
        while not is_jogada_possivel(jogada_computador,S):
            # Ensina que fazer uma jogada impossivel é errado
            computador2.feedback(S,-100) 
            jogada_computador = int( computador2.estimate_next_play( S , exploration_p ) )
        apply_jogada(jogada_computador,S,simbolo_2)

        
        if( is_estado_final(S) ) : 
            break
        else:
            pontos = pontuacao(S)
            recompensa = pontos[simbolo_1] - pontos[simbolo_2]
            recompensa=0
            computador1.feedback( S , 5*recompensa )
        primeira_jogada = False


    simbolo_ganhador = is_estado_final(S)
    print("Vencedor: {} no episodio {}".format( simbolo_ganhador , i ))
    
    if( simbolo_ganhador == simbolo_1 ):
        computador1.feedback( S , 100 )
        computador2.feedback( S , -100 )
        is_estado_final(S)
    elif( simbolo_ganhador == simbolo_2 ):
        computador1.feedback( S , -100 )
        computador2.feedback( S , 100 )
    else:
        computador1.feedback( S , 0 )
        computador2.feedback( S , 0 )

    if( i % 10000 == 0 ):
        print("Salvando aprendizado...")
        params1 = computador1.Q.copy()
        params2 = computador2.Q.copy()
        params1.update(params2)
        json.dump(params1,open("params.json","w"))



print("Salvando aprendizado...")
computador.save_params()