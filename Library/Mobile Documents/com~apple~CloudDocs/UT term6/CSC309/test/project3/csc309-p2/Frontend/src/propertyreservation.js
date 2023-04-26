import {BrowserRouter, NavLink, Routes, Route, useNavigate} from 'react-router-dom'
import {useDispatch, useSelector} from 'react-redux'
import {getToken} from './store/tokenGetter'
import {getCommentTarget, getObjectId} from './store/commentTarget.js'
import React, {useState, useEffect} from 'react'
import axios from 'axios'
import LogIn from './login'
import './css/userAccount.css'


export default function MyPropertyReservations(){

    const [propertyReservations, setPropertyReservations] = useState([])
    const [count, setCount] = useState(0)

//    const token = useSelector(state=>state.token.token)
    const token = localStorage.getItem('token')
    console.log('property reservations 16: ', token)
    const navigate = useNavigate()
    const dispatch = useDispatch()

    if(count===0){
        setCount(1)

        axios
         .get('http://localhost:8000/hotels/reservation/list/',
            {
                headers: {"Authorization": 'Bearer '+ token},
                params: {user_type: 'host'}
            }
            )
            .then(response=>{
                console.log('get property reservations: ', response.data.results)
                setPropertyReservations(response.data.results)

         }).catch(e=>{
            console.log(e)
            if(e.response.status===401){
                alert('unauthorized token')
                navigate('/accounts/login')
            }
         })
    }

    const conditional_comment_for_resident = (booking_state)=>{
        return booking_state==='F'? <button onClick={commentforResidentHandler}>Comment</button>:''
    }

    const commentforResidentHandler=(e)=>{
        const id_start_index = e.target.closest('li').innerHTML.indexOf('resident_id')+13
        const id_end_index = e.target.closest('li').innerHTML.indexOf('start-date')-2
        const target_id = e.target.closest('li').innerHTML.slice(id_start_index, id_end_index)

        dispatch(getObjectId({object_id: target_id}))
        dispatch(getCommentTarget({comment_target: 'resident'}))
        navigate('/hotels/comment/add')
    }


    return <div className="myPropertyReservation">
        <ul>
            <li><span className="title">My Properties Reservation</span></li>
            {
                  propertyReservations.map((value, index)=>{
                    return <li key={index}>
                        hotel_id: {value.hotel}, resident_id: {value.guest}, start-date: {value.start_date}, end-date: {value.end_date}, guest numbers: {value.guests}, state: {value.state}
                        { conditional_comment_for_resident(value.state) }
                    </li>
                  })
                }
        </ul>
      </div>
}

