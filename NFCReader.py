from smartcard.System import readers
from smartcard.util import toHexString
from smartcard.CardType import AnyCardType
from smartcard.CardConnection import CardConnection
from smartcard.CardRequest import CardRequest

def readTag():
	cardtype = AnyCardType()
	cardrequest = CardRequest( timeout=10, cardType=cardtype )
	cardservice = cardrequest.waitforcard()
	cardservice.connection.connect()

	COMMAND = [0xFF, 0xCA, 0x00, 0x00, 0x00] 	#cmd necessari per inicialitzar la transmissió de dades
	tagID, sw1, sw2 = cardservice.connection.transmit(COMMAND) 	#retorna 3 dades

	print("\t>>> Your UID is: ")
	print("\t>>> 0x{}".format(listenToString(toHexString(tagID))))

def listToString(s): 	#transforma una llista en un string
	str1 = ""
	for elem in s:
		str1 += str(elem)
	return str1.replace(" ", "") 	#retorna string sense espais en blanc

def main():
	print("\t>>> SCAN YOUR PASS (timeout in 10 seconds)\n")
	readTag()

if __name__ == '__main__':
	main()
