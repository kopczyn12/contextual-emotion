#!/bin/bash

BACK_PATH=app/backend
FRONT_PATH=app/frontend
ENV_BACK=$BACK_PATH/.env
ENV_FRONT=$FRONT_PATH/.env

if [ -f "$ENV_BACK" ]; then
    echo "$ENV_BACK already exists."
else
    echo 'DATABASE="mongodb+srv://chlip1:9tGqDbS41kGuE8DZ@zsd.vm4ank7.mongodb.net/?retryWrites=true&w=majority"
JWT_SECRET="secretpasswordisgoodpassword"' > $ENV_BACK
    chmod 600 $ENV_BACK
fi
if [ -f "$ENV_FRONT" ]; then
    echo "$ENV_FRONT already exists."
else
    echo 'REACT_APP_SERVER="http://localhost:5000/api/"' > $ENV_FRONT
    chmod 600 $ENV_FRONT
fi

cd $BACK_PATH
npm i
node index &
cd ../..
cd $FRONT_PATH
npm i
npm start
cd ../..
