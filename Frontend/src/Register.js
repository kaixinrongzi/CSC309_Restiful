import React, {useState} from 'react'
import './css/style1.css'
import './css/style2.css'
import './css/index.css'
import './css/bulma/bulma.css'
import './css/bulma/bulma.css.map'
import './css/bulma/bulma.min.css'
import './css/bulma/bulma-rtl.css'
import './css/bulma/bulma-rtl.css.map'
import './css/bulma/bulma-rtl.min.css'
import './css/regLog.css'
import {Navigate} from 'react-router-dom'
import $ from 'jquery';
import axios from "axios";


export default function Register(){

    console.log("registerlalala");

    const [isRegistered, setIsRegistered] = useState(false)
    const [username_error, setUsernameError] = useState("")
    const [pwd_error, setPwdError] = useState("")
    const [phone_error, setPhoneError] = useState("")
    const [email_error, setEmailError] = useState("")

    const registerHandler = (e)=>{
        e.preventDefault()
        var myForm = $(e.target.closest('form'))
        console.log(myForm)
        axios
            .post('http://localhost:8000/accounts/register/', {
                // Data to be sent to the server
                username: myForm.find('#username').val(),
                password: myForm.find('#pwd').val(),
                phone_number: myForm.find('#phone_num').val(),
                email: myForm.find('#email').val(),
            })
            .then(response => {
                console.log(response.data);

                alert("You Registered Successfully!")
                setIsRegistered(true)

            })
            .catch(function (error) {
                console.log(error.response)
                console.log(error.response.data.username)

                if(error.response.status === 400){

                    const username_error_info = 'username' in error.response.data? 'username: '+ error.response.data.username : ''
                    const pwd_error_info = 'password' in error.response.data? 'password: ' + error.response.data.password : ''
                    const phone_error_info = 'phone_number' in error.response.data? 'phone_number: ' + error.response.data.phone_number : ''
                    const email_error_info = 'email' in error.response.data? 'email: ' + error.response.data.email : ''

                    setUsernameError(username_error_info)
                    setPwdError(pwd_error_info)
                    setPhoneError(phone_error_info)
                    setEmailError(email_error_info)

                }
            })

   }

    if(!isRegistered){
        return <div className='register_overall'>
        <div className="loginOverlay">
                        <a href="/login"><button class="btn" id="logIn">Log In</button></a>
            </div>
            <div className="register">
                        <form className="form" id="form2" >
                            <h2 className="form__title">Register</h2>
                            <input type="text" placeholder="UserName" className="input" id="username"></input>
                            <input type="password" placeholder="Password" className="input" id="pwd"></input>
                            <input type="number" placeholder="Phone Number" className="input" id="phone_num"></input>
                            <input type="text" placeholder="Email" className="input" id="email"></input>
                            <input className="btn" type="submit" value="Sign In" id="register" onClick={registerHandler}></input>
                        </form>
                        <p id='username_error'>{username_error}</p>
                        <p id='pwd_error'>{pwd_error}</p>
                        <p id='phone_error'>{phone_error}</p>
                        <p id='email_error'>{email_error}</p>
            </div>
            </div>
    }else{
        return <Navigate to='/login'></Navigate>
    }



}