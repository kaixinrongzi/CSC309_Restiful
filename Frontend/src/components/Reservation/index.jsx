import {useState, useEffect} from 'react';

const Reservation = (hotel_id, price) => {
    const [hotel, setHotel] = useState([])
    const [startDate, setStartDate] = useState("")
    const [endDate, setEndDate] = useState("")
    const [totalPrice, setTotalPrice] = useState(0)
    const [guests, setGuests] = useState(0)

    useEffect(() => {
        if (startDate && endDate && price) {
            const start = new Date(startDate)
            const end = new Date(endDate)
            const diffInMs = Math.abs(end - start);
            const diffInDays = Math.ceil(diffInMs / (1000 * 60 * 60 * 24));
            setTotalPrice(diffInDays * price)
        }
    }, [startDate, endDate, price])

    useEffect(() => {
        fetch() // fetch the information of reservation
        .then(response => response.json)
        .then(json => setHotel(json.data))
        .catch(error => console.log(error))
    }, [hotel])

    const token = localStorage.getItem('token');

    const submit = {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'Authorization': "Bearer" + token
        },
        body: JSON.stringify({
            hotel: hotel_id,
            start_date: {startDate},
            end_date: {endDate},
            state: 'P',
            price: {price},
            guests: {guests},
            guest: localStorage.getItem('user_id'),
        })
    };

    return <>
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
            onClick={() => fetch("", submit)
                            .then(response => response.json)
                            .then(json => json.data)}>
    </button>
    </>
}
export default Reservation
