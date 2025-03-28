import pygame
import piano_lists as pl
import musicpy as mp
from pygame import mixer
# The following program is a GUI I created using pygame, and my side file called piano_lists,
# this code does not have sound, but can be used using a mouse. There are a few weird things I didn't get to
# fix that may look inconsistent


pygame.init()
pygame.mixer.set_num_channels(50)

# this defines the font level sizes
font = pygame.font.SysFont('arial', 50)
medium_font = pygame.font.SysFont('arial', 25)
small_font = pygame.font.SysFont('arial', 15)
xtra_small_font = pygame.font.SysFont('arial', 9)

# this defines the fps, timer, width, and height of the window as well
fps = 60
timer = pygame.time.Clock()
WIDTH = 1000
HEIGHT = 400
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Python Final Project')

# empty lists we will use in loops in order to show our white and black keys
active_whites = []
active_blacks = []


def draw_piano(whites, blacks):
    # these two lists represent the rectangles that will be appended for the white and black keys
    wr = []
    br = []
    skip_count = 0 # this checks total spaces we've skipped
    last_skip = 2 # this represents the last skip, we will define it as two for now
    skip_track = 2 # this represents when we will skip track

    # this loop goes the amount of times as there are white keys
    for i in range(52):
        # each loops prints a white rectangle, and will print a black border alongside with i
        # (it was supposed to be 52 but after seeing what we have I just redefined the window size above because
        # it is easier)
        key = pl.white_notes[i]
        rect = pygame.draw.rect(screen, 'white', [i * 35, HEIGHT - 300, 35, 300], 0, 2)
        wr.append(rect)
        pygame.draw.rect(screen, 'black', [i * 35, HEIGHT - 300, 35, 300], 2, 2)
        key_label = small_font.render(key, True, 'black')
        screen.blit(key_label, (i * 35 + 3, HEIGHT - 20))

        # This will define the notes that will play when a key is pressed
        note = mp.N(key, duration=0.5)
        mp.write(note, name=f"{key}.mid")
        chord = mp.C(f"{key}:maj", duration=0.5)
        mp.write(chord, name=f"{key}_chord.mid")
        scale = mp.chord(f"{key}, +2, +4, +5, +7, +9, +11, +12",
                     duration=[1/8, 1/8, 1/8, 1/8, 1/8, 1/8, 1/8, 1/4],
                     interval=[1/8, 1/8, 1/8, 1/8, 1/8, 1/8, 1/8, 1/4])
        mp.write(scale, name=f"{key}_scale.mid")

    # this loop ensures that the black keys are not only created, but there are keys
    # that are skipped
    for i in range(36):
        # we define the rect object down below, and use it to append to the br list
        rect = pygame.draw.rect(screen, 'black', [23 + (i * 35) + (skip_count * 35), HEIGHT - 300, 24, 200], 0, 2)

        # this defines the gray color that surrounds the black keys when clicking on it
        for q in range(len(blacks)):
            if blacks[q][0] == i:
                if blacks[q][1] > 0:
                    pygame.draw.rect(screen, 'gray35', [23 + (i * 35) + (skip_count * 35), HEIGHT - 300, 24, 200], 2, 2)
                    blacks[q][1] -= 1

        # These lines define the very small definitions for each black key and appends the rectangles
        key = pl.black_labels[i]
        key_label = xtra_small_font.render(key, True, 'white')
        screen.blit(key_label, (25 + (i * 35) + (skip_count * 35), HEIGHT - 120))
        br.append(rect)
        skip_track += 1

        # this resets each count depending on when the last skip was
        if last_skip == 2 and skip_track == 3:
            last_skip = 3
            skip_track = 0
            skip_count += 1
        elif last_skip == 3 and skip_track == 2:
            last_skip = 2
            skip_track = 0
            skip_count += 1

        # This will define the note that will play when this key is pressed
        note = mp.N(key, duration=0.5)
        mp.write(note, name=f"{key}.mid")
        chord = mp.C(f"{key}:maj", duration=0.5)
        mp.write(chord, name=f"{key}_chord.mid")
        scale = mp.chord(f"{key}, +2, +4, +5, +7, +9, +11, +12",
                     duration=[1 / 8, 1 / 8, 1 / 8, 1 / 8, 1 / 8, 1 / 8, 1 / 8, 1 / 4],
                     interval=[1 / 8, 1 / 8, 1 / 8, 1 / 8, 1 / 8, 1 / 8, 1 / 8, 1 / 4])
        mp.write(scale, name=f"{key}_scale.mid")

    # this loop defines the gray exterior surrounding the key when clicking on it
    for i in range(len(whites)):
        if whites[i][1] > 0:
            j = whites[i][0]
            pygame.draw.rect(screen, 'gray', [j * 35, HEIGHT - 100, 35, 100], 2, 2)
            whites[i][1] -= 1

    return wr, br, whites, blacks


run = True
chords = False
scales = False
while run:
    timer.tick(fps)
    screen.fill('goldenrod')

    # This will create the chord button
    chord_button = pygame.Surface((20, 20))
    if chords:
        chord_button.fill("white")
    else:
        chord_button.fill("black")
    chord_rect = chord_button.get_rect(topleft=(450, 30))
    screen.blit(chord_button, chord_rect)
    chord_label = small_font.render("chords", True, "black")
    screen.blit(chord_label, (410, 30))

    # This will create the scale button
    scale_button = pygame.Surface((20, 20))
    if scales:
        scale_button.fill("white")
    else:
        scale_button.fill("black")
    scale_rect = scale_button.get_rect(topleft=(550, 30))
    screen.blit(scale_button, scale_rect)
    scale_label = small_font.render("scales", True, "black")
    screen.blit(scale_label, (510, 30))

    white_keys, black_keys, active_whites, active_blacks = draw_piano(active_whites, active_blacks)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            black_key = False
            if chord_rect.collidepoint(event.pos):
                scales = False
                if chords:
                    chords = False
                else:
                    chords = True
            if scale_rect.collidepoint(event.pos):
                chords = False
                if scales:
                    scales = False
                else:
                    scales = True
            for i in range(len(black_keys)):
                if black_keys[i].collidepoint(event.pos):
                    key = pl.black_labels[i]
                    if chords:
                        mixer.music.load(f"{key}_chord.mid")
                    elif scales:
                        mixer.music.load(f"{key}_scale.mid")
                    else:
                        mixer.music.load(f"{key}.mid")
                    mixer.music.play()
                    black_key = True
                    active_blacks.append([i, 30])
            for i in range(len(white_keys)):
                if white_keys[i].collidepoint(event.pos) and not black_key:
                    key = pl.white_notes[i]
                    if chords:
                        mixer.music.load(f"{key}_chord.mid")
                    elif scales:
                        mixer.music.load(f"{key}_scale.mid")
                    else:
                        mixer.music.load(f"{key}.mid")
                    mixer.music.play()
                    active_whites.append([i, 30])

    pygame.display.flip()

pygame.quit()