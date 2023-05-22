import streamlit as st
from requests import get
import json

# get currencies
currs = get('https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,USD-ARS,EUR-ARS')
currs_dic = currs.json()

usd2brl = float(currs_dic['USDBRL']['bid'])
eur2brl  = float(currs_dic['EURBRL']['bid'])
usd2ars = float(currs_dic['USDARS']['bid'])
eur2ars = float(currs_dic['EURARS']['bid'])
usd2eur = usd2brl / eur2brl
dolar_tarjeta = usd2ars * 1.75
dolar_qatar   = usd2ars * 2

def calculate_dolar(val, currs, limit=300):

	limit_ars = limit * dolar_tarjeta
	if val < limit_ars:
		return val / dolar_tarjeta
	else:
		return (val - limit_ars) / dolar_qatar + limit

#######################################################################################
# Desing of web App with Streamlit
st.markdown('<iframe src="https://embed.lottiefiles.com/animation/97611"></iframe>', unsafe_allow_html=True)

# display 1 to 1 conversion
disp1, disp2, disp3, disp4 = st.columns(4)
with disp1:
	st.write('''Dolar Tarjeta \n
							%.2f ARS 
					'''%dolar_tarjeta)
with disp2:
	st.write('''Dolar Qatar \n
							%.2f ARS 
					'''%dolar_qatar)
with disp3:
	st.write('''Real \n
							%.2f BRL
					''' %usd2brl)
with disp4:
	st.write('''Euro \n 
						%.2f EUR
					''' %(usd2brl / eur2brl))

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