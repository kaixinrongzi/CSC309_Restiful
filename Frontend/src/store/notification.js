import {createSlice} from '@reduxjs/toolkit'

const notificationGetter = createSlice({
    name: 'notificationGetter',
    initialState: {notification_id: -1},
    reducers: {
        getNotificationId:(state, action)=>{
            state.notification_id = action.payload.notification_id
        }
    }

})

export default notificationGetter.reducer
export const {getNotificationId} = notificationGetter.actions