from pyquery import PyQuery as pq
from urllib import request
import json

class GeografiaImmobiliare(object):

	def __init__(self):
		self.geografia = {"Lombardia" : {}}

	def getProvince(self):
		for regione in self.geografia:
			json_data = json.loads(request.urlopen("https://www.immobiliare.it/servicesV6/mapchart/cartineMapArea/regioni/"+regione.lower()[:3]+".json").read().decode('utf8'))
			for provincia in json_data["area"]:
				self.geografia[regione][provincia["nome"]] = {"sigla": provincia["idProvincia"]}

	def getComuni(self):
		for regione in self.geografia:
			for provincia in self.geografia[regione]:
				sigla = self.geografia[regione][provincia]["sigla"]
				del(self.geografia[regione][provincia]["sigla"])
				header ={"referer":"https://www.immobiliare.it/"}
				req =  request.Request("https://www.immobiliare.it/services/geography/getGeography.php?action=getComuniProvincia&idProvincia="+sigla, headers=header)
				json_data = json.loads(request.urlopen(req).read().decode("utf8"))
				for comune in json_data["result"]:
					self.geografia[regione][provincia][comune["nome"]] = {"idComune": comune["idComune"], "conZone": comune["conZone"], "conLocalita": comune["conLocalita"]}

	def getZone(self):
		for regione in self.geografia:
			for provincia in self.geografia[regione]:
				for comune in self.geografia[regione][provincia]:
					if self.geografia[regione][provincia][comune]["conZone"]:
						del(self.geografia[regione][provincia][comune]["conZone"])
						idComune = self.geografia[regione][provincia][comune]["idComune"]
						del(self.geografia[regione][provincia][comune]["idComune"])
						header ={"referer":"https://www.immobiliare.it/"}
						req =  request.Request("https://www.immobiliare.it/services/geography/getGeography.php?action=getMacrozoneComune&idComune="+idComune, headers=header)
						json_data = json.loads(request.urlopen(req).read().decode("utf8"))
						self.geografia[regione][provincia][comune]["Zone"] = []
						for idZona in json_data["result"]:
							self.geografia[regione][provincia][comune]["Zone"] += [{"Nome" : json_data["result"][idZona]['macrozona_nome_sn'], "keyurl": json_data["result"][idZona]['macrozona_keyurl']}]
