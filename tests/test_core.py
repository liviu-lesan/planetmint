# Copyright © 2020 Interplanetary Database Association e.V.,
# Planetmint and IPDB software contributors.
# SPDX-License-Identifier: (Apache-2.0 AND CC-BY-4.0)
# Code is Apache-2.0 and docs are CC-BY-4.0

import pytest


@pytest.fixture
def config(request, monkeypatch):
    backend = request.config.getoption('--database-backend')
    if backend == 'mongodb-ssl':
        backend = 'mongodb'

    config = {
        'database': {
            'backend': backend,
            'host': 'localhost',
            'port': 3303,
            'name': 'bigchain',
            'replicaset': 'bigchain-rs',
            'connection_timeout': 5000,
            'max_tries': 3,
            'name':'bigchain'
        },
        'tendermint': {
            'host': 'localhost',
            'port': 26657,
        },
        'CONFIGURED': True,
    }

    monkeypatch.setattr('planetmint.config', config)

    return config


def test_bigchain_class_default_initialization(config):
    from planetmint import Planetmint
    from planetmint.validation import BaseValidationRules
    from planetmint.backend.tarantool.connection import TarantoolDB
    planet = Planetmint()
    #assert isinstance(planet.connection, TarantoolDB)
    assert planet.connection.host == config['database']['host']
    assert planet.connection.port == config['database']['port']
    #assert planet.connection.dbname == config['database']['name']
    assert planet.validation == BaseValidationRules


def test_bigchain_class_initialization_with_parameters():
    from planetmint import Planetmint
    from planetmint.backend import Connection
    from planetmint.validation import BaseValidationRules
    init_db_kwargs = {
        'backend': 'localmongodb',
        'host': 'this_is_the_db_host',
        'port': 12345,
        'name': 'this_is_the_db_name',
    }
    connection = Connection(**init_db_kwargs)
    planet = Planetmint(connection=connection)
    assert planet.connection == connection
    assert planet.connection.host == init_db_kwargs['host']
    assert planet.connection.port == init_db_kwargs['port']
    # assert planet.connection.name == init_db_kwargs['name']
    assert planet.validation == BaseValidationRules


@pytest.mark.bdb
def test_get_spent_issue_1271(b, alice, bob, carol):
    from planetmint.models import Transaction

    tx_1 = Transaction.create(
        [carol.public_key],
        [([carol.public_key], 8)],
    ).sign([carol.private_key])
    print( f" TX 1 : {tx_1} ")
    print( f" TX 1 ID : {tx_1.id} ")
    assert tx_1.validate(b)
    b.store_bulk_transactions([tx_1])

    tx_2 = Transaction.transfer(
        tx_1.to_inputs(),
        [([bob.public_key], 2),
         ([alice.public_key], 2),
         ([carol.public_key], 4)],
        asset_id=tx_1.id,
    ).sign([carol.private_key])
    print( f" TX 2 : {tx_2} ")
    print( f" TX 2 ID : {tx_2.id} ")
    assert tx_2.validate(b)
    b.store_bulk_transactions([tx_2])

    tx_3 = Transaction.transfer(
        tx_2.to_inputs()[2:3],
        [([alice.public_key], 1),
         ([carol.public_key], 3)],
        asset_id=tx_1.id,
    ).sign([carol.private_key])
    print(f"TX 3 : {tx_3} ")
    print(f"TX 3 ID : {tx_3.id} ")
    assert tx_3.validate(b)
    b.store_bulk_transactions([tx_3])

    tx_4 = Transaction.transfer(
        tx_2.to_inputs()[1:2] + tx_3.to_inputs()[0:1],
        [([bob.public_key], 3)],
        asset_id=tx_1.id,
    ).sign([alice.private_key])
    assert tx_4.validate(b)
    b.store_bulk_transactions([tx_4])

    tx_5 = Transaction.transfer(
        tx_2.to_inputs()[0:1],
        [([alice.public_key], 2)],
        asset_id=tx_1.id,
    ).sign([bob.private_key])
    assert tx_5.validate(b)

    b.store_bulk_transactions([tx_5])
    assert b.get_spent(tx_2.id, 0) == tx_5
    assert not b.get_spent(tx_5.id, 0)
    assert b.get_outputs_filtered(alice.public_key)
    assert b.get_outputs_filtered(alice.public_key, spent=False)
