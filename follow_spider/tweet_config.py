from neomodel import (config, db, StructuredNode, StringProperty, 
DateTimeFormatProperty, StructuredRel, RelationshipTo, RelationshipFrom)
from creds import neoLog, neoPass

# To apply constraints and indexes you must
# make sure to run this command after applying changes:
# $ neomodel_install_labels yourapp.py someapp.models --db bolt://username:password@localhost:7687

# Declare the path configuration for neo4j
# Default option pasted from online
config_URL = f'bolt://{neoLog}:{neoPass}@localhost:7687/{your_db}'

config.DATABASE_URL = config_URL

# Pretty sure this line is redundant
db.set_connection(config_URL)

# Declared relationships on nodes only have to be declared on the start node 
# Relationships:
date_format = "%m-%d-%Y %H:%M:%S"

class twit_rel(StructuredRel):
    initiated = DateTimeFormatProperty(default_now=True, format=date_format)
    last_checked = DateTimeFormatProperty(default_now=True, format=date_format)

# Nodes:

class user_bot(StructuredNode):
    initiated = DateTimeFormatProperty(default_now=True, date_format=date_format)
    last_checked = DateTimeFormatProperty(default_now=True, date_format=date_format)
    twitter_id = StringProperty(unique_index=True, required=True)
    twit_follow = RelationshipFrom('follow_bot', 'FOLLOWS', model=twit_rel)

class follow_bot(StructuredNode):
    initiated = DateTimeFormatProperty(default_now=True, date_format=date_format)
    last_checked = DateTimeFormatProperty(default_now=True, date_format=date_format)
    twitter_id = StringProperty(unique_index=True, required=True)
    twit_follow = RelationshipTo('user_bot', 'FOLLOWS', model=twit_rel)
