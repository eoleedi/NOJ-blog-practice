MONGO_USERNAME=${MONGO_USERNAME}
MONGO_PASSWORD=${MONGO_PASSWORD}
MONGO_INITDB_DATABASE=${MONGO_INITDB_DATABASE}

mongo << EOF
db = db.getSiblingDB('${MONGO_INITDB_DATABASE}')
db.createUser(
    {
        user: "$MONGO_USERNAME",
        pwd: "$MONGO_PASSWORD",
        roles: [ "readWrite", "dbAdmin" ]
    }
)
EOF