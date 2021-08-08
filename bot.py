from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)


@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    if 'frase' in incoming_msg:
        # retorne uma citação
        r = requests.get('https://api.quotable.io/random')
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["content"]} ({data["author"]})'
        else:
            quote = 'Não consegui recuperar uma citação neste momento, desculpe.'
        msg.body(quote)
        responded = True
    if 'gato' in incoming_msg or 'gata' in incoming_msg:
        # retorne uma foto de gato
        msg.media('https://cataas.com/cat')
        responded = True
    # Retorne dados de um CEP
    if incoming_msg.isnumeric() and len(incoming_msg) == 8:
        cep = request.values.get('Body', '').lower()
        r = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
        if r.status_code == 200:
            data = r.json()
            cep_return = f'Rua: {data["logradouro"]}\n' + \
                         f'Bairro: {data["bairro"]}\n' + \
                         f'Cidade: {data["localidade"]}\n' + \
                         f'Estado: {data["uf"]}'

        msg.body(str(cep_return))
        responded = True
    if not responded:
        msg.body('Só conheço frases e gatos famosos, desculpe!')
    return str(resp)


if __name__ == '__main__':
    app.run(debug=True)
