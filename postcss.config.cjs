const autoprefixer = require("autoprefixer");

const config = {
  plugins: [
    autoprefixer,
    require('cssnano')({
      preset: 'default',
    }),
  ],
};

module.exports = config;
