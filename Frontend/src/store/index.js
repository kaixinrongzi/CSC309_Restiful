import {configureStore} from '@reduxjs/toolkit'
import mytokengetter from './tokenGetter.js'
import mycommentgetter from './commentTarget.js'
import mynotificationgetter from './notification.js'
import myusergetter from './user.js'

const store = configureStore({
    reducer: {
        token: mytokengetter,
        comment: mycommentgetter,
        notification: mynotificationgetter,
        user: myusergetter
    }
})

export {store};