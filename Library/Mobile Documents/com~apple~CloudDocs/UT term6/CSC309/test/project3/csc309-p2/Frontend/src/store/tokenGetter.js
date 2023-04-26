import {createSlice} from '@reduxjs/toolkit'

const tokenGetter = createSlice({
    name: 'tokenGetter',
    initialState: {token: ''},
    reducers: {
        getToken:(state, action)=>{
            state.token = action.payload.token
            alert('state.token is set to' + state.token)
        }
    }

})

export default tokenGetter.reducer
export const {getToken} = tokenGetter.actions