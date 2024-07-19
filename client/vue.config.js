module.exports = {
  devServer: {
    proxy: {
      '/python': {
        target: 'http://project_model:5000',
        changeOrigin: true,
      },
      '/api': {
        target: 'http://project_backend:3000',
        changeOrigin: true,
      },
    },
  },
};

