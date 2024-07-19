// db.js
const mongoose = require('mongoose');
const dotenv = require('dotenv');

// 加载 .env 文件中的环境变量
dotenv.config();

// 使用环境变量中的连接字符串
const mongoURI = process.env.MONGO_URI;

const userdb = mongoose.createConnection(mongoURI, { useNewUrlParser: true, useUnifiedTopology: true });
userdb.on('connected', () => {
  console.log('Connected to user database');
});

module.exports = { userdb };


