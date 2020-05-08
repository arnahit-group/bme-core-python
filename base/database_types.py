class DataBaseTypes:
    types = {
        "mysql": {
            "int": "INTEGER",
            "str": "VARCHAR(200)",
            "unsigned int": "int(10) UNSIGNED",
        },
        "mssql": {
            "int": "INTEGER",
            "str": "VARCHAR(200)",
            "unsigned int": "UNSIGNED INTEGER",

        },
        "oracle": {
            "int": "INTEGER",
            "str": "VARCHAR(200)",
            "unsigned int": "UNSIGNED INTEGER",

        },
        "sqlite": {
            "int": "INTEGER",
            "str": "VARCHAR(200)",
            "unsigned int": "UNSIGNED INTEGER",

        }

    }
