import pygame

"""
関数名 : initPygame
引数　 : 画面の縦と横の長さ
返り値 : pygameのインスタンス
pygameの初期化
"""
def initPygame(WIDTH, HEIGHT) -> pygame.Surface:
    pygame.init()
    backColor = (255, 255, 255)
    width = WIDTH
    height = HEIGHT + 30
    screen = pygame.display.set_mode((width, height), 0, 32)
    screen.fill(backColor)
    return screen

"""
関数名 : getKey
引数　 : 
返り値 : キー入力された文字(pygame仕様)
キー入力を取得する
"""
def getKey():
    pygame.event.pump()
    return pygame.key.get_pressed()

"""
関数名 : updata
引数　 : 
返り値 : 
pygameの画面情報の更新
"""
def updata():
    pygame.display.update()

"""
関数名 : quit
引数　 : 
返り値 : 
pygameの終了
"""
def quit():
    pygame.quit()


"""
関数名 : setText
引数　 : 
返り値 : pygameに出力できるテキスト
pygameに出力するテキストの設定
"""
def setText(msg):
    font = pygame.font.Font(None, 20)
    text = font.render(msg, True, (0, 255, 0))
    return text