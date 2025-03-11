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

@patch("servidor.connect_db")
def testa_listar_imovel_por_id(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = {
        'id': 2, 'logradouro': 'Price Prairie', 'tipo_logradouro': 'Travessa', 'bairro': 'Colonton', 'cidade': 'North Garyville', 'cep': '93354', 'tipo': 'casa em condominio', 'valor': '260070', 'data_aquisicao': '2021-11-30'
    }
    mock_connect_db.return_value = mock_conn

    response = client.get('/imoveis/2')
    assert response.status_code == 200
    expected = {'imoveis':{'id':2, 'logradouro':'Price Prairie', 'tipo_logradouro':'Travessa', 'bairro':'Colonton', 'cidade':'North Garyville', 'cep':'93354', 'tipo':'casa em condominio', 'valor':'260070', 'data_aquisicao':'2021-11-30'}}
    assert response.json == expected
@patch("servidor.connect_db")
def testa_adicionar_imovel(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect_db.return_value = mock_conn

    new_property = {
        'logradouro': 'Oak Street',
        'tipo_logradouro': 'Rua',
        'bairro': 'Downtown',
        'cidade': 'Cityville',
        'cep': '12345',
        'tipo': 'casa',
        'valor': '350000',
        'data_aquisicao': '2022-01-15'
    }

    response = client.post('/imoveis', json=new_property)
    assert response.status_code == 201
    assert response.json == new_property

@patch("servidor.connect_db")
def testa_atualizar_imovel(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect_db.return_value = mock_conn

    updated_property = {
        'id': 2,
        'logradouro': 'Updated Street',
        'tipo_logradouro': 'Rua',
        'bairro': 'Updated Neighborhood',
        'cidade': 'Updated City',
        'cep': '54321',
        'tipo': 'apartamento',
        'valor': '500000',
        'data_aquisicao': '2022-02-20'
    }

    response = client.put('/imoveis/2/update', json=updated_property)
    assert response.status_code == 200
@patch("servidor.connect_db")
def testa_remover_imovel(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect_db.return_value = mock_conn

    response = client.delete('/imoveis/2/delete')
    assert response.status_code == 200
    expected = {'message': 'Imóvel removido com sucesso'}
    assert response.json == expected

@patch("servidor.connect_db")
def testa_listar_imoveis_por_tipo(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        {'id': 2, 'logradouro': 'Price Prairie', 'tipo_logradouro': 'Travessa', 'bairro': 'Colonton', 'cidade': 'North Garyville', 'cep': '93354', 'tipo': 'casa em condominio', 'valor': '260070', 'data_aquisicao': '2021-11-30'},
    ]
    mock_connect_db.return_value = mock_conn

    response = client.get('/imoveis/tipo/casa%20em%20condominio')
    assert response.status_code == 200
    expected = {'imoveis': [
        {'id': 2, 'logradouro': 'Price Prairie', 'tipo_logradouro': 'Travessa', 'bairro': 'Colonton', 'cidade': 'North Garyville', 'cep': '93354', 'tipo': 'casa em condominio', 'valor': '260070', 'data_aquisicao': '2021-11-30'}
    ]}
    assert response.json == expected

@patch("servidor.connect_db")
def testa_listar_imoveis_por_cidade(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        {'id': 2, 'logradouro': 'Price Prairie', 'tipo_logradouro': 'Travessa', 'bairro': 'Colonton', 'cidade': 'North Garyville', 'cep': '93354', 'tipo': 'casa em condominio', 'valor': '260070', 'data_aquisicao': '2021-11-30'},
        {'id': 3, 'logradouro': 'Taylor Ranch', 'tipo_logradouro': 'Avenida', 'bairro': 'West Jennashire', 'cidade': 'North Garyville', 'cep': '51116', 'tipo': 'apartamento', 'valor': '815970', 'data_aquisicao': '2020-04-24'}
    ]
    mock_connect_db.return_value = mock_conn

    response = client.get('/imoveis/cidade/North%20Garyville')
    assert response.status_code == 200
    expected = {'imoveis': [
        {'id': 2, 'logradouro': 'Price Prairie', 'tipo_logradouro': 'Travessa', 'bairro': 'Colonton', 'cidade': 'North Garyville', 'cep': '93354', 'tipo': 'casa em condominio', 'valor': '260070', 'data_aquisicao': '2021-11-30'},
        {'id': 3, 'logradouro': 'Taylor Ranch', 'tipo_logradouro': 'Avenida', 'bairro': 'West Jennashire', 'cidade': 'North Garyville', 'cep': '51116', 'tipo': 'apartamento', 'valor': '815970', 'data_aquisicao': '2020-04-24'}
    ]}
    assert response.json == expected