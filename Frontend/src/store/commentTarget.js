import {createSlice} from '@reduxjs/toolkit'

const commentTargetGetter = createSlice({
    name: 'commentTargetGetter',
    initialState: {comment_target: '', object_id: -1, comment_id: -1},
    reducers: {
        getCommentTarget:(state, action)=>{
            state.comment_target = action.payload.comment_target
//            alert('state.token is set to' + state.token)
        },
        getObjectId:(state, action)=>{
            state.object_id = action.payload.object_id
        },
        getCommentId:(state, action)=>{
            state.comment_id = action.payload.comment_id
        }
    }

})

export default commentTargetGetter.reducer
export const {getCommentTarget, getObjectId, getCommentId} = commentTargetGetter.actions