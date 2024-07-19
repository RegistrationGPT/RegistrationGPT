<template>
  <div id="app" class="container-fluid" @paste="handlePaste">
    <div class="row no-gutters">
      <div v-if="!leftLayoutVisible" class="toggle-icon" @click="btnDisplayIcon">
        <i class="fas fa-chevron-right"></i>
      </div>
      <div class="left_layout" v-show="leftLayoutVisible">
        <div class="toggle-icon" @click="btnIcon">
          <i class="fas fa-chevron-left"></i>
        </div>
        <div class="profile">
          <div class="profile-img">{{ initials }}</div>
          <div class="profile-name">{{ username }}</div>
        </div>
        <div class="new-chat btn btn-primary my-3" @click="refreshChat">Refresh</div>
      </div>
      <div :class="['right_layout', { 'col-md-12': !leftLayoutVisible }]">
        <div class="chat-header">
          <div class="datetime">{{ datetime }}</div>
          <button class="back-button" @click="goToDashboard">Back to Dashboard</button>
          <div class="user-img">{{ initials }}</div>
        </div>
        <div class="chat-content" ref="chatContent">
          <div v-for="(msg, index) in messages" :key="index" :class="{'chat-bubble-right': msg.sender === 'user', 'chat-bubble-left': msg.sender === 'ai'}">
            <div v-if="msg.type === 'text'">{{ msg.text }}</div>
            <div v-if="msg.type === 'image-text'">
              <div v-if="msg.text.image" class="image-text-content">
                <img :src="msg.text.image" class="img-thumbnail message-image" @click="viewImage(msg.text.image)" />
              </div>
              <div v-if="msg.text.text">{{ msg.text.text }}</div>
            </div>
          </div>
        </div>
        <div class="chat-input-container">
          <div class="image-upload">
            <label class="upload-label" for="file-upload">
              <i class="fas fa-paperclip"></i>
            </label>
            <input id="file-upload" type="file" accept="image/*" @change="onFileChange" class="form-control" style="display:none;">
          </div>
          <div class="input-with-image">
            <div v-if="image" class="uploaded-preview">
              <img :src="image" class="preview-image">
              <span v-if="image" class="remove-image" @click="removeImage">&times;</span>
            </div>
            <textarea ref="messageInput" class="form-control ipt" placeholder="Type your message here..." v-model="message" @keyup.enter="sendMessage" :disabled="isWaitingForResponse" rows="1" @input="adjustTextAreaHeight"></textarea>
          </div>
          <button class="btn btn-success" @click="sendMessage" :disabled="isWaitingForResponse">Send</button>
        </div>
      </div>
    </div>
    <div v-if="showImageViewer" class="image-viewer">
      <div class="image-viewer-content">
        <button class="close-btn" @click="closeImageViewer">&times;</button>
        <img :src="imageToView" class="img-fluid"/>
      </div>
    </div>
    <div v-if="showNotification" class="notification">
      <p>Please describe the symptoms.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      leftLayoutVisible: true,
      datetime: '',
      message: '',
      image: null,
      imageToView: null,
      showImageViewer: false,
      messages: [],
      isWaitingForResponse: false,
      username: 'Michael Jackson', 
      showNotification: false, 
      user_id: '用户的ID', 
    };
  },
  computed: {
    initials() {
      if (!this.username) return '';
      const nameParts = this.username.split(' ');
      if (nameParts.length < 2) return '';
      const lastName = nameParts[nameParts.length - 1];
      const firstName = nameParts[nameParts.length - 2];
      return firstName[0].toUpperCase() + lastName[0].toUpperCase();
    }
  },
  methods: {
    // 隐藏左侧栏
    btnIcon() {
      this.leftLayoutVisible = false;
    },
    // 显示左侧栏
    btnDisplayIcon() {
      this.leftLayoutVisible = true;
    },
    // 补零函数
    isZero(num) {
      return (num < 10 ? '0' : '') + num;
    },
    // 更新时间
    updateDateTime() {
      const datetime = new Date();
      const year = datetime.getFullYear();
      const month = this.isZero(datetime.getMonth() + 1);
      const day = this.isZero(datetime.getDate());
      const hour = this.isZero(datetime.getHours());
      const minute = this.isZero(datetime.getMinutes());
      const seconds = this.isZero(datetime.getSeconds());
      this.datetime = `${year}/${month}/${day} ${hour}:${minute}:${seconds}`;
    },
    // 发送消息
    sendMessage() {
      if (this.image && this.message.trim() === '') {
        this.showTemporaryNotification(); // 仅有图片且无文字时显示提示
        return;
      }
      if (this.message.trim() !== '' || this.image) {
        this.isWaitingForResponse = true; // 设置等待响应状态
        const messagePayload = {
          sender: 'user',
          text: this.image ? { text: this.message, image: this.image } : this.message,
          type: this.image ? 'image-text' : 'text'
        };
        this.messages.push(messagePayload);
        this.callApi(this.messages); // 调用API接口，发送所有消息记录
        this.message = '';
        this.image = null; // 清除图片
        this.scrollToBottom();
        this.resetTextAreaHeight(); // 发送完消息后重置输入框高度
      }
    },
    // 显示临时提示
    showTemporaryNotification() {
      this.showNotification = true;
      setTimeout(() => {
        this.showNotification = false;
      }, 4000); // 提示显示时间稍长
    },
    // 调用API接口
    callApi(messages) {
      axios.post('/python/api/process', { conversation_history: messages, user_id: localStorage.getItem('userPhone') })
        .then(response => {
          const aiResponse = response.data;
          this.messages.push({ sender: 'ai', text: aiResponse.processed_text, type: 'text' });
          this.isWaitingForResponse = false; // 取消等待响应状态
          this.scrollToBottom();
          this.focusMessageInput(); // 将光标移动到输入框中
        }).catch(error => {
          console.error('Error calling API:', error);
          this.isWaitingForResponse = false; // 取消等待响应状态
        });
    },
    // 文件选择事件
    onFileChange(e) {
      const file = e.target.files[0];
      if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.image = e.target.result;
          this.focusMessageInput(); 
        };
        reader.readAsDataURL(file);
      } else {
        console.log('No image file selected or file type is incorrect'); 
      }
    },
    // 粘贴事件
    handlePaste(event) {
      const items = (event.clipboardData || event.originalEvent.clipboardData).items;
      for (const item of items) {
        if (item.kind === 'file' && item.type.startsWith('image/')) {
          const blob = item.getAsFile();
          const reader = new FileReader();
          reader.onload = (e) => {
            console.log('Image pasted:', e.target.result); 
            this.image = e.target.result;
            this.focusMessageInput(); 
          };
          reader.readAsDataURL(blob);
        } else {
          console.log('No image file pasted or file type is incorrect'); 
        }
      }
    },
    // 移除图片
    removeImage() {
      console.log('Image removed'); 
      this.image = null;
    },
    // 查看图片
    viewImage(image) {
      this.imageToView = image;
      this.showImageViewer = true;
    },
    // 关闭图片查看器
    closeImageViewer() {
      this.showImageViewer = false;
      this.imageToView = null;
    },
    // 滚动到底部
    scrollToBottom() {
      this.$nextTick(() => {
        const chatContent = this.$refs.chatContent;
        chatContent.scrollTop = chatContent.scrollHeight;
      });
    },
    // 刷新聊天
    refreshChat() {
      window.location.reload();
    },
    // 将光标移动到输入框中
    focusMessageInput() {
      this.$nextTick(() => {
        this.$refs.messageInput.focus();
      });
    },
    // 调整输入框高度
    adjustTextAreaHeight() {
      const textarea = this.$refs.messageInput;
      textarea.style.height = 'auto';
      textarea.style.height = `${textarea.scrollHeight}px`;
    },
    // 重置输入框高度
    resetTextAreaHeight() {
      const textarea = this.$refs.messageInput;
      textarea.style.height = 'auto';
    },
    // 返回到Dashboard
    goToDashboard() {
      this.$router.push({ name: 'DashboardPage' });
    }
  },
  created() {
    const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';
    if (!isLoggedIn) {
      this.$router.push({ name: 'LoginPage' });
    }
  },
  mounted() {
    this.updateDateTime();
    setInterval(this.updateDateTime, 1000);
    this.focusMessageInput(); 
  }
};
</script>

<style scoped>
@import url('https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css');

* {
  margin: 0;
  padding: 0;
  outline: none;
  box-sizing: border-box;
}

body {
  margin: 1vh 20px;
  min-height: 98vh;
  display: flex;
  justify-content: center;
  align-content: center;
  background-color: #2c2f33; 
  font-family: 'Arial', sans-serif;
  color: #ffffff; 
}

.left_layout {
  border-right: 1px solid #444953; 
  padding: 15px;
  background-color: #23272a; 
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  width: 300px;
  flex-shrink: 0;
  border-radius: 10px;
}

.right_layout {
  padding: 15px;
  background-color: #23272a; 
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  height: 100vh;
  flex-grow: 1;
  border-radius: 10px;
}

.profile {
  text-align: center;
  margin-bottom: 20px;
}

.profile-img {
  width: 60px;
  height: 60px;
  background-color: #7289da; 
  color: #fff;
  font-size: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  margin: 0 auto;
}

.profile-name {
  margin-top: 10px;
  font-weight: bold;
}

.new-chat {
  display: block;
  width: 100%;
}

.history {
  margin-top: 20px;
}

.history-item {
  padding: 10px;
  border: 1px solid #7289da; 
  border-radius: 5px;
  margin-bottom: 10px;
  cursor: pointer;
  color: #fff; 
}

.toggle-icon {
  font-size: 24px;
  cursor: pointer;
  margin: 10px;
  color: #52bbdb;
}

.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.datetime {
  font-size: 14px;
  color: #999;
}

.user-img {
  width: 40px;
  height: 40px;
  background-color: #7289da; 
  color: #fff;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.back-button {
  background-color: #e74c3c;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 5px 10px;
  cursor: pointer;
  font-size: 14px;
  margin-left: 10px;
}

.back-button:hover {
  background-color: #c0392b;
}

.chat-content {
  flex: 1;
  overflow-y: auto;
  margin-bottom: 20px;
}

.chat-bubble-right {
  max-width: 80%;
  padding: 15px;
  background-color: #7289da; 
  border-radius: 20px;
  margin-bottom: 10px;
  position: relative;
  clear: both;
  float: right;
  color: #fff; 
}

.chat-bubble-left {
  max-width: 80%;
  padding: 15px;
  background-color: #99aab5; 
  border-radius: 20px;
  margin-bottom: 10px;
  position: relative;
  clear: both;
  float: left;
  color: #000; 
}

.image-text-content {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.message-image {
  width: 200px;
  height: auto;
  cursor: pointer;
}

.chat-input-container {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  background: #23272a; 
  padding: 10px;
  box-shadow: 0 -1px 5px rgba(0, 0, 0, 0.1);
  border-radius: 10px; 
}

.image-upload-container,
.chat-input {
  display: flex;
  align-items: center;
  background-color: #2c2f33; 
  border: 1px solid #444953; 
  border-radius: 10px; 
  padding: 5px;
  flex: 1; 
}

.image-upload {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 50px; 
  height: 50px;
  border-radius: 50%;
  background-color: #f0f0f0;
  margin-right: 10px; 
}

.upload-label {
  font-weight: bold;
  font-size: 14px;
  color: #333;
}

.uploaded-preview {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  position: relative;
  padding-right: 10px; 
}

.preview-image {
  width: auto; 
  height: 100px;
  border-radius: 5px; 
}

.remove-image {
  color: #ff0000;
  cursor: pointer;
  font-size: 18px;
  position: absolute;
  top: -5px;
  right: -5px;
  background: #fff;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-viewer {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.image-viewer-content {
  position: relative;
}

.image-viewer-content img {
  max-width: 90vw;
  max-height: 90vh;
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 24px;
  color: #fff;
  background: none;
  border: none;
  cursor: pointer;
}

.notification {
  position: fixed;
  top: 20px;
  right: 50%;
  transform: translateX(50%);
  background: #ffeb3b;
  padding: 10px 20px;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  z-index: 10000;
  animation: fadeOut 4s forwards; 
}

@keyframes fadeOut {
  0% {
    opacity: 1;
  }
  100% {
    opacity: 0;
    display: none;
  }
}

.btn-success {
  background-color: #4caf50; 
  border-color: #4caf50;
  height: 50px; 
  font-size: 18px; 
  padding: 10px 20px; 
  border-radius: 10px; 
}

textarea.ipt {
  width: 1500px; 
  resize: none; 
  overflow-y: hidden; 
  transition: height 0.2s; 
  font-size: 16px; 
  padding: 10px; 
  color: #fff; 
  background-color: #2c2f33; 
  border: 1px solid #444953; 
  border-radius: 10px; 
}

textarea.ipt:focus {
  outline: none;
  box-shadow: none;
}
</style>


