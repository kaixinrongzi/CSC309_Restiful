import {BrowserRouter, NavLink, Routes, Route} from 'react-router-dom'
import {useDispatch, useSelector} from 'react-redux'
import {getToken} from './store/tokenGetter'
import Profile from './profile'


export default function MyAccount(){

    const token = useSelector(state=>state.token.token)
    console.log('myaccount 11: ', token)



}

