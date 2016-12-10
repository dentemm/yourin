import geopy

from django.core.management.base import BaseCommand, CommandError

from home.models import Address, Location

class Command(BaseCommand):

	help = 'Adds latitude and longitude properties for all Address objects'

	def handle(self, *args, **options):

		for location in Location.objects.all():

			geolocator = geopy.geocoders.Nominatim()

			address_string = location.street + ' ' + location.number + ' ' + location.postal_code + ' ' + location.city + ' ' + str(location.country.name)

			loc = geolocator.geocode(address_string)

			if not isinstance(loc, geopy.location.Location):

				alternative = location.street + ' ' + location.postal_code + ' ' + location.city + ' ' + str(location.country.name)

				loc = geolocator.geocode(alternative)


			if isinstance(loc, geopy.location.Location):

				location.latitude = loc.latitude
				location.longitude = loc.longitude

				location.save()

		self.stdout.write(self.style.SUCCESS('Het is gefixt!'))
