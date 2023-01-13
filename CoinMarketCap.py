# Importando função que envia email
from envia_email import envia_email

from oculto import chave_api

# Importando biblioteca para manipulação e visualização dos dados
import pandas as pd
import matplotlib.pyplot as plt

# Importando biblioteca para conexão com a api do coinmarketcap
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

# Importando biblioteca time
from time import sleep


class CoinMarketCap:

    @staticmethod
    def conexao():
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        parameters = {

            'start': '1',
            'limit': '1000'
        }
        headers = {
            'Accepts': 'application/json',
            'Accept-Encoding': 'deflate, gzip',
            'X-CMC_PRO_API_KEY': chave_api,
        }

        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(url, params=parameters)
            dado = json.loads(response.text)
            return (dado)

        except (ConnectionError, Timeout, TooManyRedirects) as error:
            return(error)

    @staticmethod
    def filtro():

        contador = 0

        while True:

            dados = CoinMarketCap.conexao()
            nome = list(map(lambda dado: dado['name'], dados['data']))
            siglas = list(map(lambda sigla: sigla['symbol'], dados['data']))
            preco = list(map(lambda valor: valor['quote']['USD']['price'], dados['data']))

            # Passando preço para real
            preco_real = list()
            for d in preco:
                preco_real.append(d * 5.18)

            # Para arredondar casas decimais
            pd.set_option('display.precision', 2)

            # Para tirar formatação de notação cientifica
            pd.set_option('float_format', '{:.3f}'.format)

            df = pd.DataFrame({
                'Criptomoeda': nome,
                'Sigla': siglas,
                'Preço Atual R$': preco_real
            })

            filtro = df.query('Sigla == "BTC"')

            lista = list()

            for query in filtro.values:
                lista.append(query)

            texto = f'{lista[0][0]} - {lista[0][1]} - R${lista[0][2]:.3f}'

            if filtro['Preço Atual R$'].values <= 100500:
                contador += 1
                #print(contador)
                #sleep(100)
                if contador >= 3:
                    print(texto)
                    envia_email(texto)
                    break
            sleep(2)




