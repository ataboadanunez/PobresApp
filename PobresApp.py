import streamlit as st
from requests import get
import json
from bs4 import BeautifulSoup


def curr_to_float(curr):
	spl = curr.split(',')
	return float(spl[0] + '.' + spl[1])

def get_dolar_tarjeta(currs):
	strVal = currs['tarjeta']['sell']
	return curr_to_float(strVal)

def get_dolar_qatar(currs):
	strVal = currs['qatar']['sell']
	return curr_to_float(strVal)

def calculate_dolar(val, currs, limit=300):
	dolarTarjeta = get_dolar_tarjeta(currs)
	dolarQatar   = get_dolar_qatar(currs)

	limit_ars = limit * dolarTarjeta
	if val < limit_ars:
		return val / dolarTarjeta
	else:
		return (val - limit_ars) / dolarQatar + limit

# get BRL-USD / BRL-EUR 
realito = get('https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL')
realito_dic = realito.json()

usd2brl = float(realito_dic['USDBRL']['bid'])
eur2brl  = float(realito_dic['EURBRL']['bid'])
usd2eur = usd2brl / eur2brl

# get ARS-USD
dolarito = get('https://www.dolarito.ar/')
dolarito_soup = BeautifulSoup(dolarito.content, "html.parser")

# find tag with dolar values
scripts = dolarito_soup.find_all('script')
for script in scripts:
	if 'dolar' in script.text:
		# prepare string for json
		jsonStr = script.text.strip()
		jsonData = json.loads(jsonStr)
		# get currency values navigating through keys
		currs = jsonData['props']['pageProps']['realTimeQuotations']['quotations']



#######################################################################################
# Desing of web App with Streamlit
st.markdown('<iframe src="https://embed.lottiefiles.com/animation/97611"></iframe>', unsafe_allow_html=True)

# display 1 to 1 conversion
disp1, disp2, disp3, disp4 = st.columns(4)
with disp1:
	st.success('Dollar Tarjeta: \n %.2f ARS' %get_dolar_tarjeta(currs))
with disp2:
	st.success('Dollar Qatar: \n %.2f ARS' %get_dolar_qatar(currs))
with disp3:
	st.success('Dollar a Real: \n %.2f BRL' %usd2brl)
with disp4:
	st.success('Dollar a Euro: \n %.2f EUR' %(usd2brl / eur2brl))

col1, col2 = st.columns(2)
with col1:
	curr1 = st.selectbox('Currency 1', ['ARS', 'BRL', 'USD', 'EUR'])
with col2:
	curr2 = st.selectbox('Currency 2', ['ARS (Tarjeta)', 'ARS (Qatar)', 'BRL', 'USD', 'EUR'])


# input / output section
col1, col2 = st.columns(2)
# input value
with col1:
	amount = st.number_input(curr1)
	
# switch between currencies to get conversion. Write a function instead!
def get_conversion(curr1, amount):
	
	dolar_tarjeta = get_dolar_tarjeta(currs)
	dolar_qatar   = get_dolar_qatar(currs)
	
	if (curr1 == 'ARS'):
		usd = calculate_dolar(amount, currs)
		brl = usd * usd2brl
		eur = brl / eur2brl
		ars_tarjeta = amount
		ars_qatar   = amount

	elif curr1 == 'BRL':
		usd = amount / usd2brl
		eur = amount / eur2brl
		brl = amount
		ars_tarjeta = (usd * dolar_tarjeta) if (usd < 300) else (usd * dolar_qatar)
		ars_qatar = usd * dolar_qatar
	
	elif curr1 == 'USD':
		brl = usd2brl * amount
		ars_tarjeta = dolar_tarjeta * amount
		ars_qatar = dolar_qatar * amount
		usd = amount
		eur = usd2eur * amount

	elif curr1 == 'EUR':
		brl = eur2brl * amount
		usd =  amount / usd2eur
		ars_tarjeta = dolar_tarjeta * usd
		ars_qatar = dolar_qatar * usd
		eur = amount
	
	
	conversion = {  'ARS (Tarjeta)' : ars_tarjeta,
					'ARS (Qatar)' : ars_qatar,
					'BRL' : brl,
					'USD' : usd,
					'EUR' : eur
				}

	
	return conversion
		

converted = get_conversion(curr1, amount).get(curr2)


# Disclaimer
disc = False
if curr1 == 'ARS':
	st.text("[*] Conversion using value of Dolar Tarjeta (Qatar) bellow (above) 300USD.")
	disc = True
if curr1 != 'ARS' and curr2 == 'ARS (Tarjeta)' and get_conversion(curr1, amount).get('USD') > 300:
	st.text("[*] Conversion using value of Dolar Qatar as value exceeds 300USD limit.")
	disc = True
with col2:
	if disc:
		st.text('[*] Converted value:')
	else:
		st.text('Converted value:')
	st.success(converted)




hide_menu = """
<style> body {
			text-align : center;
		}

		#MainMenu { 
			visibility : hidden;
		}

		footer {
			visivility : hidden;
		}

		footer:after {
		content:'a. taboada @ 2023';
		display:block;
		}
</style

"""
st.markdown(hide_menu, unsafe_allow_html=True)