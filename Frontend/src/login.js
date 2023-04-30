import './css/style1.css'
import './css/style2.css'
import './css/index.css'
import './css/bulma/bulma.css'
import './css/bulma/bulma.css.map'
import './css/bulma/bulma.min.css'
import './css/bulma/bulma-rtl.css'
import './css/bulma/bulma-rtl.css.map'
import './css/bulma/bulma-rtl.min.css'
import $ from 'jquery';
import axios from 'axios'
import {useNavigate} from 'react-router-dom'
import React, {useState, useEffect} from 'react'


function LogIn(){

    const [isLogin, setIsLogin] = useState(false)
    const [token, setToken] = useState('')
    const navigate = useNavigate()
    console.log("loginlalala", isLogin);

    const loginHandler=(e)=>{

        e.preventDefault()

        console.log("handle login")

        var myForm = $(e.target.closest('form'))

        axios
            .post('http://localhost:8000/accounts/token/api/',
            {
                // Data to be sent to the server
                username: myForm.find('#username').val(),
                password: myForm.find('#password').val(),
            }

//            ,{
//                headers: {"Authorization": 'Bearer '+"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjgyMDQ2MTc5LCJpYXQiOjE2ODIwNDU4NzksImp0aSI6IjI3NmZiMGZmNDA2ZTQzODA5ZDg2NzQxMzQyNzg1OWNlIiwidXNlcl9pZCI6MTd9._jgPlwjsSqEeN_9zco1S_MxQvPlSwxbzPR7x2FUzWWU"}
//             }
             )
            .then(response => {
                console.log(response.data);

                if(!response.data.error){
                    $('#username_error').html('')
                    $('#pwd_error').html('')

                    setToken(response.data.access)
                    localStorage.setItem('token', response.data.access)

                    alert("You Have Gotten Your token!")

                    axios
                        .post('http://localhost:8000/accounts/login/',
                        {
                            // Data to be sent to the server
                            username: myForm.find('#username').val(),
                            password: myForm.find('#password').val(),
                        },
                        {headers: {'Authorization': 'Bearer '+response.data.access}}
                        ).then(response=>{
                            localStorage.setItem('user_id', response.data.id)
                        }).catch(error=>console.log(error))

                    setIsLogin(true);

//                    return <Navigate to='/profile'></Navigate>
                }else{
                    $('#login_error').html(response.data.error)
                }

            })
            .catch(function (error) {
               console.log(error.response)
               if(error.response.status === 401){
                    //unauthorized
                    $('#login_error').html(error.response.status + ' ' + error.response.statusText)
               }

            })
    }

    if(!isLogin){
        return <div className='login_overall'>
            <div className="login">
			    <form action="../users/UserAccount.html" className="form" id="form1">
					<h2 className="form__title">Log In</h2>
					<input type="text" placeholder="User" className="input" id='username'/>
					<input type="password" placeholder="Password" className="input" id='password'/>
					<input className="btn" type="submit" value="Sign In" onClick={loginHandler}></input>
				</form>
				<p id='login_error'></p>
			</div>
            <div className="registerOverlay">
                <a href="/accounts/register"><button className="btn" id="signIn">Register</button></a>
           </div>

           </div>
    }else{
        navigate('/accounts/profile', { state: {token: token}, replace: false })
    }

}


function LogOut(){

    const [logoutInfo, setLogoutInfo] = useState('')
    const token = localStorage.getItem('token')

    const navigate = useNavigate()
    useEffect(()=>{
        axios.
            get('http://localhost:8000/accounts/logout/',
                {headers: {'Authorization': 'Bearer '+token}}
            ).then(response=>{
                console.log(response.data)
                localStorage.setItem('token', '')
                setLogoutInfo(response.data.username + ' : ' + response.data.result)
            })
            .catch(err=>{
                console.log(err)

            })
    }, [navigate])

    return <main>
        <div className='logout'>
            <p className='logoutInfo'>{ logoutInfo }</p>
        </div>
    </main>

}

export {LogIn, LogOut}
