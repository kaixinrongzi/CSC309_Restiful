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

    const [count, setCount] = useState(0)
    const [currentPage, setCurrentPage] = useState(1)
    const [notifications, setNotifications] = useState([])
    const [notifications_error, setNotificationsError] = useState('')
    const [lastPage, setLastPage] = useState(2)
    const [currentPageDisplay, setcurrentPageDisplay] = useState(1)

    useEffect(()=>{
        getNotifications()
    }, [currentPage])

    function getNotifications(){
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
                setLastPage(lastPage + 1)
                setcurrentPageDisplay(currentPage)
            }).catch(error=>{
                console.log(error)
                if(error.response.status===401){
                    //unauthorized
                     alert("Unauthorized! Please check your token")
                     navigate('/accounts/login')
                }else if(error.response.status===404){
                    //page not found
                    setNotificationsError('END')
                    setLastPage(currentPage)
                }
            })
    }

    if(count===0){
        setCount(1)
        getNotifications()
    }

    const NotificationReadHandler=(e, notification)=>{

//        navigate('/hotels/notification/view', { state:
//                                            {token: token,
//                                            notification_id: notification.id,
//                                            comment_id: notification.object_id,
//                                             replace: false }})
        dispatch(getNotificationId({notification_id: notification.id}))
        dispatch(getCommentId({comment_id: notification.object_id}))
        navigate('/hotels/notification/view')

    }


    const previousPageHandler=()=>{
        if(currentPage>1){
            setCurrentPage(currentPage - 1)
        }
    }

    const nextPageHandler=()=>{
        if(currentPage < lastPage){
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
        <button onClick={previousPageHandler}>Previous Page</button>Current Page {  currentPageDisplay } <button onClick={nextPageHandler}>Next Page</button>
        <p className='notifications_error'>{ notifications_error }</p>
    </main>

}

function NotificationView(){
//    const location = useLocation()
    const navigate = useNavigate()
    const dispatch = useDispatch()

    useSelector(state=>console.log('notification 77: ', state))
//    const token = location.state?location.state.token:''
//    const token = useSelector(state=>state.token.token)
    const token = localStorage.getItem('token')
    const notification_id = useSelector(state=>state.notification.notification_id)
//    const notification_id = location.state?location.state.notification_id:''
     const comment_id = useSelector(state=>state.comment.comment_id)
//    const comment_id = location.state?location.state.comment_id:''

    axios.
        get('http://localhost:8000/hotels/notifications/' + notification_id + '/view/',
            {
               headers: {"Authorization": 'Bearer '+ token}
            }
        ).then(response=>{
            console.log(response.data)
//             navigate('/hotels/comment/view', { state:
//                                            {token: token,
//                                            comment_id:comment_id,
//                                             replace: false }})
            navigate('/hotels/comment/view')

        }).catch(error=>{
            console.log(error.response)
        })

}


export {NotificationViewAll, NotificationView}