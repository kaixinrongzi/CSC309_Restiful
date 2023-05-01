import {useState, useEffect} from 'react';
import axios from 'axios';

const Reservation = (props) => {
    const [hotel, setHotel] = useState([])
    const [startDate, setStartDate] = useState("")
    const [endDate, setEndDate] = useState("")
    const [totalPrice, setTotalPrice] = useState(0)
    const [guests, setGuests] = useState(0)
    const {hotel_id, price} = props
    useEffect(() => {
        if (startDate && endDate && price) {
            const start = new Date(startDate)
            const end = new Date(endDate)
            const diffInMs = Math.abs(end - start);
            const diffInDays = Math.ceil(diffInMs / (1000 * 60 * 60 * 24));
            setTotalPrice(diffInDays * price)
        }
    }, [startDate, endDate, price])

    // useEffect(() => {
    //     fetch() // fetch the information of reservation
    //     .then(response => response.json)
    //     .then(json => setHotel(json.data))
    //     .catch(error => console.log(error))
    // }, [hotel])

    const token = localStorage.getItem('token');

    const submit = {
        hotel: hotel_id,
        start_date: startDate,
        end_date: endDate, 
        guests: guests
    }
    const config = {
        headers: { 'Content-Type': 'application/json',
                    'Authorization': "Bearer " + token},
    };
    console.log(submit)
    console.log("56", startDate)

    function handleSubmit() {
        axios.post("http://localhost:8000/hotels/reservation/reserve/", JSON.stringify(submit),
          config)
          .then(response => {
            console.log("57", "post successfully")
            console.log(response);
          })
          .catch(error => {
            console.log('61', "what happening")
            console.log(error);
          });
      }

    return <>
    <main>
    <h1>Reservation</h1>
    <label for='guestNumber'>Number of Guest</label>
    <select name='guestNumber'
            onChange={(event) => setGuests(event.target.value)}>
        <option value="1">1</option>
        <option value="2">2</option>
        <option value="3">3</option>
        <option value="4">4 or more</option>
    </select>

    <label for="startDate">Choose start date</label>
    <input type="date" 
            name="startDate" 
            value={startDate} 
            onChange={(event) => setStartDate(event.target.value)}
            />

    <label for="endDate">Choose end date</label>
    <input type="date"
            name='endDate'
            value={endDate}
            onChange={(event) => setEndDate(event.target.value)}
            />

    <p>The reservation starts on {startDate} and ends on {endDate}.</p>
    <p>The total price is {totalPrice}.</p>
    {/* transfer the data to backend */}
    <button type="button"
            onClick={handleSubmit}>Submit
    </button>
   
    </main>
    </>
}
export default Reservation
