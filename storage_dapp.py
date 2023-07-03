from dash import Dash, html, callback, clientside_callback, Output, Input, State
import dash_bootstrap_components as dbc
from web3 import Web3
import json


app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG], external_scripts=[{'src': '../static/signerinfo.js', 'type':'module'}])
app.layout = dbc.Container([
    html.H1('Simple Storage Decentralized Application'),
    dbc.Alert(children="", id="tx-alert", is_open=False, duration=3000, style={'width':'50%'}),

    dbc.Input(id="insert-data", placeholder="Type something...", type="text", value="", style={"width": 200}),
    dbc.Button("Submit", id="submit-btn", color='primary', n_clicks=0, className="mb-4"),

    html.H3("Get the latest sentence added to the blockchain:"),
    dbc.Button("Retrieve", id="get-data", color='info', n_clicks=0),
    html.Div(id='placeholder', children=""),

])


clientside_callback(
    """async function (n, value) {
         try {
         await sendTransaction(value);
         } catch (e) { return [false, 'Submit', true, 'Transaction Unsuccessful!', 'danger']; }
         return [false, 'Submit', true, 'Transaction Successful!', 'success']
       }
    """,
    Output("submit-btn", "disabled"),
    Output("submit-btn", "children"),
    Output("tx-alert", "is_open"),
    Output("tx-alert", "children"),
    Output("tx-alert", "color"),
    Input("submit-btn", "n_clicks"),
    State("insert-data", "value"),
    prevent_initial_call=True,
)

@callback(
    Output("submit-btn", "disabled", allow_duplicate=True),
    Output("submit-btn", "children", allow_duplicate=True),
    Input("submit-btn", "n_clicks"),
    prevent_initial_call=True,
)
def access_data(_):
    return True, "Loading..."


@callback(
    Output("placeholder", "children"),
    Input("get-data", "n_clicks"),
    prevent_initial_call=True,
)
def access_data(_):
    # Connect to a node
    quicknode_url = 'https://solitary-solitary-sky.ethereum-sepolia.discover.quiknode.pro/a7db444267edb0b97aeccc9dbc46815151a4f4a1/'
    w3 = Web3(Web3.HTTPProvider(quicknode_url))
    print(w3.is_connected())

    # Create an instance of the smart contract
    abi = json.loads(
        '[{"inputs": [{"internalType": "string","name": "initialSentence","type": "string"}],"stateMutability": "nonpayable","type": "constructor"}, {"inputs": [],"name": "getSentence","outputs": [{"internalType": "string","name": "","type": "string"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "string","name": "newSentence","type": "string"}],"name": "setSentence","outputs": [],"stateMutability": "nonpayable","type": "function"}]')
    address = w3.to_checksum_address('0x711BD4B4f32ca39cbfDd05CA19D063632f4F50B4')
    contract = w3.eth.contract(address=address, abi=abi)

    latest_sentence = contract.functions.getSentence().call()
    return latest_sentence


if __name__ == '__main__':
    app.run(debug=True)
