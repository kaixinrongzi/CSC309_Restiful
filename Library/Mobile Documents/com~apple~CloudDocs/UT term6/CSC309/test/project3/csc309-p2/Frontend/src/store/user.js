import {createSlice} from '@reduxjs/toolkit'

const userGetter = createSlice({
    name: 'userGetter',
    initialState: {user_id: -1, user_name: ''},
    reducers: {
        getUser:(state, action)=>{
            state.user_id = action.payload.user_id
            state.user_name = action.payload.user_name
            alert('user_id: '+ state.user_id)
        }
    }

})

export default userGetter.reducer
export const {getUser} = userGetter.actions