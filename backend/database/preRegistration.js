const mongoose = require('mongoose');

// 定义预挂号模式
const preRegistrationSchema = new mongoose.Schema({
  userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true }, // 引用用户ID
  existingMedicalHistory: { type: String, required: true }, // 具体的既往病史
  department: { type: String, required: true }, // 应挂号科室
  healthAnalysis: { type: String, required: true }, // 健康状况分析
  mainSymptoms: { type: String, required: true }, // 主要疾病或症状
}, { timestamps: true });

// 创建并导出预挂号模型
const PreRegistration = mongoose.model('PreRegistration', preRegistrationSchema);

module.exports = PreRegistration;
