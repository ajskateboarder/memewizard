const axios = require('axios')
const PolynomialRegression = require('ml-regression').PolynomialRegression;
const prompt = require('prompt-sync')
const { closestMatch } = require('closest-match')

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
axios.get('http://localhost:5000/api/v1/memes/popular/stats')
.then(res => {
    var d = res.data['response']
    var names = d.map((c) => { return c['name'] })
    var object = d.reduce(
        (obj, item) => Object.assign(obj, { [item['name']]: item['trend'] } ), {});
    var close = closestMatch(inp, names)

    var y = object[close]
    var x = [...Array(y.length).keys()]

    var regression = new PolynomialRegression(x,y,5)
    var predictions = x.slice(-10).map(c => regression.predict(c+1))

    console.log(y.slice(-10), predictions)
}) 