
const path = require('path');
const { VueLoaderPlugin } = require('vue-loader');

module.exports = {
    entry: './src/main.ts',
    output: {
        path: path.resolve(__dirname, 'dist'),
        filename: 'bundle.js'
    },
    resolve: {
        extensions: ['.ts', '.js', '.vue', '.json']
    },
    module: {
        rules: [
            {
                test: /\.vue$/,
                loader: 'vue-loader'
            },
            {
                test: /\.ts$/,
                loader: 'ts-loader',
                options: {
                    appendTsSuffixTo: [/\.vue$/]
                }
            },
            {
                test: /\.s?css$/,
                use: [
                    'vue-style-loader',
                    'css-loader',
                    {
                        loader: 'sass-loader',
                        options: {
                            additionalData: `
                                @import "@/styles/_variables.scss";
                            `,
                            sassOptions: {
                                includePaths: [path.resolve(__dirname, 'src/styles')],
                            },
                        },
                    }
                ]
            },
        ]
    },
    resolve: {
        alias: {
            '@': path.resolve(__dirname, 'src'), // Allows using '@' as a shortcut for 'src'
        },
        extensions: ['.js', '.ts', '.vue', '.scss'], // Add any other extensions you need
    },
    plugins: [
        new VueLoaderPlugin()
    ],
    devtool: 'inline-source-map',
    devServer: {
        static: path.resolve(__dirname, 'dist'), // Ensure this points to the correct directory
        compress: true,
        hot: true,
        port: 9000,
        open: true
    }
};
