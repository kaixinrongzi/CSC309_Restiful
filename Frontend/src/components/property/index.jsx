import { useState, useEffect } from 'react'
import axios from 'axios'
import './style.css'

function Property(props) {
    const [hotel, setHotel] = useState("");
    const hotel_id = props.hotel_id

    useEffect(() => {
        axios.get(`http://localhost:8000/hotels/${hotel_id}/view/`)
        .then(response => {
            setHotel(response.data);
            console.log(response.data);
        })
        .catch(error => {
            console.log(error);
        });
    }, [])
    
    
    return <>
    <main>
    <table>
        <thead>
            <th>Property_name</th>
            <th>Description</th>
            <th>Owner</th>
            <th>Rating</th>
            <th>Capacity</th>
            <th>Beds</th>
            <th>Baths</th>
            <th>is_active</th>
        </thead>
        <tbody>
            <td>{hotel.name}</td>
            <td>{hotel.description}</td>
            <td>{hotel.owner}</td>
            <td>{hotel.rating}</td>
            <td>{hotel.capacity}</td>
            <td>{hotel.beds}</td>
            <td>{hotel.baths}</td>
            <td>{hotel.is_active}</td>
        </tbody>
    </table>
    </main>
    </>
}
export default Property
