require('dotenv').config();
const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const mongoose = require('mongoose');
const bcrypt = require('bcrypt');
const User = require('./database/User');
const PreRegistration = require('./database/preRegistration');
const promClient = require('prom-client'); 

const { userdb } = require('./db');

const app = express();
const port = process.env.PORT || 3000;

// Middleware
app.use(bodyParser.json());
app.use(cors({
  origin: 'http://project-frontend:8080', 
  methods: 'GET,HEAD,PUT,PATCH,POST,DELETE',
  credentials: true,
  allowedHeaders: ['Content-Type', 'Authorization']
}));

// Prometheus 指标
const register = promClient.register;
const counter = new promClient.Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'status']
});

app.use((req, res, next) => {
  res.on('finish', () => {
    counter.inc({ method: req.method, status: res.statusCode });
  });
  next();
});

// Health check endpoint
app.get('/healthz', (req, res) => {
  res.send('OK');
});

// Readiness check endpoint
app.get('/readiness', (req, res) => {
  res.send('OK');
});

// 定义 createUserIfNotExists 函数
async function createUserIfNotExists(phone, password, name, gender, age, idCard) {
  try {
    const existingUser = await User.findOne({ phone });
    if (!existingUser) {
      const newUser = new User({
        _id: new mongoose.Types.ObjectId(),
        name,
        gender,
        age,
        phone,
        idCard,
        password, 
        medicalHistory: '',
      });
      await newUser.save();
      console.log('User created:', phone);
    } else {
      console.log('User already exists:', phone);
    }
  } catch (error) {
    console.error('Error creating user:', error);
    throw error;  
  }
}

// 创建默认用户的函数
async function createDefaultUser() {
  try {
    const phone = '12312312312';
    const password = '123123123';
    const name = 'Default User';
    const gender = 'Male';
    const age = 30;
    const idCard = '123456789012345678';
    await createUserIfNotExists(phone, password, name, gender, age, idCard);
  } catch (error) {
    console.error('Error creating default user:', error);
  }
}

// 使用 db.js 文件中的 userdb 进行数据库连接
userdb.on('connected', async () => {
  console.log('Connected to user database');

  createDefaultUser(); // 创建默认用户
});

userdb.on('error', (err) => {
  console.error('Failed to connect to user database:', err);
});

// API endpoint to check phone
app.post('/api/check-phone', async (req, res) => {
  try {
    const { phone } = req.body;
    const user = await User.findOne({ phone });
    res.send({ exists: !!user });
  } catch (error) {
    console.error('Error checking phone:', error);
    res.status(500).send('Server error');
  }
});

// API endpoint to check ID number
app.post('/api/check-id', async (req, res) => {
  try {
    const { idNumber } = req.body;
    const user = await User.findOne({ idCard: idNumber });
    res.send({ exists: !!user });
  } catch (error) {
    console.error('Error checking ID:', error);
    res.status(500).send('Server error');
  }
});

// API endpoint to register user
app.post('/api/register', async (req, res) => {
  try {
    const { name, phone, password, idNumber, gender, age } = req.body;
    await createUserIfNotExists(phone, password, name, gender, age, idNumber);
    res.send({ success: true });
  } catch (error) {
    console.error('Error registering user:', error);
    res.status(500).send({ success: false, message: 'Server error' });
  }
});

// 登录接口
app.post('/api/login', async (req, res) => {
  try {
    const { phone, password } = req.body;
    const user = await User.findOne({ phone });
    if (user) {
      const isPasswordCorrect = await bcrypt.compare(password, user.password);
      console.log('Password correct:', isPasswordCorrect); 
      if (isPasswordCorrect) {
        res.send({ success: true });
      } else {
        res.send({ success: false });
      }
    } else {
      res.send({ success: false });
    }
  } catch (error) {
    console.error('Error logging in:', error);
    res.status(500).send('Server error');
  }
});

// 获取用户信息接口
app.get('/api/user/:phone', async (req, res) => {
  try {
    const { phone } = req.params;
    const user = await User.findOne({ phone }).lean();
    if (user) {
      const userInfo = {
        ...user,
        idNumber: user.idCard
      };
      delete userInfo.idCard;
      res.send({ success: true, data: userInfo });
    } else {
      res.send({ success: false, message: 'User not found' });
    }
  } catch (error) {
    console.error('Error fetching user info:', error);
    res.status(500).send({ success: false, message: 'Server error' });
  }
});

app.put('/api/user/:phone', async (req, res) => {
  try {
    const { phone } = req.params;
    const updateData = req.body; // Expecting the body to contain the field(s) to be updated

    // Validate the incoming data here if necessary
    if (!updateData || Object.keys(updateData).length === 0) {
      return res.status(400).send({ success: false, message: 'No update data provided' });
    }

    const user = await User.findOneAndUpdate({ phone }, updateData, { new: true }).lean();
    if (user) {
      const updatedUserInfo = {
        ...user,
        idNumber: user.idCard
      };
      delete updatedUserInfo.idCard;
      res.send({ success: true, data: updatedUserInfo });
    } else {
      res.send({ success: false, message: 'User not found' });
    }
  } catch (error) {
    console.error('Error updating user info:', error);
    res.status(500).send({ success: false, message: 'Server error' });
  }
});

// Prometheus metrics endpoint
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
});

// 启动服务器
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
}).on('error', (err) => {
  if (err.code === 'EADDRINUSE') {
    console.error(`Port ${port} is already in use, trying another port...`);
    app.listen(0, () => {
      console.log(`Server is running on port ${app.address().port}`);
    });
  } else {
    console.error(err);
  }
});

