import React, {useState, useEffect} from 'react'
import './css/index.css'
import './css/bulma/bulma.css'
import './css/bulma/bulma.css.map'
import './css/bulma/bulma.min.css'
import './css/bulma/bulma-rtl.css'
import './css/bulma/bulma-rtl.css.map'
import './css/bulma/bulma-rtl.min.css'
import './css/userAccount.css'
import {useLocation} from 'react-router-dom'
import $ from 'jquery';
import axios from "axios";

export default function Profile(){

    console.log('profile lalala')
    const location = useLocation()
    console.log('location: ', location)

    const [first, setFirst] = useState(false)
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [phone, setPhone] = useState('')
    const [email, setEmail] = useState('')
    const [rating, setRating] = useState(5)
    const [hotels, setHotels] = useState([])
    const [count, setCount] = useState(0)
    const [token, setToken] = useState('')

    console.log('token1: ', token)
    console.log('count:' ,count)

//    console.log('count: ', count)
//    setToken(location.state.token)

    useEffect(()=>{
        console.log('username change to: ', username)

    }, [username])

    if(count === 0){
        setCount(1)
        setToken(location.state.token)
        console.log('token2: ', token)
        axios
       .get('http://localhost:8000/accounts/profile/view/',
            {
                headers: {"Authorization": 'Bearer '+location.state.token}
             }
             )
            .then(response => {
                console.log('profile.response', response.data);

                const myUser = response.data.results[0]
                setUsername(myUser.username)
                setPassword(myUser.password)
                setPhone(myUser.phone_number)
                setEmail(myUser.email)
                setRating(myUser.rating)
            }
            )
            .catch(function (error) {
               console.log(error.response)
               if(error.response.status === 401){
                    //unauthorized
                     alert("Unauthorized! Please check your token")
               }
            })

          axios
         .get('http://localhost:8000/hotels/view/',
            {
               headers: {"Authorization": 'Bearer '+location.state.token}
            }
            )
            .then(response=>{
                console.log('get hotels')
                setHotels(response.data.results.slice())

           })
    }

    const updateProfileHandler=(e)=>{

        console.log('99')
        var myUl = $(e.target.closest('ul'))

        const new_username = myUl.find('#username').val()===''?myUl.find('#username').attr('placeholder'):myUl.find('#username').val()
        const new_pwd = myUl.find('#pwd').val()===''?myUl.find('#pwd').attr('placeholder'):myUl.find('#pwd').val()
        const new_phone = myUl.find('#phone').val()===''?myUl.find('#phone').attr('placeholder'):myUl.find('#phone').val()
        const new_email = myUl.find('#email').val()===''?myUl.find('#email').attr('placeholder'):myUl.find('#email').val()

        axios.
        put('http://localhost:8000/accounts/profile/update/',
        {
            username: new_username,
            password: new_pwd,
            phone_number: new_phone,
            email: new_email
        },
        {headers: {
            'Authorization': 'Bearer '+location.state.token
        }}).then(response=>{
            console.log('117', response.data)

        })

    }

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
                       headers: {"Authorization": 'Bearer '+location.state.token}
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


    return <main class="userAccount">
      <div className="aboutMe">
        <p>About Me</p>
        <div className="personalInfo">
            <div className="portrait"></div>
            <ul className="info">
                <li><label for='username'>User Name: </label></li><input id='username' placeholder={username}/>
                <li><label for='pwd'>Password: </label></li><input id='pwd' placeholder={password}/>
                <li><label for='phone'>Phone: </label></li><input id='phone' placeholder={phone}/>
                <li><label for='email'>Email: </label></li><input id='email' placeholder={email}/>
                <li><label for='rating'>Rating: </label></li><input id='rating' placeholder={rating}/>
                <li><button onClick={updateProfileHandler}>Update Profile</button></li>
            </ul>
        </div>
      </div>
      <div className="myRenting">
          <ul>
              <li><span className="title">Where I booked</span></li>
          </ul>
          <div className="rentingInfo">
          </div>
      </div>
      <div class="myProperty">
            <ul>
              <li><span className="title">My Properties</span></li>
           </ul>
      <div className="rentingInfo">
            <ul>
                {
                  hotels.map((value, index)=>{
                    const hotel_id = 'hotel_' + value.id
                      return <form key={index} id={hotel_id} action=''>
                                <label for={hotel_id+'name'}>name: </label><input id={hotel_id+'name'} placeholder={value.name}/>
                                <label for={hotel_id+'addr'}>address: </label><input id={hotel_id+'addr'} placeholder={value.address} />
                                <label for={hotel_id+'cap'}>capacity: </label><input id={hotel_id+'cap'} placeholder={value.capacity} />
                                <label for={hotel_id+'beds'}>beds: </label><input id={hotel_id+'beds'} placeholder={value.beds} />
                                <label for={hotel_id+'baths'}>baths: </label><input id={hotel_id+'baths'}  placeholder={value.baths}/>
                                <button onClick={updateHotelHandler}>update</button>
                                <p className='hotel_update_err'></p>
                            </form>
                  })
                }
            </ul>
      </div>
      </div>
    </main>

}