from __future__ import unicode_literals
from random import sample
import csvunicode as csv
 
cartas = {}  # dicionário (tabela)
imagens = {}
tela = 0
reta_final = -2

def setup():
    global espaco_vertical, espaco_horizontal
    global altura_carta, largura_carta
    global um
    fullScreen()
    fonte_bold = loadFont('Tomorrow-Bold-24.vlw')
    # fonte_bold = createFont('Tomorrow Bold', 24)
    textFont(fonte_bold)    
    carregar_cartas()
    espaco_vertical = height * 0.125
    altura_carta = height * 0.75
    um = altura_carta / 120.0
    largura_carta = altura_carta / 3.0 * 2
    espaco_horizontal = (width - 3 * largura_carta) / 4
    # noLoop()
    sorteio()
    
def draw():
    background(0)
    textSize(altura_carta / 100.0)
    if tela == 0:
        textSize(20)
        textAlign(CENTER, CENTER)
        fill(255)
        text("Metonímia\nclique com o mouse ou aperte uma tecla", width / 2, height / 2)
    elif tela == 1:
        desenha_cartas(None, None, None)
    elif tela == 2:
        desenha_cartas(t1, None, None)
    elif tela == 3:
        desenha_cartas(t1, t2, None)
    elif tela == 4:
        desenha_cartas(t1, t2, t3)

def sorteio():
    global t1, t2, t3
    # global reta_final
    # t1 = sentimentos[reta_final]
    # t2 = sentimentos[reta_final + 1]
    # t3 = sentimentos[reta_final + 2]
    # reta_final = reta_final + 3
    t1, t2, t3 = sample(sentimentos, 3)
    # t1 = 'Ódio' # para forçar uma carta
    # while t1 not in cartas or t2 not in cartas or t3 not in cartas:    
    #     t1, t2, t3 = sample(sentimentos, 3)
    imagens.clear()
    imagens[t1] = loadImage(cartas[t1][1])
    imagens[t2] = loadImage(cartas[t2][1])
    imagens[t3] = loadImage(cartas[t3][1])
          
    
def desenha_cartas(t1, t2, t3):
    x = espaco_horizontal
    y = espaco_vertical
    if t1 is not None:
        carta(x, y, t1)
    else:
        image(verso, x, y, largura_carta, altura_carta)
    x2 = espaco_horizontal * 2 + largura_carta
    if t2 is not None:
        carta(x2, y, t2)
    else:
        image(verso, x2, y, largura_carta, altura_carta)
    x3 = espaco_horizontal * 3 + largura_carta * 2
    if t3 is not None:
        carta(x3, y, t3)
    else:
        image(verso, x3, y, largura_carta, altura_carta)

def carta(x, y, t):     
    if t in cartas:
        xi, yi = x + 4 * um, y + 4 * um
        largura_imagem = largura_carta - 8 * um
        altura_imagem = altura_carta - 24 * um
        num, img, cor_moldura, cor_texto = cartas[t]
        fill(cor_moldura)
        rect(x, y, largura_carta, altura_carta)
        if imagens[t]:
            image(imagens[t], xi, yi, largura_imagem, altura_imagem)
        else:
            print('imagem não carregada: ' + img)
        textAlign(CENTER, CENTER)
        textSize(altura_carta * 0.05)
        fill(cor_texto)
        text(str(num) + '. ' + t, x + largura_carta / 2, 
            y + altura_carta - 10 * um)
    
def keyReleased():
    proxima_tela()

def mouseReleased():
    proxima_tela()
            
def proxima_tela():    
    global tela
    tela = tela + 1
    if tela == 5:
        tela = 0
        sorteio()

def carregar_cartas():
    global sentimentos, verso
    verso = loadImage('capa.jpg')
    sentimentos = loadStrings('sentimentos.txt')  # nomes para o sorteio
    with open('dados.csv') as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            arquivo_imagem = linha['arquivo']
            if arquivo_imagem:
                sentimento = linha['sentimento']
                num = linha['num']
                try:
                    r = int(linha['R'])
                    g = int(linha['G'])
                    b = int(linha['B'])
                    cor_texto = int(linha.get('cor_texto', 128))
                except ValueError:
                    print(linha)
                    r, g, b = 255, 255, 255
                    cor_texto = 100  
                
                print(sentimento)
                cartas[sentimento] = num, arquivo_imagem, color(r, g, b), cor_texto
