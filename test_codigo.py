import pytest
from unittest.mock import patch, MagicMock
from servidor import app, connect_db

@pytest.fixture
def client():
    """Cria um cliente de teste para a API."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
@patch("servidor.connect_db")
def testa_resposta(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
    {'id': 2, 'logradouro': 'Price Prairie', 'tipo_logradouro': 'Travessa', 'bairro': 'Colonton', 'cidade': 'North Garyville', 'cep': '93354', 'tipo': 'casa em condominio', 'valor': '260070', 'data_aquisicao': '2021-11-30'},
    {'id': 3, 'logradouro': 'Taylor Ranch', 'tipo_logradouro': 'Avenida', 'bairro': 'West Jennashire', 'cidade': 'Katherinefurt', 'cep': '51116', 'tipo': 'apartamento', 'valor': '815970', 'data_aquisicao': '2020-04-24'}
]
    mock_connect_db.return_value = mock_conn

    reponse=client.get('/')
    assert reponse.status_code == 200
    expected = {'imoveis':[{'id':2, 'logradouro':'Price Prairie', 'tipo_logradouro':'Travessa', 'bairro':'Colonton', 'cidade':'North Garyville', 'cep':'93354', 'tipo':'casa em condominio', 'valor':'260070', 'data_aquisicao':'2021-11-30'
    },
    {'id':3, 'logradouro':'Taylor Ranch', 'tipo_logradouro':'Avenida', 'bairro':'West Jennashire', 'cidade':'Katherinefurt', 'cep':'51116', 'tipo':'apartamento', 'valor':'815970', 'data_aquisicao':'2020-04-24'
    }
    ]}
    assert reponse.json == expected