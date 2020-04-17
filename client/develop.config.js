const path = require('path');

module.exports = {
    mode: 'production',
    entry: path.resolve(__dirname, path.join('.\\','src', 'index')),
    output: {
        path: path.resolve(__dirname, path.join('..\\','docs', 'docs', 'js')),
        library: 'fsl'
    },
    module: {
        rules: [
            {
                test: /\.css$/i,
                use: ['style-loader', 'css-loader'],
            },
        ],
    },
}