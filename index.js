
const prompt = require('prompt-sync')
const { exit } = require('process')
const util = require('./memecli.util')

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

var inp = prompt()('\u001b[36;1mEnter a meme (type %all for a popularity pie chart or %exit to exit) > \u001b[0m')
if (inp === '%exit') {
    exit(0)
} else if (inp === '%all') {
    (async()=>util.fetch_popularity())()
} else {
    (async()=>util.fetch_meme(inp))()
}

