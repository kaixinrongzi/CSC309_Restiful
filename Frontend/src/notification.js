import React, {useState, useEffect} from 'react'
import {useNavigate, useLocation} from 'react-router-dom'
import $ from 'jquery'
import axios from 'axios'
import './css/notifications.css'
import {useDispatch, useSelector} from 'react-redux'
import {getToken} from './store/tokenGetter'
import {getCommentTarget, getObjectId, getCommentId} from './store/commentTarget.js'
import {getNotificationId} from './store/notification.js'
import './css/userAccount.css'


function NotificationViewAll(){

    console.log('notification lalala')

    const navigate = useNavigate()
    const dispatch = useDispatch()
//    const location = useLocation()
//    const token = location.state?location.state.token:''
//    const token = useSelector(state=>state.token.token)
    const token = localStorage.getItem('token')

    const [notificationCounts, setNotificationCounts] = useState(0)
    const [currentPage, setCurrentPage] = useState(1)
    const [notifications, setNotifications] = useState([])
    const [notifications_error, setNotificationsError] = useState('')

    useEffect(()=>{
        getNotifications(true)
    }, [navigate])

    useEffect(()=>{
        getNotifications(false)
    }, [currentPage])

    function getNotifications(first_time){
//        alert('32')
        axios
         .get('http://localhost:8000/hotels/notifications/view/',
            {
               headers: {"Authorization": 'Bearer '+ token},
               params: {page: currentPage}
            }
            ).then(response=>{
                console.log(response)
                setNotifications(response.data.results.slice())
                setNotificationsError('')
                if(first_time){
                    setNotificationCounts(response.data.count)
                }
            }).catch(error=>{
                console.log(error)
                if(error.response.status===401){
                    //unauthorized
                     alert("Unauthorized! Please check your token")
                     navigate('/accounts/login')
                }else if(error.response.status===404){
                    //page not found
                    setNotificationsError('END')

                }
            })
    }

    const NotificationReadHandler=(e, notification)=>{

//        navigate('/hotels/notification/view', { state:
//                                            {token: token,
//                                            notification_id: notification.id,
//                                            comment_id: notification.object_id,
//                                             replace: false }})
//        dispatch(getNotificationId({notification_id: notification.id}))
//        dispatch(getCommentId({comment_id: notification.object_id}))
        navigate('/hotels/notification/view', {state: {notif_id: notification.id}, replace: false})

    }


    const previousPageHandler=()=>{
        if(currentPage>1){
            setCurrentPage(currentPage - 1)
        }
    }

    const nextPageHandler=()=>{
        if(currentPage < Math.ceil(notificationCounts / 5)){
            setCurrentPage(currentPage + 1)
        }
    }


    return <main className='notifications'>
        <ul>
            {
                notifications.map((value, index)=>{
                    const notif_id = 'notif_'+value.id
                    return <li key={index} id={notif_id}><a onClick={e=>{NotificationReadHandler(e, value)}} target="_blank"> {value.read?'read':'unread'}  {value.date}  {value.message}  {value.content_type}  {value.object_id}</a></li>
                })

            }
        </ul>
        <button onClick={previousPageHandler}>Previous Page</button>Current Page {  currentPage } <button onClick={nextPageHandler}>Next Page</button>
        <p className='notifications_error'>{ notifications_error }</p>
    </main>

}

function NotificationView(){
    const location = useLocation()
    const navigate = useNavigate()
    const dispatch = useDispatch()

//    useSelector(state=>console.log('notification 77: ', state))
    const notification_id = location.state?location.state.notif_id:''
    console.log('notification 118: ', notification_id)
//    const token = useSelector(state=>state.token.token)
    const token = localStorage.getItem('token')
//    const notification_id = useSelector(state=>state.notification.notification_id)
//    const notification_id = location.state?location.state.notification_id:''
//     const comment_id = useSelector(state=>state.comment.comment_id)
//    const comment_id = location.state?location.state.comment_id:''

    useEffect(()=>{
        axios.
        get('http://localhost:8000/hotels/notifications/' + notification_id + '/view/',
            {
               headers: {"Authorization": 'Bearer '+ token}
            }
        ).then(response=>{
            console.log(response.data)
            const notif = response.data.results[0]
            if (parseInt(notif.content_type)===11){
                //notif is caused by a comment
                navigate('/hotels/comment/view', {state: {comment_id: notif.object_id}, replace: false})
            }else if(parseInt(notif.content_type)===8){
                //notif is caused by a reservation
                navigate('/', {state: {comment_id: notif.object_id}, replace: false})
            }else if(parseInt(notif.content_type)===12){
                //notif is caused by a reply
                navigate('/hotels/reply/view', {state: {reply_id: notif.object_id}, replace: false})
            }

        }).catch(error=>{
            console.log(error.response)
        })
    }, [navigate])

}


export {NotificationViewAll, NotificationView}