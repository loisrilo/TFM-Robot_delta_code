# -*- coding: utf-8 -*-
# Copyright 2016 Lois Rilo Antelo (loisriloantelo@gmail.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import Tkinter


print('hola')


master = Tkinter.Tk()


w = Tkinter.Scale(master, from_=0, to=42, orient=Tkinter.HORIZONTAL)
w.pack()
w = Tkinter.Scale(master, from_=0, to=200, orient=Tkinter.HORIZONTAL)
w.pack()



master.mainloop()
print(w)
