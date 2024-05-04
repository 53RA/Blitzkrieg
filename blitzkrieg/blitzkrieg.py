import pygame, math, random, tkinter as Tk
from functools import partial
from tkinter import *

pygame.init()
pygame.display.set_caption('Blitzkieg')

schermo = pygame.display.set_mode((1900, 1000))
clock = pygame.time.Clock()

# --- dichiaro tutte le variabili importanti ---
angolo_corpo_carro=0
bianco = (225,225,225)
nero = (0,0,0)
contatore1=0
proiettile = False
#font per le scritte
font = pygame.font.Font('pixelmania.ttf', 32)
font2 = pygame.font.Font('upheavtt.ttf', 32)
# x e y giocatore
xP1=950 
yP1=500
# x e y cursore
x=0
y=0
# x e y cursore nel momento in cui spari
xs = 0
ys = 0
# x e y proiettile
xProiettile = 0
yProiettile = 0
#nemici
nemici = []
proiettili_nemici = []
#variabile usata per determinare eventi casuali
a_caso = 0
#punteggio
punteggio = -1
#altro
frame = 0
hitbox = False
gioco = False
done = False
numero_nemici = 0
visuallizzazione_punteggio = False

#nascondere il cursore del mouse (per sostituirlo con il mio custom fighissimo)
pygame.mouse.set_visible(False)

def probabilità_spawn_nemico():
    global spawna_un_nemico
    spawna_un_nemico = 0
    if frame % 100 == 0:
        spawna_un_nemico = 1

def movimento_carro():
    global xP1, yP1, angolo_corpo_carro, tasto
    tasto=pygame.key.get_pressed()
    if tasto[pygame.K_d]:
        angolo_corpo_carro=0
        xP1+=6
    if tasto[pygame.K_a]:
        angolo_corpo_carro=180
        xP1-=6
    if tasto[pygame.K_w]:
        angolo_corpo_carro=90
        yP1-=6
    if tasto[pygame.K_s]:
        angolo_corpo_carro=270
        yP1+=6
    if tasto[pygame.K_w] and tasto[pygame.K_d]:
        angolo_corpo_carro=45
    if tasto[pygame.K_w] and tasto[pygame.K_a]:
        angolo_corpo_carro=135
    if tasto[pygame.K_s] and tasto[pygame.K_d]:
        angolo_corpo_carro=315
    if tasto[pygame.K_s] and tasto[pygame.K_a]:
        angolo_corpo_carro=225

def blitRotate2(surf, immagine, topleft, angle):
    global new_rect
    rotated_immagine = pygame.transform.rotate(immagine, angle)
    new_rect = rotated_immagine.get_rect(center = immagine.get_rect(topleft = topleft).center)
    surf.blit(rotated_immagine, new_rect.topleft)

def generazione__proiettile_nemico():
    global proiettili_nemici
    global xP1
    global yP1
    try:
        a_caso = random.randint(0, (len(nemici) - 1))
        nemico_che_spara = nemici[a_caso]
        if (nemico_che_spara['x'] >= 0 and nemico_che_spara['x'] <= 1900) and (nemico_che_spara['y'] >= 0 and nemico_che_spara['y'] <= 1000):
            immagine_proiettile = pygame.image.load('immagini\\Proiettile - tagliato.png').convert_alpha()
            immagine_proiettile = pygame.transform.scale(immagine,(54,54))
            rect_proiettile = immagine_proiettile.get_rect()
            rect_proiettile.center = [nemico_che_spara['x'], nemico_che_spara['y']]
            proiettile = {
                'texture_proiettile' : immagine_proiettile,
                'rect_proiettile' : rect_proiettile,
                'x' : nemico_che_spara['x'],
                'y' : nemico_che_spara['y'],
                #x e y del giocatore al momento dello sparo:
                'xp' : xP1,
                'yp' : yP1,
                #x e y del nemico al momento dello sparo:
                'xn' : nemico_che_spara['x'],
                'yn' : nemico_che_spara['y']
            }
            proiettili_nemici.append(proiettile)
    except: pass

def generazione_nemico():
    global nemici
    a_caso = random.randint(1,2)
    ynemico = random.randint(100, 900)
    if a_caso == 1:
        xnemico = -200
    if a_caso == 2:
        xnemico = 2100

    rect_corpo = immagine_corpo_nemico.get_rect()
    rect_corpo.center = [xnemico, ynemico]
    immagine_cannone_nemico = pygame.image.load('immagini\\sprite carri\\cannone_nemico.png').convert_alpha()
    immagine_cannone_nemico = pygame.transform.scale(immagine_cannone_nemico, (325, 163))
    immagine_cannone_nemico = pygame.transform.flip(immagine_cannone_nemico, True, False)
    rect_cannone = immagine_cannone_nemico.get_rect()
    rect_cannone.center = [xnemico, ynemico]
    nemico = {
        'corpo' : immagine_corpo_nemico,
        'cannone' : immagine_cannone_nemico,
        'rect_corpo' : rect_corpo,
        'rect_cannone' : rect_cannone,
        'x' : xnemico,
        'y' : ynemico,
        'lato_iniziale' : a_caso    #per sapere da che lato dello schermo il nemico è partito
    }
    nemici.append(nemico)

# --- scegliere le immagini ---
corpo = pygame.image.load('immagini\\sprite carri\\corpo_carro_V3_copia.png').convert_alpha()
corpo = pygame.transform.scale(corpo,(231, 150))

cannone = pygame.image.load('immagini\\sprite carri\\cannone_carro_V3.png').convert_alpha()
cannone = pygame.transform.scale(cannone,(300, 150))

immagine_corpo_nemico = pygame.image.load('immagini\\sprite carri\\corpo_nemico.png').convert_alpha()
immagine_corpo_nemico = pygame.transform.scale(immagine_corpo_nemico, (300, 150))

immagine_cursore = pygame.image.load('immagini\\cursore_a.png').convert_alpha()
immagine_cursore = pygame.transform.scale(immagine_cursore, (150, 150))

medaglia = pygame.image.load('immagini\\medaglia.png').convert_alpha()
medaglia = pygame.transform.scale(medaglia,(256, 1024))

# --- inizia il gaming ---

while not done:

    frame += 1
    
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
        if event.type == pygame.MOUSEBUTTONDOWN and gioco == False:
            click = event.pos
            if escir.collidepoint(click):
                done = True
            if riprendir.collidepoint(click) and punteggio != -1:
                gioco = True
            if nuovarunr.collidepoint(click):
                punteggio = 0
                xP1=  950 
                yP1 = 500
                xProiettile = -100
                yProiettile = -100
                gioco = True
                frame = 0
                nemici = []
                nemicir = []
                nemicicord = []
            if hitbox_tastor.collidepoint(click):
                hitbox = not hitbox
            if high_scorer.collidepoint(click):
                visuallizzazione_punteggio = True
        elif event.type == pygame.MOUSEBUTTONDOWN and proiettile == False:
            if event.button == 1:
                proiettile = True
                xProiettile = xP1 - 50
                yProiettile = yP1 - 50 
                # x e y del cursore al momento dello sparo
                xs = x
                ys = y
                angolo_proiettile = angolo_gradi
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                gioco = not(gioco)
                visuallizzazione_punteggio = False

    if gioco == True:

        schermo.fill(bianco)

        # --- movimento personaggio ---
        movimento_carro()

        # --- sparare ---
        #si può sparare un colpo solo se non ci sono altri colpi già sullo schermo
        rect_proiettile = pygame.Rect(xProiettile,yProiettile,100,100)
        for i in range(len(nemici)-1):
            try:
                if pygame.Rect.colliderect(nemici[i]['rect_corpo'], rect_proiettile):
                    proiettile = False
                    immagine_esplosione = pygame.image.load('immagini\\esplosione.png').convert_alpha()
                    immagine_esplosione = pygame.transform.scale(immagine_esplosione, (250, 250))
                    rect_esplosione = immagine_esplosione.get_rect()
                    rect_esplosione.center = [nemici[i]['x'], nemici[i]['y']]
                    schermo.blit(immagine_esplosione, rect_esplosione)
                    xProiettile = -100
                    yProiettile = -100
                    punteggio += 1
                    nemici.pop(i)
            except: pass

        if (xProiettile > 1900) or (xProiettile < -100) or (yProiettile > 1000) or (yProiettile < -100):
            proiettile = False
        
        if proiettile:
            immagine = pygame.image.load('immagini\\Proiettile - tagliato.png').convert_alpha()
            immagine = pygame.transform.scale(immagine,(50,50))
            topleft = (xProiettile,yProiettile)
            blitRotate2(schermo, immagine, topleft, angolo_proiettile)
            v = (xs - xP1, ys - yP1)
            mod_v = math.sqrt(((v[0])**2)+((v[1]**2)))
            v_n = ((v[0] / mod_v),(v[1] / mod_v))
            try: 
                xProiettile += (v_n[0])*75
                yProiettile += (v_n[1])*75
            except: pass
            rect_proiettile = pygame.Rect(xProiettile,yProiettile,100,100)

        # --- personaggio ---
        #corpo
        topleft = (xP1 -  115, yP1 - 75)
        blitRotate2(schermo, corpo, topleft, angolo_corpo_carro)
        if hitbox:
            pygame.draw.rect(schermo, (0, 0, 200), new_rect, 5)
        #cannone
        topleft = (xP1 - 150, yP1 - 75)
        #calcolo angolo cannone
        angolo = math.atan2(y - yP1, x - xP1)
        angolo_gradi = angolo * 180 / math.pi
        angolo_gradi = -angolo_gradi
        blitRotate2(schermo, cannone, topleft, angolo_gradi)
        if hitbox:
            pygame.draw.rect(schermo, (200, 200, 200), new_rect, 5)

        # --- punteggio ---
        scritta_punteggio = font.render(f'{punteggio}', True, nero, bianco)
        scritta_punteggior = scritta_punteggio.get_rect()
        scritta_punteggior.center = (1800, 100)
        schermo.blit(scritta_punteggio, scritta_punteggior)

        # --- proiettili nemici ---
        if frame % 150 == 0:
            generazione__proiettile_nemico()
        
        rect_corpo = corpo.get_rect()
        rect_corpo.center = [xP1, yP1]
        
        try:
            for i in range (len(proiettili_nemici)):
                
                if pygame.Rect.colliderect(proiettili_nemici[i]['rect_proiettile'], rect_corpo):
                        xP1=  950 
                        yP1 = 500
                        xProiettile = -100
                        yProiettile = -100
                        frame = 0
                        nemici = []
                        nemicir = []
                        nemicicord = []
                        proiettili_nemici = []
                        gioco = False
                        schermo.blit

                        #salvo il punteggio su un altra variabile perché ho bisogno di cancellarlo ma non perdere il valore
                        punteggio_b = punteggio
                        punteggio = 0


                        #dopo essere stati colpiti si chiede in input il nome del giocatore
                        def Salvare_il_nome(usernameEntry) :
                            global nome_utente
                            usernameText = usernameEntry.get()
                            nome_utente = usernameText
                            print(nome_utente)
                            tkWindow.destroy()
                            return
                        #finestra creata con tkiner
                        tkWindow = Tk()  
                        tkWindow.geometry('400x150')  
                        tkWindow.title('Inserire Nome')
                        usernameLabel = Label(tkWindow, text = 'inserisci il tuo nome')
                        usernameEntry = Entry(tkWindow)
                        Salvare_il_nomeCallable = partial(Salvare_il_nome, usernameEntry)
                        #submit button
                        submitButton = Button(tkWindow, text= 'Submit', command = Salvare_il_nomeCallable)
                        #place label, entry, and button in grid
                        usernameLabel.grid(row=0, column=0)
                        usernameEntry.grid(row=0, column=1)
                        submitButton .grid(row=1, column=1) 
                        #main loop
                        tkWindow.mainloop()


                        #si scrive il nome assieme al punteggio nel fal dove sono custoditi tutti i record
                        def leggi_dati(file_path):
                            global dati
                            dati = []
                            try:
                                with open('punteggi.txt', 'r') as file:
                                    for riga in file:
                                        
                                        nome, punteggio = riga.strip().split()
                                        dati.append((nome, int(punteggio)))
                            except FileNotFoundError:
                                pass  # Se il file non esiste, iniziamo con una lista vuota
                            return(dati)
                        
                        def scrivi_dati(file_path, dati):
                            with open('punteggi.txt', 'w') as file:
                                for nome, punteggio in dati:
                                    file.write(f'{nome} {punteggio}\n')
                                    print(f'{nome} {punteggio}\n')

                        # Leggi dati esistenti dal file
                        file_path = 'punteggi.txt'
                        dati = leggi_dati(file_path)
                        print(dati)
                        punteggio_giocatore = punteggio_b
                        # Aggiungi il nuovo giocatore ai dati
                        dati.append((nome_utente, punteggio_giocatore))
                        print(dati)

                        # Ordina i dati in base al punteggio
                        dati.sort(key=lambda x: x[1], reverse=True)

                        # Scrivi i dati aggiornati nel file
                        scrivi_dati(file_path, dati)
                        

                immagine_proiettile = proiettili_nemici[i]['texture_proiettile']
                rect_proiettile = proiettili_nemici[i]['rect_proiettile']
                schermo.blit(proiettili_nemici[i]['texture_proiettile'], proiettili_nemici[i]['rect_proiettile'])
                v = (proiettili_nemici[i]['xn'] - proiettili_nemici[i]['xp'], proiettili_nemici[i]['yn'] - proiettili_nemici[i]['yp'])
                mod_v = math.sqrt(((v[0])**2)+((v[1]**2)))
                v_n = ((v[0] / mod_v),(v[1] / mod_v))
                try: 
                    proiettili_nemici[i]['x'] -= (v_n[0])*10
                    proiettili_nemici[i]['y'] -= (v_n[1])*10
                except: pass
                proiettili_nemici[i]['rect_proiettile'] = pygame.Rect(proiettili_nemici[i]['x'],proiettili_nemici[i]['y'],100,100)
                
        except: pass
            


        # --- nemici ---

        probabilità_spawn_nemico()

        if spawna_un_nemico == 1:
            generazione_nemico()

        for i in range (len(nemici)-1):
            immagine_cannone_nemico = nemici[i]['corpo']
            rect_corpo = immagine_corpo_nemico.get_rect()
            rect_corpo.center = [nemici[i]['x'], nemici[i]['y']]

            topleft = (nemici[i]['x'] - 162.5, nemici[i]['y'] - 81.5)

            if nemici[i]['lato_iniziale'] == 1:
                nemici[i]['x'] += 3
                schermo.blit(nemici[i]['corpo'], rect_corpo)
            else:
                nemici[i]['x'] -= 3
                blitRotate2(schermo, nemici[i]['corpo'], topleft, 180)

            if nemici[i]['x'] < -300:
                nemici[i]['x'] = 2300
            
            if nemici[i]['x'] > 2300:
                nemici[i]['x'] = -300

            nemici[i]['rect_corpo'] = rect_corpo
            
            #calcolo angolo cannone
            angolo = math.atan2(xP1 - nemici[i]['x'], yP1 - nemici[i]['y'])
            angolo_gradi = angolo * 180 / math.pi
            angolo_gradi = angolo_gradi + 90
            blitRotate2(schermo, nemici[i]['cannone'], topleft, angolo_gradi)
            if hitbox:
                pygame.draw.rect(schermo, (225, 0, 0), rect_corpo, 5)

        # --- cursore ---
        immagine_cursorer = immagine_cursore.get_rect()
        (x, y) = pygame.mouse.get_pos()
        immagine_cursorer.center=[x, y]
        schermo.blit(immagine_cursore, immagine_cursorer)


    # --- schermata che appare quando si vedono i punteggi:
    
        
    elif visuallizzazione_punteggio:
        schermo.fill(0)
        medagliar = medaglia.get_rect()
        medagliar.center = (200, 425)
        schermo.blit(medaglia,medagliar)
        medagliar = medaglia.get_rect()
        medagliar.center = (1700, 425)
        schermo.blit(medaglia,medagliar)
        with open('punteggi.txt','r') as file_highscore:
            highscore = file_highscore.readline()
        high_score = font2.render(f'highscores', True, bianco, nero)
        high_score = pygame.transform.scale(high_score,(1000, 156))
        high_scorer = high_score.get_rect()
        high_scorer.center = (950, 100)
        schermo.blit(high_score, high_scorer)
        with open('punteggi.txt', 'r') as file:
            y_nome = 225
            for riga in file:
                y_nome += 50
                nome_da_scrivere = riga.strip()
                nome_scritto = font2.render(f'-- {nome_da_scrivere} --', True, bianco, nero)
                nome_scrittor = nome_scritto.get_rect()
                nome_scrittor.center = (950, y_nome)
                schermo.blit(nome_scritto, nome_scrittor)


    # --- quando il gioco è in pausa o è avviato per la prima volta ---
    else:
        schermo.fill(0)

        #titolo
        titolo = pygame.image.load('immagini\\bottoni_menù\\titolo.png').convert_alpha()
        titolo = pygame.transform.scale(titolo,(1000, 156))
        titolor = titolo.get_rect()
        titolor.center = (950, 150)
        schermo.blit(titolo,titolor)

        #tasto riprendi
        riprendi = pygame.image.load('immagini\\bottoni_menù\\riprendi.png').convert_alpha()
        riprendi = pygame.transform.scale(riprendi,(550, 58))
        riprendir = riprendi.get_rect()
        riprendir.center = (950, 400)
        if riprendir.collidepoint(x,y) and punteggio != -1:
            riprendi = pygame.image.load('immagini\\bottoni_menù\\riprendi_rosso.png').convert_alpha()
            riprendi = pygame.transform.scale(riprendi,(583, 61))
            riprendir = riprendi.get_rect()
            riprendir.center = (950, 400)
        elif punteggio == -1:
            riprendi = pygame.image.load('immagini\\bottoni_menù\\riprendi_grigio.png').convert_alpha()
            riprendi = pygame.transform.scale(riprendi,(550, 58))
            riprendir = riprendi.get_rect()
            riprendir.center = (950, 400)
        schermo.blit(riprendi,riprendir)

        #tasto nuova run
        nuovarun = pygame.image.load('immagini\\bottoni_menù\\nuova_run.png').convert_alpha()
        nuovarun = pygame.transform.scale(nuovarun,(589, 58))
        nuovarunr = nuovarun.get_rect()
        nuovarunr.center = (950, 500)
        if nuovarunr.collidepoint(x,y):
            nuovarun = pygame.image.load('immagini\\bottoni_menù\\nuova_run_rosso.png').convert_alpha()
            nuovarun = pygame.transform.scale(nuovarun,(622, 61))
            nuovarunr = nuovarun.get_rect()
            nuovarunr.center = (950, 500)
        schermo.blit(nuovarun,nuovarunr)

        #tasto esci
        esci = pygame.image.load('immagini\\bottoni_menù\\esci.png').convert_alpha()
        esci = pygame.transform.scale(esci,(267, 58))
        escir = esci.get_rect()
        escir.center = (950, 600)
        if escir.collidepoint(x,y):
            esci = pygame.image.load('immagini\\bottoni_menù\\esci_rosso.png').convert_alpha()
            esci = pygame.transform.scale(esci,(300, 65))
            escir = esci.get_rect()
            escir.center = (950, 600)
        schermo.blit(esci, escir)

        #tasto hitbox
        if hitbox == False:
            hitbox_tasto = pygame.image.load('immagini\\bottoni_menù\\checkbox_off.png').convert_alpha()
            hitbox_tasto = pygame.transform.scale(hitbox_tasto,(100, 100))
        else:
            hitbox_tasto = pygame.image.load('immagini\\bottoni_menù\\checkbox_on.png').convert_alpha()
            hitbox_tasto = pygame.transform.scale(hitbox_tasto,(100, 100))
        hitbox_tastor = hitbox_tasto.get_rect()
        hitbox_tastor.center = (650, 802)
        schermo.blit(hitbox_tasto, hitbox_tastor)
        hitbox_tasto = pygame.image.load('immagini\\bottoni_menù\\hitbox onoff.png').convert_alpha()
        hitbox_tasto = pygame.transform.scale(hitbox_tasto,(682, 58))
        hitbox_tastor = hitbox_tasto.get_rect()
        hitbox_tastor.center = (950, 800)
        schermo.blit(hitbox_tasto, hitbox_tastor)

        #high_score
        with open('punteggi.txt','r') as file_highscore:
            highscore = file_highscore.readline()
        high_score = font2.render(f'highscore: {highscore}', True, bianco, nero)
        high_scorer = high_score.get_rect()
        high_scorer.center = (950, 950)
        if high_scorer.collidepoint(x,y):
            high_score = font2.render(f'highscore: {highscore}', True, (225,0,0), nero)
            high_scorer = high_score.get_rect()
            high_scorer.center = (950, 950)
        schermo.blit(high_score, high_scorer)

        #cursore
        immagine = pygame.image.load('immagini\\cursore_a.png').convert_alpha()
        immagine = pygame.transform.scale(immagine,(150,150)) 
        immaginer = immagine.get_rect()
        (x, y) = pygame.mouse.get_pos()
        immaginer.center=[x, y]
        schermo.blit(immagine, immaginer)

    frame += 1
    if frame == 1000:
        frame = 0

    pygame.display.update()

pygame.quit()
exit()