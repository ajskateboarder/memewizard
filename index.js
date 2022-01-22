const axios = require('axios')
const prompt = require('prompt-sync')
const { closestMatch } = require('closest-match')
const fs = require('fs')

console.log( '\x1b[32m\x1b[1m', 
` 
+--------------------------------------------------------------------------+
| ███   ███   ███████   ███   ███   ███████          ███████   ██       ██ |
| ████ ████   ██        ████ ████   ██               ██        ██       ██ |
| ██ ███ ██   ███████   ██ ███ ██   ███████   █████  ██        ██       ██ |
| ██     ██   ██        ██     ██   ██               ██        ██       ██ |
| ██     ██   ███████   ██     ██   ███████          ███████   ███████  ██ |
+--------------------------------------------------------------------------+ 
`, 
'\x1b[0m' ) 

var inp = prompt()('\u001b[36;1mEnter a meme > \u001b[0m')
async function fetch() {
    var res = await axios.get('http://192.168.68.116:5000/api/v1/memes/popular/stats')
    var d = res.data['response']
    var names = d.map((c) => { return c['name'] })
    var object = d.reduce(
        (obj, item) => Object.assign(obj, { [item['name']]: [...item['trend'],...item['predict']] } ), {});
    var close = closestMatch(inp, names)

    var y = object[close]
    var doc = await axios.get('https://raw.githubusercontent.com/ajskateboarder/stuff/main/meme.js/document.html')

    fs.promises.writeFile(`${close}.html`, doc.data.replace('/*name*/', close).replace('/*data*/', y.toString()))
}

fetch()