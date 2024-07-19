const mongoose = require('mongoose');
const bcrypt = require('bcrypt');
const { userdb } = require('../db');

// 定义用户模式
const userSchema = new mongoose.Schema({
  _id: mongoose.Schema.Types.ObjectId,  // 主键 ID
  name: { type: String, required: true },
  gender: { type: String, enum: ['Male', 'Female', 'Other'], required: true }, // 性别
  age: { type: Number, required: true, min: 0 },
  phone: { type: String, required: true, match: /^[0-9]{10,15}$/, unique: true }, // 电话
  idCard: { type: String, required: true, unique: true, match: /^[0-9]{18}$/ }, // 身份证
  password: { type: String, required: true }, // 密码
  medicalHistory: { type: String }, // 个人病史
}, { timestamps: true });

// 在保存用户之前对密码进行哈希加密
userSchema.pre('save', async function(next) {
  if (!this.isModified('password')) {
    return next();
  }
  try {
    const salt = await bcrypt.genSalt(10);
    this.password = await bcrypt.hash(this.password, salt);
    next();
  } catch (err) {
    next(err);
  }
});

// 验证密码的方法
userSchema.methods.comparePassword = function(candidatePassword) {
  return bcrypt.compare(candidatePassword, this.password);
};

const User = userdb.model('User', userSchema);

module.exports = User;

