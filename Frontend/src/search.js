import {BrowserRouter, NavLink, Routes, Route, useNavigate} from 'react-router-dom'
import {useDispatch, useSelector} from 'react-redux'
import {getToken} from './store/tokenGetter'
import {getCommentTarget, getObjectId} from './store/commentTarget.js'
import React, {useState, useEffect} from 'react'
import axios from 'axios'
import LogIn from './login'
import './css/userAccount.css'
import $ from 'jquery'


export default function Search(){

    const [searchResults, setSearchResults] = useState([])
    //TODO: to change
    const [searchParams, setSearchParams] = useState(null)
    const [searchCounts, setSearchCounts] = useState(0)
    const [currentPage, setCurrentPage] = useState(1)


    const navigate = useNavigate()


//    const token = useSelector(state=>state.token.token)
    const token = localStorage.getItem('token')
    const dispatch = useDispatch()

    useEffect(()=>{

        var search_params = new Map(Object.entries(setSearchParams));
        console.log(search_params)
        search_params.set('page', currentPage)
        console.log(search_params)

        axios
         .get('http://localhost:8000/hotels/search/availability/',
            {
                headers: {"Authorization": 'Bearer '+ token},
                params: Object.fromEntries(search_params)
            }
            )
            .then(response=>{
                console.log('get avails: ', response.data.results)
                setSearchResults(response.data.results)

         }).catch(e=>{
            console.log(e)
            if(e.response.status===401){
                alert('unauthorized token')
                navigate('/accounts/login')
            }
         })
    },[currentPage])

    const previousPageHandler=()=>{
        if(currentPage > 1){
            setCurrentPage(currentPage - 1)
        }
    }

    const nextPageHandler=()=>{
        if(currentPage < Math.ceil(searchCounts / 5)){
            setCurrentPage(currentPage + 1)
        }
    }

    const search=(e)=>{
        e.preventDefault();

        const myForm = e.target.closest('form')

        var search_params = new Map()
        search_params.set('hotel_id', $(myForm).find("#search_by_hotel_id").val())
        search_params.set('start_date', $(myForm).find("#search_by_end_date").val())
        search_params.set('end_date', $(myForm).find("#search_by_end_date").val())
        search_params.set('price', $(myForm).find("#search_by_price").val())

        setSearchParams(Object.fromEntries(search_params))

        axios
         .get('http://localhost:8000/hotels/search/availability/',
            {
                headers: {"Authorization": 'Bearer '+ token},
                params: Object.fromEntries(search_params)
            }
            )
            .then(response=>{
                console.log('search: ', response)
                setSearchCounts(response.data.count)
                setSearchResults(response.data.results)
         }).catch(e=>{
            console.log(e)
            if(e.response.status===401){
                alert('unauthorized token')
                navigate('/accounts/login')
            }
         })
    }

    const bookHandler=(e)=>{

    }

    return <main className="searchResults">
          <form onSubmit={search}>
            <label for='search_by_hotel_id'>Search By Hotel ID:</label>
            <input id='search_by_hotel_id'></input><br/>
            <label for='search_by_start_date'>Search By Start Date:</label>
            <input id='search_by_start_date' type='date'></input>
            <label for='search_by_end_date'>Search By End Date:</label>
            <input id='search_by_end_date' type='date'></input><br/>
            <label for='search_by_price'>Search By Price:</label>
            <input id='search_by_price'></input>
            <input type='submit'/>
          </form>

            <ul>
                {
                  searchResults.map((value, index)=>{
                    return <li key={index}>
                        hotel_id: {value.hotel}, start-date: {value.start_date}, end-date: {value.end_date}, price: {value.price}, capacity: {value.capacity}, beds: {value.beds}, baths: {value.baths}
                       <button onClick={bookHandler}>Book</button>
                       </li>

                  })
                }
            </ul>
            <ul className='pagesHandler'>
                <li><button onClick={previousPageHandler}>Previous Page</button></li>
                <li>Current Page: { currentPage }</li>
                <li><button onClick={nextPageHandler}>Next Page</button></li>
            </ul>

      </main>
}

