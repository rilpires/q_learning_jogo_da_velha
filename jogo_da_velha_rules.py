
def printa_estado(S):
    print(" ")
    for y in range(0,3):
        offset = 3*y
        print( " {} | {} | {} ".format(S[0+offset],S[1+offset],S[2+offset]) )
        if(y<2):
            print("-----------")
    print(" ")

def is_estado_final(S):
    for x in range(0,3):
        if S[x] != ' ' and S[x] == S[x+3] and S[x] == S[x+6]:
            return S[x]
    for y in range(0,3):
        if S[3*y] != ' ' and S[3*y] == S[1+3*y] and S[3*y] == S[2+3*y]:
            return S[3*y]
    if S[0] != ' ' and S[0] == S[4] and S[0] == S[8]:
        return S[0]
    if S[2] != ' ' and S[2] == S[4] and S[2] == S[6]:
        return S[2]
    if not ' ' in S: return ' '
    return None

def is_jogada_possivel(jogada,S):
    return type(jogada) == int and jogada>=1 and jogada<=9 and S[jogada-1]==' '

def apply_jogada(jogada,S,simbolo):
    S[jogada-1] = simbolo

def pontuacao(S):
    ret = {'X':0,'O':0}
    for simbolo in ret.keys():
        for x in range(0,3):
            for y in range(0,3):
                if S[x+3*y]==simbolo:
                    for dx in [-1,0,1]:
                        for dy in [-1,0,1]:
                            next_x = x + dx
                            next_y = y + dy
                            if( next_x == x and next_y == y ): continue
                            if( next_x>=0 and next_x<=2 and next_y>=0 and next_y<=2 and S[next_x+3*next_y] == simbolo ):
                                ret[simbolo]+=1
    return ret
