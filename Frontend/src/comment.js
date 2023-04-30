import axios from 'axios'
import $ from 'jquery';
import './css/comment.css'
import {useLocation, useNavigate} from 'react-router-dom'
import React, {useState, useEffect} from 'react'
import {getToken} from './store/tokenGetter'
import {getCommentTarget, getObjectId, getCommentId} from './store/commentTarget.js'
import {useDispatch, useSelector} from 'react-redux'
import './css/userAccount.css'

function CommentAdd(){

//    const location = useLocation()
    const navigate = useNavigate()
//    console.log('10', location.state)
//    if(!location.state){
//        navigate('/accounts/login')
//    }
//
//    const token = location.state.token
    useSelector(state=>console.log(state))
//    const token = useSelector(state=>state.token.token)
    const token = localStorage.getItem('token')
    const comment_target = useSelector(state=>state.comment.comment_target)
    const object_id = useSelector(state=>state.comment.object_id)
    console.log('comment 21: ', token)
    console.log('comment 23: ', comment_target)
    console.log('comment 25: ', object_id)


//    const content_type_choice=()=>{
//        if(location.state.comment_target==='hotel'){
//            return <input type="radio" id='hotel' value="Hotel"/>
//        }else{
//            // location.state.comment_target==='resident'
//            console.log('resident')
//            return <input type="radio" id='resident' value="Resident"/>
//        }
//    }

    const comment_target_type=()=>{
//        if(location.state.comment_target==='hotel'){
        if(comment_target ==='hotel'){
//            return <><label for='hotel_or_resident'>Hotel ID: </label><input id='hotel_or_resident' value={location.state.target_id}/></>
             return <><label for='hotel_or_resident'>Hotel ID: </label><input id='hotel_or_resident' value={object_id}/></>
        }else{
            // location.state.comment_target==='resident'
            console.log('resident')
//            return <><label for='hotel_or_resident'>Resident ID: </label><input id='hotel_or_resident' value={location.state.target_id}/></>
            return <><label for='hotel_or_resident'>Resident ID: </label><input id='hotel_or_resident' value={object_id}/></>
        }
    }

    const CommentHandler=()=>{
//        const content_type = location.state.comment_target==='hotel'?7:6
        const content_type = comment_target==='hotel'?7:6
        console.log('comment 57: ', content_type)

        axios.
          post('http://localhost:8000/hotels/comment/add/', {
                content_type: content_type,
                object_id: $('#hotel_or_resident').val(),
                rating: $('#rating').val(),
                detail: $('#detail').val(),
          },
          {
                 headers: {"Authorization": 'Bearer '+ token}
          }).then(response=>{
                console.log(response.data)
                $('#comment_res').html('Commented Successfully! Thank you!')
          }).catch(err=>{
                console.log(err.response)
                if(err.response.status===401){
                    //unauthorized
                     alert("Unauthorized! Please check your token")
                     navigate('/accounts/login')
                }else if(err.response.status===403){
                    if(err.response.data.error){
                        $('#comment_res').html(err.response.data.error)
                    }else{
                        $('#comment_res').html(err.response.data[0] + ' ' + err.response.data[1])
                    }
                }else if(err.response.status===400){
                    var comment_err = ''
                    if(err.response.data.rating){
                        comment_err = comment_err + 'rating: ' + err.response.data.rating
                    }
                    if(err.response.data.detail){
                        comment_err = comment_err + '\ndetail: ' + err.response.data.detail
                    }
                     $('#comment_res').html(comment_err)
                }else{
                    $('#comment_res').html('Unknown Error')
                }

          })

    }

    return <main className='comment'>
             { comment_target_type() }
             <label for='rating'>Rating: </label>
             <input id='rating'/><br/>
             <label for='detail'>Detail: </label>
             <input id='detail'/><br/>
             <button onClick={CommentHandler}>Comment</button>
             <p id='comment_res'></p>
             </main>
}


function CommentView(){
    const location = useLocation()
    const navigate = useNavigate()

//    const token = location.state?location.state.token:''
//    const token = useSelector(state=>state.token.token)
    const token = localStorage.getItem('token')
    const comment_id = location.state?location.state.comment_id:''
    console.log('comment 120: ', comment_id)
//    const comment_id = useSelector(state=>state.comment.comment_id)

    const [comment, setComment] = useState('')
    const [count, setCount] = useState(0)

    if(count===0){
        setCount(1)
        axios
         .get('http://localhost:8000/hotels/commentforme/' + comment_id + '/view/',
            {
               headers: {"Authorization": 'Bearer '+ token}
            }
            ).then(response=>{
                console.log(response.data)
                setComment(response.data)
         }).catch(error=>{
            console.log(error)
            if(error.response.status === 401){
                    //unauthorized
                     alert("Unauthorized! Please check your token")
                     navigate('/accounts/login')
               }
         })
    }

    const commentTarget=()=>{
        console.log(comment.content_type)
        if(parseInt(comment.content_type) === 7){//comment on hotel
            return <b>There is a comment on your hotel {comment.object_id}</b>
        }else if(parseInt(comment.content_type) === 6){
            return <b>There is a comment on you</b>
        }else{
             return <b>Unknown Error</b>
        }
    }

    const replyHandler=()=>{
        console.log('comment 158: ', comment.id)
        navigate('/hotels/reply/add', {state: {object_id: comment.id, reply_to: 'comment'}, replace: false})
    }

   return <main className='comment'>
        { commentTarget() } <br/>
        <b>Rating: </b>{comment.rating} - <b>Detail: </b>{comment.detail} <br/>
        <button onClick={replyHandler}>Reply</button>
   </main>

}


function CommentsView(){

    const navigate = useNavigate()

//    const token = useSelector(state=>state.token.token)
    const token = localStorage.getItem('token')
    const user_id = useSelector(state=>state.user.user_id)
    const user_name = useSelector(state=>state.user.user_name)
    console.log('comment 167: ', user_id + user_name)

    const [comments, setComments] = useState([])
    const [count, setCount] = useState(0)
    const [currentPage, setCurrentPage] = useState(1)
    const [lastPage, setLastPage] = useState(2)
    const [currentPageDisplay, setCurrentPageDisplay] = useState(1)

    useEffect(()=>{
        getComments()
    }, [currentPage])

    function getComments(){
        axios
         .get('http://localhost:8000/hotels/comments/view/',
            {
               headers: {"Authorization": 'Bearer '+ token},
               params: {page: currentPage}
            }
            ).then(response=>{
                console.log(response.data)
                setComments(response.data.results)
                setLastPage(currentPage + 1)
                setCurrentPageDisplay(currentPage)
//                isAuthenticated = true
         }).catch(error=>{
            console.log(error)
            if(error.response.status === 401){
                    //unauthorized
                alert("Unauthorized! Please check your token")
                navigate('/accounts/login')
            }else if(error.response.status === 404){
                setLastPage(currentPage)
            }
         })
    }

    if(count===0){
        setCount(1)
        getComments()
    }

    const conditional_author_name = (author_id)=>{
        if(author_id===user_id){
            return 'myself'
        }else{
            return author_id
        }
    }

    const conditional_receiver_name = (receiver_id)=>{
        if(receiver_id===user_id){
            return 'myself'
        }else{
            return receiver_id
        }
    }

    const conditional_reply=(author_id, object_id)=>{

        if(author_id===user_id){
            return ''
        }else{
            return <button onClick={(e)=>replyHandler(e, object_id)}>Reply</button>
        }

    }

    const replyHandler=(e, comment_id)=>{
        navigate('/hotels/reply/add', {state: {object_id: comment_id, reply_to: 'comment'}, replace: false})
    }

    const previousPageHandler=()=>{
        if(currentPage > 1){
            setCurrentPage(currentPage - 1)
        }
    }

    const nextPageHandler=()=>{
        if(currentPage < lastPage){
            setCurrentPage(currentPage + 1)
        }
    }


   return <main className='comments'>
            <ul>
                {
                    comments.map((value, index)=>{
                        return <li key={index} id={value.id}><b/>Comment Id: {value.id} - <b/>Rating: {value.rating} - <b/>Detail: {value.detail} - <b/>Author: { conditional_author_name(value.author) } - <b/>Receiver: {conditional_receiver_name(value.receiver_id)}{ conditional_reply(value.author, value.id) }</li>
                     })
                }
            </ul>
            <button onClick={previousPageHandler}>Previous Page</button> Current Page: {currentPageDisplay} <button onClick={nextPageHandler}>Next Page</button>
   </main>

}


function CommentsforHotelView(){

    const location = useLocation()
    const navigate = useNavigate()
    const hotel_id = location.state?location.state.hotel_id:''

//    const token = useSelector(state=>state.token.token)
    const token = localStorage.getItem('token')

    const [comments, setComments] = useState([])
    const [count, setCount] = useState(0)
    const [currentPage, setCurrentPage] = useState(1)
    const [lastPage, setLastPage] = useState(2)
    const [currentPageDisplay, setCurrentPageDisplay] = useState(1)

    useEffect(()=>{
        getCommentsforHotel()
    }, [currentPage])

    function getCommentsforHotel(){
        axios.
            get('http://localhost:8000/hotels/hotel/' + hotel_id + '/comments/view/',
                {
                    headers: {"Authorization": 'Bearer '+ token},
                    params: {page: currentPage}
                }
            ).then(response=>{
                console.log(response)
                setComments(response.data.results)
                setLastPage(currentPage+1)
                setCurrentPageDisplay(currentPage)
            }).catch(error=>{
                console.log(error.response)
                if(error.response.status===401){
                    alert('unauthorized! please renew your token!')
                    navigate('/accounts/login')
                }else if(error.response.data===404){
                    setLastPage(currentPage)
                }
            })
    }

//    if(count===0){
//        setCount(1)
//        getCommentsforHotel(1)
//    }


     const replyHandler=(e, comment_id)=>{
        navigate('/hotels/reply/add', {state: {object_id: comment_id, reply_to: 'comment'}, replace: false})
     }

     const previousPageHandler=()=>{
        if(currentPage > 1){
            setCurrentPage(currentPage - 1)
        }
    }

    const nextPageHandler=()=>{
        if(currentPage < lastPage){
            setCurrentPage(currentPage + 1)
        }
    }


    return <main className='comments_for_hotel'>
        <ul>
            {
                comments.map((value, index)=>{
                    return <li key={index} id={value.id}><b/>Comment Id: {value.id} - <b/>Rating: {value.rating} - <b/>Detail: {value.detail} - <b/>Author: { value.author} <button onClick={(e)=>{replyHandler(e, value.id)}}>Reply</button></li>
                })
            }
        </ul>
        <button onClick={previousPageHandler}>Previous Page</button> Current Page: {currentPageDisplay} <button onClick={nextPageHandler}>Next Page</button>
    </main>
}



export {CommentAdd, CommentView, CommentsView, CommentsforHotelView}