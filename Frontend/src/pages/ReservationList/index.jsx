import { useState, useEffect } from 'react';
import Table from '../ReservationTable'
import axios from 'axios';
import {useDispatch, useSelector} from 'react-redux'

const Reservations = () => {
    const [reservations, setReservations] = useState([])
    const [query, setQuery] = useState({user_type: "", state: "", page: 1})
    const [totalPages, setTotalPages] = useState(1)

    const token = useSelector(state=>state.token.token)
    useEffect(() => {
        const {user_type, state, page} = query;
        // fetch from reservation list
        axios.get(`http://localhost:8000/hotels/reservation/list/?user_type=${user_type}&state=${state}&page=${page}`, 
                {headers: {'Authorization': 'Bearer' + token}}
        )
        .then(response => response.json)
        .then(json => {
            setReservations(json.results);
            setTotalPages(Math.max(Math.ceil(json.count / 2), 1));
        }, [query])
    })

    return <>
    <p>
        <label>Choose User Type:
            <select 
                id="user_type" 
                value={query.user_type}
                onChange={event => setQuery({...query, user_type: event.target.value, page:1})}>
                <option key="guest" value="guest">Guest</option>
                <option key="host" value='host'>Host</option>
            </select>
        </label>
    </p>
    <p>
        <label>Choose state:
        <select id="state" 
                value={query.state}
                onChange={event => setQuery({...query, state: event.target.value, page: 1})}>
            <option key="P" value="P">Pending</option>
            <option key="A" value="A">Approved</option>
            <option key="Ca" value="Ca">Cancelled</option>
            <option key="D" value="D">Denied</option>
            <option key="E" value="E">Expired</option>
            <option key="P" value="T">Terminated</option>
            <option key="P" value="F">Finished</option>
        </select>
    </label>
    </p>
    <Table reservations={reservations}/>
    <p>
        {query.page > 1
            ? <button onClick={() => setQuery({...query, page: query.page - 1})}>Previous</button>
            : <></>
        }
        {query.page < totalPages
            ? <button onClick={() => setQuery({...query, page: query.page + 1})}>Next</button>
            : <></>
        }
    </p>
    <p>Page {query.page} out of {totalPages}</p>
    
    </>
}
export default Reservations