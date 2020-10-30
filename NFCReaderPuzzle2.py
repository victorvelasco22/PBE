import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from smartcard.System import readers
from smartcard.util import toHexString
from smartcard.CardType import AnyCardType
from smartcard.CardConnection import CardConnection
from smartcard.CardRequest import CardRequest
import threading

class Finestra(Gtk.Window):
	def __init__(self):
	
		#Creem la finestra
		Gtk.Window.__init__(self, title="Let's read your card")
		self.connect("destroy", Gtk.main_quit)
		self.set_border_width(10)

		#Creem una caixa per situar l'etiqueta a dalt i el botó a baix
		self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)

		#Afegim la caixa a la finestra
		self.add(self.box)

		#Creem una caixa eventual que canviarà de color
		self.evbox = Gtk.EventBox()
		self.evbox.override_background_color(0, Gdk.RGBA(0,0,8,1))

		#Creem l'etiqueta que anirà a la caixa
		self.label = Gtk.Label('<span foreground="white" size="x-large">Please, login with your university card</span>')
		self.label.set_use_markup(True)
		self.label.set_name("Bluelabel")
		self.label.set_size_request(500,100)

		#Afegim l'etiqueta a la caixa
		self.evbox.add(self.label)

		#Creem el botó
		self.button = Gtk.Button(label="Clear")
		self.button.connect("clicked", self.clicked)

		#Afegim el botó a la caixa
		self.box.pack_start(self.evbox, True, True, 0)	
		self.box.pack_start(self.button, True, True, 0)
	
		#Creem i posem en marxa un thread
		thread = threading.Thread(target=self.scan_uid)
		thread.setDaemon(true)
		thread.start()

		#Ho mostrem tot
		slef.show_all()
		Gtk.main()
	
	#Funció que es crida al polsar el botó
	def clicked(self, widget):
		
		#Canviem a la label blava
		self.label.set_label('<span foreground="white" size="x-large">Please, login with your university card</span>')
		self.evbox.override_background_color(0, Gdk.RGBA(0,0,8,1))

		#Tornem a posar en marxa el thread
		thread = threading.Thread(target=self.scan_uid)
		thread.start()

	def scan_uid():

		cardtype = AnyCardType()
		cardrequest = CardRequest( timeout=10, cardType=cardtype )
		cardservice = cardrequest.waitforcard()
		cardservice.connection.connect()

		COMMAND = [0xFF, 0xCA, 0x00, 0x00, 0x00] 	#cmd necessari per inicialitzar la transmissió de dades
		tagID, sw1, sw2 = cardservice.connection.transmit(COMMAND) 	#retorna 3 dades

		def listToString(s): 	#transforma una llista en un string
		
			str1 = ""
			for elem in s:
				str1 += str(elem)
			return str1.replace(" ", "") 	#retorna string sense espais en blanc

		uid = listToString(toHexString(tagID))
		
		#Canviem el color de la label a vermell
		self.label.set_label('<span foreground="white" size="x-large">UID:'+uid+'</span>')
		self.evbox.override_background_color(0, Gdk.RGBA(8,0,0,1))

win = Finestra()
