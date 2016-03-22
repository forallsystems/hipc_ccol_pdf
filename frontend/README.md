
To install React and React DOM:

$ npm install --save react react-dom babelify babel-preset-react
$ browserify -t [ babelify --presets [ react ] ] main.js -o bundle.js


To install react-select:

$ npm install react-select --save

Install browserify:

$ sudo npm install -g browserify

Build library bundle:

$ browserify -t [ babelify --presets [ react ] ] -r react -r react-dom -r react-select -o libraries.js
