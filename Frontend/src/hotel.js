import {useDispatch, useSelector} from 'react-redux'
import {useNavigate} from 'react-router-dom'
import {getToken} from './store/tokenGetter'
import $ from 'jquery'
import axios from 'axios'
import React, {useState, useEffect} from 'react'
import './css/userAccount.css'

export default function Hotels(){

        const navigate = useNavigate()
//        const token = useSelector(state=>state.token.token)
        const token = localStorage.getItem('token')
        console.log('hotel 8: ', token)

        const [hotels, setHotels] = useState([])
        const [hotelCounts, setHotelCounts] = useState(0)
        const [addHotelCount, setAddHotelCount] = useState(0)
        const [currentPage, setCurrentPage] = useState(1)

        const updateHotelHandler=(e)=>{

           e.preventDefault()

           var myForm = e.target.closest('form')
           const hotel_id = myForm.id.slice(myForm.id.indexOf('_') + 1,)

           const hotel_new_name = $('#hotel_'+hotel_id+'name').val()===''?$('#hotel_'+hotel_id+'name').attr('placeholder'):$('#hotel_'+hotel_id+'name').val()
           const hotel_new_addr = $('#hotel_'+hotel_id+'addr').val()===''?$('#hotel_'+hotel_id+'addr').attr('placeholder'):$('#hotel_'+hotel_id+'addr').val()
           const hotel_new_cap = $('#hotel_'+hotel_id+'cap').val()===''?$('#hotel_'+hotel_id+'cap').attr('placeholder'):$('#hotel_'+hotel_id+'cap').val()
           const hotel_new_beds = $('#hotel_'+hotel_id+'beds').val()===''?$('#hotel_'+hotel_id+'beds').attr('placeholder'):$('#hotel_'+hotel_id+'beds').val()
           const hotel_new_baths = $('#hotel_'+hotel_id+'baths').val()===''?$('#hotel_'+hotel_id+'baths').attr('placeholder'):$('#hotel_'+hotel_id+'baths').val()

           axios
              .put('http://localhost:8000/hotels/' + hotel_id + '/update/',
                  {
                    name: hotel_new_name,
                    address: hotel_new_addr,
                    capacity: hotel_new_cap,
                    beds: hotel_new_beds,
                    baths: hotel_new_baths,
                    },
                    {headers:
                        {"Authorization": 'Bearer '+token}
                    }
                   ).then(response=>{
                    console.log(response)
                    $('#' + myForm.id + ' .hotel_update_err').html('updated successfully!')

                    axios
                     .get('http://localhost:8000/hotels/view/',
                        {
                           headers: {"Authorization": 'Bearer '+token}
                        }
                        )
                        .then(response=>{
                            console.log('get hotels')
                            setHotels(response.data.results.slice())
                       })
                   })
                   .catch(err=>{
                       const err_info = err.response.data
                       console.log(err_info)
                      if (err.response.data.code==='token_not_valid'){
                         $('#' + myForm.id + ' .hotel_update_err').html('token_not_valid')
                      }else{
                        var err_feedback = []
                        if(err_info.name){
                            err_feedback.push('name: '+err_info.name+'\n')
                        }
                        if(err_info.capacity){
                            err_feedback.push('capacity: '+err_info.capacity+'\n')
                        }
                        if(err_info.beds){
                            err_feedback.push('beds: '+err_info.beds+'\n')
                        }
                        if(err_info.baths){
                            err_feedback.push('baths: '+err_info.baths+'\n')
                        }
                        $('#' + myForm.id + ' .hotel_update_err').html(err_feedback)

                      }

                   })

    }

    useEffect(()=>{
        axios
         .get('http://localhost:8000/hotels/view/',
            {
               headers: {"Authorization": 'Bearer '+ token}
            }
            ).then(response=>{
                console.log('hotel 95: ', response.data)
                setHotels(response.data.results)
                setHotelCounts(response.data.count)
            }).catch(error=>{
                console.log(error.response)
                if(error.response.status===401){
                    alert('Unauthorized! Please Login')
                    navigate('/accounts/login')
                }
            })

    }, [navigate])

    useEffect(()=>{
        axios
         .get('http://localhost:8000/hotels/view/',
            {
               headers: {"Authorization": 'Bearer '+ token},
               params: {'page': currentPage}
            }
            ).then(response=>{
                console.log('hotel 95: ', response.data)
                setHotels(response.data.results)
                setHotelCounts(response.data.count)
            }).catch(error=>{
                console.log(error.response)
                if(error.response.status===401){
                    alert('Unauthorized! Please Login')
                    navigate('/accounts/login')
                }
            })
    }, [currentPage])

     const viewCommentsHandler=(e)=>{
         const hotel_id = e.target.closest('form').id.slice(e.target.closest('form').id.indexOf('_')+1)
         navigate('/hotels/hotel/comments/view', {state: {hotel_id: hotel_id}, replace: false})
     }


    const viewAvailabilityHandler=(e, hotel_id)=>{
        navigate('/hotels/availability/add', {state: {hotel_id: hotel_id}, replace: false})
    }

    const addHotelHandler=(e)=>{
        if(addHotelCount === 0){
            var myUl = e.target.closest('ul')
            var addHotelDiv =$("<div className='addhotel'>" +
                "<label for='newHotelName'>Hotel Name: </label>" +
                "<input id='newHotelName'></input><br/>" +
                "<label for='newHotelAddr'>Hotel Address: </label>" +
                "<input id='newHotelAddr'></input><br/>" +
                "<label for='newHotelDes'>Hotel Description: </label>" +
                "<input id='newHotelDes'></input><br/>" +
                "<label for='newHotelCap'>Hotel Capacity: </label>" +
                "<input id='newHotelCap'></input><br/>" +
                "<label for='newHotelBeds'>Hotel Beds: </label>" +
                "<input id='newHotelBeds'></input><br/>" +
                "<label for='newHotelBaths'>Hotel Baths: </label>" +
                "<input id='newHotelBaths'></input><br/>" +
                "<button>Add</button>" +
            "</div>")
            $(addHotelDiv).find('button').click(function(e){
                console.log('hotel 135: ', localStorage.getItem('user_id'))
                var myDiv = e.target.closest('div')
                axios.post('http://localhost:8000/hotels/add/',
                        {name: $(myDiv).find('#newHotelName').val(),
                         description: $(myDiv).find('#newHotelDesc').val(),
                         address: $(myDiv).find('#newHotelAddr').val(),
                         capacity: $(myDiv).find('#newHotelCap').val(),
                         beds: $(myDiv).find('#newHotelBeds').val(),
                         baths: $(myDiv).find('#newHotelBaths').val(),
                         owner: localStorage.getItem('user')
                        },
                        {headers: {"Authorization": 'Bearer '+ token}}
                        ).then(response=>{
                            console.log(response.data)
                        }).catch(error=>{
                            console.log(error.response)
                        })
                        })
                        $(myUl).append(addHotelDiv)

                        setAddHotelCount(1)
        }
    }

    const previousPageHandler=()=>{
        if(currentPage > 1){
            setCurrentPage(currentPage - 1)
        }
    }

    const nextPageHandler=()=>{
        if(currentPage < Math.ceil(hotelCounts / 5)){
            setCurrentPage(currentPage + 1)
        }
    }


        return <div className="myProperty">
            <ul>
                <li><span className="title">My Properties</span></li>
                {
                  hotels.map((value, index)=>{
                    const hotel_id = 'hotel_' + value.id
//                    return <li key={index} id={hotel_id}><b>Name:</b> {value.name} - <b>Address:</b> {value.address} - <b>Rating:</b> {value.rating} <button onClick={updateHandler}>Edit</button></li>
                      return <form key={index} id={hotel_id} action=''>
                                <label for={hotel_id+'name'}>name: </label><input id={hotel_id+'name'} placeholder={value.name}/>
                                <label for={hotel_id+'addr'}>address: </label><input id={hotel_id+'addr'} placeholder={value.address} /><br/>
                                <label for={hotel_id+'cap'}>capacity: </label><input id={hotel_id+'cap'} placeholder={value.capacity} />
                                <label for={hotel_id+'beds'}>beds: </label><input id={hotel_id+'beds'} placeholder={value.beds} /><br/>
                                <label for={hotel_id+'baths'}>baths: </label><input id={hotel_id+'baths'}  placeholder={value.baths}/>
                                <button onClick={updateHotelHandler}>update</button><br/>
                                <button onClick={e=>viewAvailabilityHandler(e, value.id)}> View Availabilities </button><br/><br/>
                                <button onClick={viewCommentsHandler}>View Comments</button><br/><br/>
                                <p className='hotel_update_err'></p>
                            </form>
                  })
                }
                <li><button onClick={ addHotelHandler }>Add Hotel</button></li>
            </ul>
            <ul className='pagesHandler'>
                <li><button onClick={previousPageHandler}>Previous Page</button></li>
                <li>Current Page: {currentPage}</li>
                <li><button onClick={nextPageHandler}>Next Page</button></li>
            </ul>
      </div>
    }

