#!/usr/bin/env python3
"""SandStress - A sand-based stress test."""

# To the extent possible under law,
# Arnaud Meuret has waived all copyright
# and related or neighboring rights to Canola Field.
# This work is published from: Japan.

# nuitka-project: --windows-product-name="Canola Field"
# nuitka-project: --windows-company-name="Arnaud MEURET"
# nuitka-project: --windows-file-description="Canola Field - A video toy by Arthus MEURET"
# nuitka-project: --windows-product-version=0.2.0.0
# nuitka-project: --windows-icon-from-ico=icon64.png
# nuitka-project: --windows-disable-console

# NOTnuitka-project: --linux-onefile-icon=icon64.png

# nuitka-project: --include-data-file=canola320.png=
# nuitka-project: --include-data-file=CanolaField.png=
# nuitka-project: --include-data-file=clouds320x180-01.png=
# nuitka-project: --include-data-file=PD320x180.png=
# nuitka-project: --include-data-file=help.png=
# nuitka-project: --include-data-file=fist.png=
# nuitka-project: --onefile

from random import randint
from time import perf_counter
import pyxel
from tweening import TimedBool
from tweening import TimedValue


class App:

    def __init__(self):
        self.version = 0.2
        self.w = 320
        self.h = 180

        pyxel.init(self.w, self.h,
                   title="Canola Field - Just Relax",
                   fps=60,
                   quit_key=pyxel.KEY_Q)

        self.colliders = pyxel.Image(self.w, self.h)
        self.colliders.rect(0, 0, self.w, self.h, 0)

        self.palette = [0x2B2B17,
                        0x3971BB,
                        0x4A86CF,
                        0x4B4B2D,
                        0x5F9CE5,
                        0x625922,
                        0x7DB0F2,
                        0x7F6C1A,
                        0x9E8B2E,
                        0xABB2BD,
                        0xBAA11F,
                        0xBFC9E4,
                        0xCBCEDB,
                        0xD0B929,
                        0xDFC516,
                        0xEEEEF6]
        pyxel.colors.from_list(self.palette)

        self.photo = pyxel.Image(320, 180)
        self.photo.load(0, 0, "canola320.png")

        self.titleI = pyxel.Image(320, 180)
        self.titleI.load(0, 0, "CanolaField.png")

        self.cloudsI = pyxel.Image(320, 180)
        self.cloudsI.load(0, 0, "clouds320x180-01.png")

        self.pdI = pyxel.Image(320, 180)
        self.pdI.load(0, 0, "PD320x180.png")

        self.helpI = pyxel.Image(320, 180)
        self.helpI.load(0, 0, "help.png")

        self.fistI = pyxel.Image(320, 180)
        self.fistI.load(0, 0, "fist.png")

        self.vzI = pyxel.Image(320, 180)
        self.vzI.load(0, 0, "vz.png")

        self.grainCountCeil = 300
        self.maxGrains = TimedValue(self.grainCountCeil, 60*20, 'easeInExpo')
        self.inBeach = 0
        self.inAir = 0
        self.showColliders = True
        self.sticky = True
        self.jitter = True
        self.spread = 4
        self.guided = False
        self.autofill = True
        self.paused = False
        self.pauseVisible = True
        self.titleScreen = True
        self.helpOn = False
        self.maskOn = False
        self.flash = False

        self.titleIntro = TimedBool(3*60)
        self.countVisible = TimedBool(1*60)
        self.pdY = TimedValue(0, 60*2, 'easeInOutQuart', -80)
        self.helpOnY = TimedValue(50, 60*1, 'easeOutCubic', 180)
        self.helpOffY = TimedValue(180, 60*1, 'easeInCubic', 50)
        self.helpY = self.helpOffY
        self.cloudsY = TimedValue(0, 60*1.0, 'easeOutElastic', -180, delay=60*2)
        self.titleX = TimedValue(0, 60*1, 'easeOutBack', 320, delay=60*2.5)

        pyxel.run(self.update, self.draw)

    def draw(self):
        if self.titleScreen:
            self.drawTitle()
            return

        if self.flash:
            pyxel.cls(15)
            self.flash = False
            return

        pyxel.blt(0, 0, self.beach, 0, 0, self.w, self.h)

        self.drawGrains()

        if self.maskOn:
            pyxel.blt(0, 0, self.vzI, 0, 0, self.w, self.h, 14)
        if self.paused:
            self.drawPause()
        # pyxel.text(10, 30, "IN AIR: " + str(self.inAir), 5)
        # pyxel.text(10, 40, "IN BEACH: " + str(self.inBeach), 5)
        # pyxel.text(10, 48, str(pyxel.mouse_x) + str(pyxel.mouse_y), 5)
        if not self.countVisible.true():
            pyxel.text(self.centX(str(self.grainCountCeil)), 100, str(self.grainCountCeil), 15)

        self.drawHelp()
        # self.drawPalette()
        pyxel.pset(pyxel.mouse_x, pyxel.mouse_y, 15)

    def drawPause(self):
        if not self.pauseVisible:
            return
        pauseText = ["- CANOLA -",
                     "Relax watching a golden canola field",
                     "",
                     "[ESC] to resume",
                     "[SPACEBAR] to hide this message",
                     "[H] for Help",
                     "[S] to Stop",
                     "",
                     "Send me an e-mail to enjoy updates",
                     "",
                     "arnaud@meuret.net"]
        for i in range(len(pauseText)):
            t = pauseText[i]
            x = self.centX(t)
            y = self.h * 0.15 + i * 7
            pyxel.text(x+1, y+1, t, 3)
            pyxel.text(x, y, t, 11)

    def drawTitle(self):
        pyxel.cls(0)
        pyxel.blt(0, self.cloudsY.value(), self.cloudsI, 0, 0, self.w, self.h)
        pyxel.blt(self.titleX.value(), 0, self.titleI, 0, 0, self.w, self.h, 0)
        pyxel.blt(0, self.pdY.value(), self.pdI, 0, 0, self.w, self.h, 6)
        if self.titleIntro.elapsed():
            pyxel.text(304, 180-6, f"v{self.version}", 1)
            if pyxel.frame_count % 60 < 30:
                t = "PRESS SPACE"
                pyxel.text(self.centX(t), 100, t, 1)
        # self.drawPalette()

    def drawHelp(self):
        pyxel.blt(0, self.helpY.value(), self.helpI, 0, 0, self.w, self.h, 14)

    def drawPalette(self):
        for x in range(16):
            pyxel.rect(x * 4, 0, 4, 4, x)
            pyxel.text(x * 4, 4, str(x%10), 8)

    def drawGrains(self):
        for g in self.grains:
            if not g: continue
            pyxel.pset(g[0], g[1], g[2])

    def centX(self, text, col=-1):
        if col == -1:
            col = self.w // 2
        x = col - len(text) // 2 * 4
        return x

    def newGrain(self):
        retries = 0
        if self.autofill:
            spawnY = 0
        else:
            spawnY = pyxel.mouse_y
        keepSearching = True
        while keepSearching: # Python Sucks !!!
            if self.guided:
                spawnX = pyxel.mouse_x
            else:
                spawnX = randint(0, self.w - 1)
            if self.jitter:
                spawnX += randint(0, self.spread) - self.spread//2
            retries += 1
            keepSearching = spawnX >= self.w or spawnX < 0
            if keepSearching: continue
            # keepSearching = self.busy[spawnX] or self.altitudes[spawnX] < 100 and retries < 100
            keepSearching = self.busy[spawnX] and retries < 100

        if retries == 100 or self.altitudes[spawnX] < spawnY: return

        for i in range(int(self.maxGrains.value())):
            if not self.grains[i]:
                color = self.photo.pget(spawnX, self.altitudes[spawnX] - 1)
                speed = randint(10, 10) / 10
                # self.grains[i] = [spawnX, spawnY, [10, 9, 4][randint(0, 2)]]
                self.grains[i] = [spawnX, spawnY, color, speed]
                self.inAir += 1
                self.busy[spawnX] = True
                # print("New grain ", i, spawnX, spawnY)
                break

    def paintCollider(self, erase=False):
        self.colliders.circ(pyxel.mouse_x, pyxel.mouse_y, 2, 0 if erase else 8)

    def updateReactionField(self):
        print("Updating RF")
        for y in range(0, self.h):
            for x in range(0, self.w):
                self.updateReaction(x, y, False)

    def updateReaction(self, x, y, single=True):
        if x < 0 or x >= self.w or y < 0 or y >= self.h:
            print("Out of bounds")
            return
        # Look up Decision Code
        dc = self.colliders.pget(x, y)
        if dc == 0:
            if self.beach.pget(x, y) == 12:
                # print("No update")
                return
            else:
                dc = 8
        dcBelow = self.colliders.pget(x, y + 1)
        # if dcBelow == 0:
        #     print("Decision: NOP (below is empty)")
        #     self.colliders.pset(x, y, 0)  # NOP
        #     return
        dcAbove = self.colliders.pget(x, y - 1)
        # if dcAbove != 0:
        #     print("Decision: UNK (above is not empty)")
        #     self.colliders.pset(x, y, 8)  # UNK
        #     return
        if not single and (dc == 0 or dc == 2 or dc == 1):
            print("No update")
            return
        # UNKnown: compute new Decision Code
        if dc == 8 or single:
            print("Updating ", x, y, dc)
            if self.colliders.pget(x + 1, y) == 0:
                print("Decision: RDH")
                self.colliders.pset(x, y, 2)  # RDH
                # Update neighbours
                if (dc == 8 or dc == 0) and single:
                    print("Propag to -1, -1")
                    self.updateReaction(x - 1, y - 1)
                    print("Propag to -1, 0")
                    self.updateReaction(x - 1, y)
                    print("Propag to +1, -1")
                    self.updateReaction(x + 1, y - 1)
                    print("Propag to 0, -1")
                    self.updateReaction(x, y - 1)
                    print("Propag to 1, 0")
                    self.updateReaction(x + 1, y)
            elif self.colliders.pget(x - 1, y) == 0:
                print("Decision: LDH")
                self.colliders.pset(x, y, 3)  # RDH
            else:
                print("Decision: STY")
                self.colliders.pset(x, y, 1)  # STY
                return True
        else:
            print("Unex ", dc)

    def updateGrain(self, idx):
        if self.paused:
            return
        g = self.grains[idx]
        if not g: return
        nextX = g[0]
        nextY = g[1] + 1
        dc = self.colliders.pget(nextX, nextY)
        # RDH
        if dc == 2:
            nextX += 1
        # LDH
        elif dc == 3:
            nextX -= 1
        # STY
        elif dc == 1:
            print("UpdateGrain STY")
            nextY = nextY - 1
            # Grain now becomes static
            # self.updateReaction(nextX, nextY)
            self.updateReactionField()
            self.beach.pset(nextX, nextY, g[2])
            self.grains[idx] = None
        g[0] = nextX
        g[1] = nextY

    def update(self):

        if pyxel.btnp(pyxel.KEY_SPACE):
            if self.titleScreen:
                self.resetField()
                self.titleScreen = False
            if self.paused:
                self.pauseVisible = not self.pauseVisible

        if not self.titleScreen and pyxel.btnp(pyxel.KEY_S):
            self.pauseVisible = True
            self.titleScreen = True
            self.paused = False
            self.helpOn = False
            self.titleIntro.reset()
            self.pdY.reset()
            self.titleX.reset()

        if (pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and
            pyxel.mouse_x > 0 and
            pyxel.mouse_y > 0 and
            pyxel.mouse_x < self.w and
            pyxel.mouse_y < self.h or
            self.autofill
            and not self.titleScreen
            and not self.paused):
            self.newGrain()

        if pyxel.btnp(pyxel.KEY_H):
            if self.helpOn:
                self.helpY = self.helpOffY
            else:
                self.helpY = self.helpOnY
            self.helpOn = not self.helpOn
            self.helpY.reset()

        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self.paused = not self.paused

        if pyxel.btnp(pyxel.KEY_M):
            self.maskOn = not self.maskOn

        if pyxel.btnp(pyxel.KEY_PAGEUP):
            self.grainCountCeil += 10
            if self.grainCountCeil > 300:
                self.grainCountCeil = 300
                self.flash = True
            self.countVisible.reset()
            self.maxGrains = TimedValue(self.grainCountCeil, 60*1, 'linear')

        if pyxel.btnp(pyxel.KEY_PAGEDOWN):
            self.grainCountCeil -= 10
            if self.grainCountCeil < 1:
                self.grainCountCeil = 1
                self.flash = True
            self.countVisible.reset()
            self.maxGrains = TimedValue(self.grainCountCeil, 60*1, 'linear')

        if not self.paused and not self.titleScreen:
            for i in range(300):
                # self.updateGrain(i)
                g = self.grains[i]
                if g:
                    g[1] += g[3]
                    if g[1] >= self.altitudes[g[0]]:
                        right = False
                        restX = g[0]
                        restY = self.altitudes[restX] - 1
                        if not self.sticky:
                            while restX < self.w -1 and self.altitudes[restX + 1] > restY + 1:
                                right = True
                                self.busy[restX] = False
                                restX += 1
                                restY = self.altitudes[restX] - 1
                            if not right:
                                while restX > 0 and self.altitudes[restX - 1] > restY + 1:
                                    self.busy[restX] = False
                                    restX -= 1
                                    restY = self.altitudes[restX] - 1
                            if restY < 0:
                                restY = 0
                        self.altitudes[restX] = restY
                        self.beach.pset(restX, restY, g[2])
                        self.grains[i] = None
                        self.busy[restX] = False
                        self.inAir -= 1
                        self.inBeach += 1

    def resetField(self):
        self.maxGrains = TimedValue(self.grainCountCeil, 60*20, 'easeInExpo')
        self.grains = [None for _ in range(300)]
        self.altitudes = [self.h for _ in range(self.w)]
        self.beach = pyxel.Image(self.w, self.h)
        self.beach.rect(0, 0, self.w, self.h, 1)
        self.busy = [False for _ in range(self.w)]



App()
