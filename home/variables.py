from django.utils.translation import ugettext_lazy as _

EVENT_CATEGORY_CHOICES = (
	(1, 'Sport'),
	(2, 'Kamp'),
	(3, 'Festival'),
	(4, 'Club'),
)

RELATED_LINK_CHOICES = (
    (1, _("Facebook")),
    (2, _("Twitter")),
    (3, _("Youtube")),
)

ICON_CHOICES = (
	('bar-chart', 'Grafiek'),
	('car', 'Auto'),
	('battery-3', 'Batterij'),
	('bolt', 'Bliksem'),
	('bomb', 'Bom'),
	('calendar', 'kalender'),
	('camera', 'Fototoestel'),
	('child', 'Link'),
	('cloud', 'Wolk'),
	('commenting-o', 'Tekstballon'),
	('exclamation', 'Uitroepteken'),
	('flag', 'Vlag'),
	('gift', 'Geschenk'),
	('group', 'Groep mensen'),
	('glass', 'Glas'),
	('home', 'Home'),
	('heart-o', 'Hart'),
	('cutlery', 'Bestek'),
	('globe', 'Wereldbol'),
	('hashtag', 'Hashtag'),
	('key', 'Sleutel'),
	('magic', 'Toverstaf'),
	('microphone', 'Microfoon'),
	('mobile', 'GSM'),
	('paint-brush', 'Penceel'),
	('pencil', 'Potlood'),
	('quote-right', 'Aanhalingstekens'),
	('shopping-basket', 'Mandje'),
	('star', 'Ster'),
	('user', 'Gebruiker'),
	('video-camera', 'Camera'),
)

ICON_COLOR_CHOICES = (
	('text-default', 'Zwart'),
	('text-gray', 'Lichtgijs'),
	('text-primary', 'Groen'),
	('text-deluge', 'Paars'),
	('text-piction-blue', 'Blauw'),
	('text-mantis', 'Lichtgroen'),
	('text-malibu', 'Lichtblauw'),
	('text-carrot', 'Oranje'),
	('text-red', 'Rood'),
	('text-blue-gray', 'Paars-blauw'),
	('text-pink', 'Donkerpaars')
)