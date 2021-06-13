import time
import traceback
import os

from overlay import Overlay
from entities import *

import pymem

overlay = Overlay()
overlay.init()

def loadDriver(filename):
    wrd = os.getcwd()
    command = "start " + str(wrd) + "\\kernel\\" + "kdmapper.exe" + " " + str(filename) + ".sys"
    os.system(command)

class Program:
    def __init__(self):
        self.memory = True

        if overlay.crosshair:
            overlay.create_crosshair()

        if self.memory:
            self.mem = pymem.Pymem("RustClient.exe")
            self.gameassembly_base = pymem.process.module_from_name(self.mem.process_handle, "GameAssembly.dll").lpBaseOfDll
            self.unityplayer_base = pymem.process.module_from_name(self.mem.process_handle, "UnityPlayer.dll").lpBaseOfDll
            print("Process RustClient.Exe, handle opened")

        self.mainloop()

    def mainloop(self):
        gomaddress = 0x17C1F18
        basenetworkable = 0x29402C0
        off_playermodel = 0x4A8
        off_inventory = 0x608
        off_activegun = 0x570
        off_displayname = 0x650
    
        while True:
            if self.memory:
                ullBufferlist = self.mem.read_ulonglong(self.mem.read_ulonglong(self.mem.read_ulonglong(self.mem.read_ulonglong(self.mem.read_ulonglong(self.gameassembly_base + basenetworkable) + 0xB8)) + 0x10) + 0x28)
                ullObjectlist = self.mem.read_ulonglong(ullBufferlist + 0x18)
                self.matrix4x4 = []
                self.entities = []
                self.sznames = ["LootContai", "Stash", "OreResource", "SupplyDrop", "Boar", "Bear", "Chicken", "Deer", "Wolf", "Horse"]
                try:
                    for i in range(self.mem.read_int(ullBufferlist + 0x10)):
                        element = self.mem.read_ulonglong(ullObjectlist + (0x20 + (i * 0x8)))
                        temp = self.mem.read_ulonglong(element)
                        szName = self.mem.read_string(self.mem.read_ulonglong(temp + 0x10), 13)
                   

                        pBaseObject = self.mem.read_ulonglong(element + 0x10)

                        if pBaseObject == 0:
                            continue

                        pObjectt = self.mem.read_ulonglong(pBaseObject + 0x30)

                        if pObjectt == 0:
                            continue

                        pObject = self.mem.read_ulonglong(pObjectt + 0x30)

                        if pObject == 0:
                            continue

                        if i == 0 and szName == "BasePlayer":
                            TEMPTEMPplayer = self.mem.read_ulonglong((pObject + 0x18))
                            LocalPlayer = self.mem.read_ulonglong((TEMPTEMPplayer + 0x28))

                        if overlay.norecoil and i == 0 or not overlay.norecoil and i == 0:
                            if overlay.norecoil:
                                value_aimcone = overlay.recoil_aimcone
                                value_recoil = overlay.recoil_value
                            else:
                                value_aimcone = 1.0
                                value_recoil = -8.0

                            player = LocalPlayer
                            if player != 0:
                                inventory = self.mem.read_ulonglong(player + off_inventory)
                                belt = self.mem.read_ulonglong(inventory + 0x28)
                                itemlist = self.mem.read_ulonglong(belt + 0x38)
                                items = self.mem.read_ulonglong(itemlist + 0x10)
                                for itemsOnbelt in range(6):
                                    try:
                                        if items != 0:
                                            item = self.mem.read_ulonglong(items + 0x20 + (itemsOnbelt * 0x8))
                                            if self.mem.read_int(item + 0x28) == self.mem.read_int(player + off_activegun):
                                                held = self.mem.read_ulonglong(item + 0x98)
                                               
                                                self.mem.write_float(held + 0x2D4, value_aimcone)
                                                self.mem.write_float(held + 0x2D8, value_aimcone)

                                                recoilPropert = self.mem.read_longlong(held + 0x2C0)

                                                self.mem.write_float(recoilPropert + 0x18, value_recoil * -1)
                                                self.mem.write_float(recoilPropert + 0x1C, value_recoil * -1)
                                                self.mem.write_float(recoilPropert + 0x20, value_recoil)
                                                self.mem.write_float(recoilPropert + 0x24, value_recoil)


                                            else:
                                                pass
                                    except:
                                        continue

                        if overlay.esp:
                            if i % 100 == 0:
                                camera = self.mem.read_ulonglong(self.mem.read_ulonglong(self.mem.read_ulonglong(self.mem.read_ulonglong(self.unityplayer_base + gomaddress) + 0x8) + 0x10) + 0x30)
                                matrix4x4 = []
                                for j in range(16):
                                    matrix4x4.append(self.mem.read_float(self.mem.read_ulonglong(camera + 0x18) + 0xDC + 0x4 * j))
                                overlay.matrix4x4 = matrix4x4
                            
                            #  PlayerBase Entities
                            if "BasePlayer" or "NPCPlayer" in szName:
                                try:
                                    TEMPTEMP = self.mem.read_ulonglong((pObject + 0x18))
                                    temp_pObject = self.mem.read_ulonglong((TEMPTEMP + 0x28))
                                    name = self.mem.read_ulonglong(temp_pObject + off_displayname)
                                    intname = self.mem.read_int(name + 0x10)
                                    name_ = ""
                                    for i in range(intname):
                                        name_ += str(self.mem.read_string(name + 0x14 + i))
                                    if temp_pObject == LocalPlayer:
                                        pass
                                    else:
                                        x = self.mem.read_float(self.mem.read_ulonglong(temp_pObject + off_playermodel) + 0x1d8)
                                        y = self.mem.read_float(self.mem.read_ulonglong(temp_pObject + off_playermodel) + 0x1dc)
                                        z = self.mem.read_float(self.mem.read_ulonglong(temp_pObject + off_playermodel) + 0x1e0)
                                        position = (x, y, z)
                                        health = int(self.mem.read_float(temp_pObject + 0x20C))
                                        self.entities.append(Entity(position, "Player", health = health, playername = name_))
                                        continue
                                except:
                                    pass

                            for i in range(len(self.sznames)):
                                try:
                                    if self.sznames[i] in szName:
                                        szName2 = self.mem.read_string(self.mem.read_ulonglong(pObjectt + 0x60), 50)
                                        TEMPTEMP = self.mem.read_ulonglong(pObject + 0x8)
                                        x = self.mem.read_float(self.mem.read_ulonglong(TEMPTEMP + 0x38) + 0x90)
                                        y = self.mem.read_float(self.mem.read_ulonglong(TEMPTEMP + 0x38) + 0x90 + 0x4)
                                        z = self.mem.read_float(self.mem.read_ulonglong(TEMPTEMP + 0x38) + 0x90 + 0x8)
                                        position = (x, y, z)
                                        self.entities.append(Entity(position, self.sznames[i], szName2 = szName2))
                                        break
                                except:
                                    pass


                    overlay.entities = self.entities
                except:
                    pass
            time.sleep(0.001)

if __name__ == "__main__":
    #loadDriver("driver")
    Program()
