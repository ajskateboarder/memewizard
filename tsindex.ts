import axios from 'axios'
import prompt from 'prompt-sync'
import {closestMatch} from 'closest-match'

console.log(
    '\x1b[32m\x1b[1m',
    `
    +--------------------------------------------------------------------------+
    | #       #   # # # #   #       #   # # # #          # # # #   #         # |
    | # #   # #   #         # #   # #   #                #         #         # |
    | #  # #  #   # # # #   #  # #  #   # # # #   # # #  #         #         # |
    | #   #   #   #         #   #   #   #                #         #         # |
    | #       #   # # # #   #       #   # # # #          # # # #   # # # #   # |
    +--------------------------------------------------------------------------+
    `,
    '\x1b[0m'
)

var inp = prompt()('\u001b[36;1mEnter a meme > \u001b[0m')
axios.get('http://localhost:5000/api/v1/memes/popular/stats')
.then(res => {
    var d:object[] = res.data['response']
    var names = d.map((c:any) => { return c['name'] })
    var object = d.reduce(
        (obj:any, item:any) => Object.assign(obj, { [item['name']]: item['trend'] } ), {});
    var close:any = closestMatch(inp, names)
    console.log(close, object[close])
})