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
	('fa fa-bar-chart', 'Grafiek'),
	('fa fa-car', 'Auto'),
	('fa fa-battery-3', 'Batterij'),
	('fa fa-bolt', 'Bliksem'),
	('fa fa-bomb', 'Bom'),
	('fa fa-calendar', 'kalender'),
	('fa fa-camera', 'Fototoestel'),
	('fa fa-child', 'Link'),
	('fa fa-cloud', 'Wolk'),
	('fa fa-commenting-o', 'Tekstballon'),
	('fa fa-exclamation', 'Uitroepteken'),
	('fa fa-flag', 'Vlag'),
	('fa fa-gift', 'Geschenk'),
	('fa fa-group', 'Groep mensen'),
	('fa fa-glass', 'Glas'),
	('fa fa-home', 'Home'),
	('fa fa-heart-o', 'Hart'),
	('fa fa-cutlery', 'Bestek'),
	('fa fa-globe', 'Wereldbol'),
	('fa fa-hashtag', 'Hashtag'),
	('fa fa-key', 'Sleutel'),
	('fa fa-magic', 'Toverstaf'),
	('fa fa-microphone', 'Microfoon'),
	('fa fa-mobile', 'GSM'),
	('fa fa-paint-brush', 'Penceel'),
	('fa fa-pencil', 'Potlood'),
	('fa fa-quote-right', 'Aanhalingstekens'),
	('fa fa-shopping-basket', 'Mandje'),
	('fa fa-star', 'Ster'),
	('fa fa-user', 'Gebruiker'),
	('fa fa-video-camera', 'Camera'),
)

ICON_COLOR_CHOICES = (
	('text-default', 'Wit'),
	('text-gray', 'Lichtgijs'),
	('text-primary', 'Yourin Rood'),
	('text-deluge', 'Paars'),
	('text-piction-blue', 'Blauw'),
	('text-mantis', 'Rood-oranje'),
	('text-malibu', 'Lichtblauw'),
	('text-carrot', 'Oranje'),
	('text-red', 'Fel Rood'),
	('text-blue-gray', 'Paars-blauw'),
	('text-pink', 'Donkerpaars'),
	('text-green', 'Groen'),
	('text-yellow', 'Geel'),
)