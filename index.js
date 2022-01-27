
const prompt = require('prompt-sync')
const { exit } = require('process')
const util = require('./memecli.util')
const inquirer = require('inquirer')

console.log( '\x1b[32m\x1b[1m', 
` 
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
  ███   ███   ███████   ███   ███   ███████          ███████   ██       ██ 
  ████ ████   ██        ████ ████   ██               ██        ██       ██ 
  ██ ███ ██   ███████   ██ ███ ██   ███████   █████  ██        ██       ██ 
  ██ ███ ██   ██        ██ ███ ██   ██               ██        ██       ██ 
  ██     ██   ███████   ██     ██   ███████          ███████   ███████  ██ 
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬ 
`, 
'\x1b[0m' );

var opts = ['Fetch all memes and create a pie chart based on popularity', 'Fetch info for a particular meme', 'Exit']
inquirer.prompt([
    {
        name: 'value',
        message: 'What do you want to do?',
        type: 'list',
        choices: opts
    }
]).then(response => {
    switch (response.value) {
        case opts[0]: util.fetch_popularity(); break
        case opts[1]: {
            var inp = prompt()('\x1b[32m?\x1b[0m \x1b[1mEnter a meme > \x1b[0m')
            util.fetch_meme(inp)
            break
        }
        case opts[2]: exit(0)
    }
})
