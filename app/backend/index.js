const express = require('express')
const app = express()
const bodyParser = require('body-parser')
const cors = require('cors')

const config = require('./config')


//routes
const userRoutes = require('./routes/user.routes');
const modelRoutes = require('./routes/model.routes');
const emotionsRoutes = require('./routes/emotions.routes')
const stableRoutes = require('./routes/stable.routes')

// connect to database
require('./db/mongoose')

//parser
app.use(bodyParser.json());

//fix cors
app.use(cors());

// routes
app.use('/api/user', userRoutes);
app.use('/api/model', modelRoutes);
app.use('/api/emotions/', emotionsRoutes)
app.use('/api/stable/', stableRoutes)

app.get('/', (req, res) => {
  res.send('success.')
})

app.listen(config.port, () => {
  console.log('Serwer slucha...!')
})