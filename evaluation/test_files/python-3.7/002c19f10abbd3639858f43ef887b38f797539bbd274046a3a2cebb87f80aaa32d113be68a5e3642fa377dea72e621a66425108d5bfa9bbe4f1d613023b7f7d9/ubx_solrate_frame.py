"""
UBX Configuration frame for CFG-RATE commands

Created on 19 Feb 2020

:author: semuadmin
:copyright: SEMU Consulting © 2020
:license: BSD 3-Clause
"""
from tkinter import Frame, Spinbox, Button, Label, IntVar, StringVar, E, W
from PIL import ImageTk, Image
from pyubx2 import UBXMessage, POLL, SET
from .globals import ENTCOL, ICON_SEND, ICON_WARNING, ICON_PENDING, ICON_CONFIRMED, READONLY, UBX_CFGRATE, CONNECTED
from .strings import LBLCFGRATE
TIMEREFS = {0: 'UTC', 1: 'GPS', 2: 'GLO', 3: 'BEI', 4: 'GAL'}

class UBX_RATE_Frame(Frame):
    """
    UBX Navigation Solution Rate configuration command panel.
    """

    def __init__(self, app, container, *args, **kwargs):
        """
        Constructor.

        :param Frame app: reference to main tkinter application
        :param Frame container: reference to container frame (config-dialog)
        :param args: optional args to pass to Frame parent class
        :param kwargs: optional kwargs to pass to Frame parent class
        """
        self.__app = app
        self.__master = self.__app.appmaster
        self.__container = container
        Frame.__init__(self, self.__container.container, *args, **kwargs)
        self._img_send = ImageTk.PhotoImage(Image.open(ICON_SEND))
        self._img_pending = ImageTk.PhotoImage(Image.open(ICON_PENDING))
        self._img_confirmed = ImageTk.PhotoImage(Image.open(ICON_CONFIRMED))
        self._img_warn = ImageTk.PhotoImage(Image.open(ICON_WARNING))
        self._measint = IntVar()
        self._navrate = IntVar()
        self._timeref = StringVar()
        self._body()
        self._do_layout()
        self._attach_events()

    def _body(self):
        """
        Set up frame and widgets.
        """
        self._lbl_cfg_rate = Label(self, text=LBLCFGRATE, anchor='w')
        self._lbl_ubx_measint = Label(self, text='Solution Interval (ms)')
        self._spn_ubx_measint = Spinbox(self, values=(25, 50, 100, 200, 500, 1000, 2000, 5000, 10000), width=6, state=READONLY, readonlybackground=ENTCOL, wrap=True, textvariable=self._measint)
        self._lbl_ubx_navrate = Label(self, text='Measurement Ratio')
        self._spn_ubx_navrate = Spinbox(self, from_=1, to=127, width=4, state=READONLY, readonlybackground=ENTCOL, wrap=True, textvariable=self._navrate)
        self._lbl_ubx_timeref = Label(self, text='Time Reference')
        self._spn_ubx_timeref = Spinbox(self, values=list(TIMEREFS.values()), width=5, state=READONLY, readonlybackground=ENTCOL, wrap=True, textvariable=self._timeref)
        self._lbl_send_command = Label(self, image=self._img_pending)
        self._btn_send_command = Button(self, image=self._img_send, width=50, command=self._on_send_rate, font=self.__app.font_md)

    def _do_layout(self):
        """
        Layout widgets.
        """
        self._lbl_cfg_rate.grid(column=0, row=0, columnspan=6, padx=3, sticky=(W, E))
        self._lbl_ubx_measint.grid(column=0, row=1, columnspan=2, rowspan=1, padx=3, pady=3, sticky=W)
        self._spn_ubx_measint.grid(column=2, row=1, columnspan=1, rowspan=1, sticky=W)
        self._lbl_ubx_navrate.grid(column=0, row=2, columnspan=2, rowspan=1, padx=3, pady=3, sticky=W)
        self._spn_ubx_navrate.grid(column=2, row=2, columnspan=2, rowspan=1, sticky=W)
        self._lbl_ubx_timeref.grid(column=0, row=3, columnspan=2, rowspan=1, padx=3, pady=3, sticky=W)
        self._spn_ubx_timeref.grid(column=2, row=3, columnspan=2, rowspan=1, sticky=W)
        self._btn_send_command.grid(column=4, row=1, rowspan=3, ipadx=3, ipady=3, sticky=E)
        self._lbl_send_command.grid(column=5, row=1, rowspan=3, ipadx=3, ipady=3, sticky=E)
        (cols, rows) = self.grid_size()
        for i in range(cols):
            self.grid_columnconfigure(i, weight=1)
        for i in range(rows):
            self.grid_rowconfigure(i, weight=1)
        self.option_add('*Font', self.__app.font_sm)

    def _attach_events(self):
        """
        Bind events to widget.
        """
        self.bind('<Button>', self._do_poll_rate)

    def reset(self):
        """
        Reset panel to initial settings.
        """
        if self.__app.conn_status == CONNECTED:
            self._do_poll_rate()

    def update_status(self, msg: UBXMessage):
        """
        Update pending confirmation status.

        :param UBXMessage msg: UBX config message
        """
        if msg.identity == 'CFG-RATE':
            self._measint.set(msg.measRate)
            self._navrate.set(msg.navRate)
            self._timeref.set(TIMEREFS[msg.timeRef])
            self._lbl_send_command.config(image=self._img_confirmed)
            self.__container.set_status('CFG-RATE GET message received', 'green')
        elif msg.identity == 'ACK-NAK':
            self.__container.set_status('CFG-RATE POLL message rejected', 'red')
            self._lbl_send_command.config(image=self._img_warn)

    def _on_send_rate(self, *args, **kwargs):
        """
        Handle Send rate config button press.
        """
        tref = 0
        for (key, val) in TIMEREFS.items():
            if val == self._timeref.get():
                tref = key
                break
        msg = UBXMessage('CFG', 'CFG-RATE', SET, measRate=self._measint.get(), navRate=self._navrate.get(), timeRef=tref)
        self.__container.send_command(msg)
        self._lbl_send_command.config(image=self._img_pending)
        self.__container.set_status('CFG-RATE SET message sent', 'blue')
        self.__container.set_pending(UBX_CFGRATE, ('ACK-ACK', 'ACK-NAK'))
        self._do_poll_rate()

    def _do_poll_rate(self, *args, **kwargs):
        """
        Poll RATE message configuration.
        """
        msg = UBXMessage('CFG', 'CFG-RATE', POLL)
        self.__container.send_command(msg)
        self._lbl_send_command.config(image=self._img_pending)
        self.__container.set_status('CFG-RATE POLL message sent', 'blue')
        for msgid in ('CFG-RATE', 'ACK-NAK'):
            self.__container.set_pending(msgid, UBX_CFGRATE)