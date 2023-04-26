const myExpress = require('express')
const myApp = myExpress()

myApp.get('/api/user', (req, res)=>{
    res.send({
        msg: '来自server的消息'
    })
})

myApp.listen(8000, ()=>{
    console.log('server正在监听8000port')
})