class Models:
    orm_types = [
        ["hasOne", "1-1"],
        ["belongsTo", "1-1 reverse ,1-n reverse "],
        ["hasMany", "1-n"],
        ["belongsToMany", "n-n , n-n reverse"]
    ]
    base = {
        "Hotel": {
            "fields": {
                "id": {"type": "unsigned int", "key": True},
                "title": {"type": "str", "default": "'-'"}
            },
            "has_properties": True,
            "has_settings": True,
        },
        "Room": {
            "fields": {
                "id": {"type": "unsigned int", "key": True},
                "title": {"type": "str", "default": "'-'"},
                "description": {"type": "str", "default": "'-'"},
                "content": {"type": "str", "default": "'-'"},
                "floor": {"type": "int", "default": "1"},
                "image": {"type": "int", "default": "0", "relations": [{'type': 'hasOne', 'table': 'images'}]},
                "images": {"type": "str", "extra": ["null"], "default": "'-'",
                           "relations": [{'type': 'belongsToMany', 'table': 'images', 'middle_table': 'room_image'}]},
                "video": {"type": "int", "default": "0", "relations": [{'type': 'hasOne', 'table': 'videos'}]},
                "flash": {"type": "int", "default": "0", "relations": [{'type': 'hasOne', 'table': 'flashes'}]},
                "locked_days": {"type": "str", "default": "'-'"},
                "inactive_days": {"type": "str", "default": "'-'"},
                "price": {"type": "str", "default": "'-'", "relations": [{'type': 'hasMany', 'table': 'room_prices', 'field': 'room'}]},
                "hotel": {"type": "int", "default": "0", "relations": [{'type': 'belongsTo', 'table': 'hotels'}]},
                "available": {"type": "int", "default": "1"}
            },
            "has_properties": True,
            "has_settings": True,
        },
        "User": {
            "fields": {
                "id": {"type": "unsigned int", "key": True},
                "username": {"type": "str", "default": "'-'"},
                "password": {"type": "str", "default": "'-'"},
            },
            "has_properties": True,
            "has_settings": True
        }
    }

    templates = {
        "properties": {
            "title": "{0}_properties",
            "fields": {
                "id": {"type": "unsigned int", "key": True, "extra": ["not null"]},
                "title": {"type": "str", "default": "''"},
                "values": {"type": "str", "default": "''"},
                "default_value": {"type": "str", "default": "''"},
                "input_type": {"type": "str", "default": "''"},
                "actions": {"type": "str", "default": "'-'"},
                "locales": {"type": "str", "default": "'-'"},
                "validation_rules": {"type": "str", "default": "'-'"},
                "filling_rules": {"type": "str", "default": "'-'"},
                "parent": {"type": "unsigned int", "default": "0"},
            },
        },
        "settings": {
            "title": "{0}_settings",
            "fields": {
                "id": {"type": "unsigned int", "key": True, "extra": ["not null"]},
                "title": {"type": "str", "default": "''"},
                "values": {"type": "str", "default": "''"},
                "default_value": {"type": "str", "default": "'-'"},
                "input_type": {"type": "str", "default": "'-'"},
                "actions": {"type": "str", "default": "'-'"},
                "locales": {"type": "str", "default": "'-'"},
                "validation_rules": {"type": "str", "default": "'-'"},
                "filling_rules": {"type": "str", "default": "'-'"},
                "parent": {"type": "unsigned int", "default": "0"},
            },
        },
        "assigned_properties": {
            "title": "{0}_assigned_properties",
            "fields": {
                "id": {"type": "unsigned int", "key": True, "extra": ["not null"]},
                "item": {"type": "unsigned int", "extra": ["not null"]},
                "property": {"type": "unsigned int", "extra": ["not null"]},
                "values": {"type": "str", "default": "''"}
            }
        },
        "assigned_settings": {
            "title": "{0}_assigned_settings",
            "fields": {
                "id": {"type": "unsigned int", "key": True, "extra": ["not null"]},
                "item": {"type": "unsigned int", "extra": ["not null"]},
                "property": {"type": "unsigned int", "extra": ["not null"]},
                "values": {"type": "str", "default": "''"}
            }
        },
        "general_relation": {
            "title": "{0}_{1}",
            "fields": {
                "id": {"type": "unsigned int", "key": True, "extra": ["not null"]},
                "{0}": {"type": "unsigned int", "extra": ["not null"]},
                "{1}": {"type": "unsigned int", "extra": ["not null"]},
            }
        }

    }
