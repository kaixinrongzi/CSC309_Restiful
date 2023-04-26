import axios from 'axios'
import $ from 'jquery';
import './css/comment.css'
import {useLocation, useNavigate} from 'react-router-dom'
import React, {useState} from 'react'
import {getToken} from './store/tokenGetter'
import {useDispatch, useSelector} from 'react-redux'
import './css/userAccount.css'


export default function ReplyAdd(){

//    const token = useSelector(state=>state.token.token)
    const token = localStorage.getItem('token')
    const location = useLocation()
    const object_id = location.state?location.state.object_id:''
    const reply_to = location.state?location.state.reply_to:''

    const replyHandler=(e)=>{

        const detail = $(e.target.closest('div')).find('#object_id').val()

        const reply_to_type = reply_to==='comment'?11:12

        axios.
        post('http://localhost:8000/hotels/reply/add/',
            {
                reply_to: reply_to_type,
                object_id: object_id,
                detail: detail
            },
            {
                headers: {"Authorization": 'Bearer '+ token}
            }
        ).then(response=>{
            console.log(response.data)
            var reply_info = ''
            response.data.map((value, index)=>{
                reply_info += value + ' '
            })
            $('.reply_info').html(reply_info)
        }).catch(error=>{
            console.log(error.response)
        })

    }


    return <main>
        <div className='reply'>
            <label for='object_id'>Object ID: </label>
            <input id='object_id' value={object_id}/>
            <label for='detail'>Detail: </label>
            <input id='detail'/>
            <button onClick={replyHandler}>Reply</button>
            <p className='reply_info'></p>
        </div>
        </main>



}