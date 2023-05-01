import React, { useState, useEffect } from "react";
import axios from "axios";
import "./css/HotelAvailability.css";
import { useLocation, useNavigate } from "react-router-dom";
import $ from 'jquery'

export default function Hotel_Availability() {
  const [availability, setAvailability] = useState([]);
  const [create_res, setCreateRes] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [avaiCounts, setAvailCounts] = useState(0);
  const token = localStorage.getItem("token");
  const navigate = useNavigate()
  const location = useLocation();
  const hotel_id = location.state?location.state.hotel_id:-1;

  console.log("Hotel ID:", hotel_id);
  useEffect(() => {
    axios
      .get("http://localhost:8000/hotels/search/availability/", {
        headers: { Authorization: "Bearer " + token }, 
        params: {hotel_id: hotel_id},
      })
      .then((response) => {
        console.log("API Response:", response.data);
        setAvailability(response.data.results);
        setAvailCounts(response.data.count)
      })
      .catch((error) => {
        console.log(error);
      });
  }, [navigate]);

  useEffect(() => {
    axios
      .get("http://localhost:8000/hotels/search/availability/", {
        headers: { Authorization: "Bearer " + token },
        params: {hotel_id: hotel_id, page: currentPage},
      })
      .then((response) => {
        console.log("API Response:", response.data);
        setAvailability(response.data.results);
        setAvailCounts(response.data.count)
      })
      .catch((error) => {
        console.log(error);
      });
  }, [currentPage]);
  
  const handleUpdateAvailability = (event) => {
    event.preventDefault();
    const form = event.target.closest("form");
    const start_date = form.querySelector(".start_date_input").value;
    const end_date = form.querySelector(".end_date_input").value;
    const price = form.querySelector(".price-input").value;

    axios
      .put(
        //update/<int:pk>/availability/
        `http://localhost:8000/hotels/update/${hotel_id}/availability/`,
        {
          start_date,
          end_date,
          price,
        },
        {
          headers: { Authorization: "Bearer " + token },
        }
      )
      .then((response) => {
        console.log(response);
        const updatedAvailability = availability.map((value, index) => {
          if (value.id === hotel_id) {
            return { ...value, start_date, end_date, price };
          }
          return value;
        });

        setAvailability(updatedAvailability);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const handleReturn = () => {
    return <ul>
      {availability.map((value, index) => (
        <li key={index}>
          <form onSubmit={(event) => {handleUpdateAvailability(event, value.id)}}>
            <label>
              Start Date:
              <input
                type="date"
                className="start_date_input"
                defaultValue={value.start_date}
              />
            </label>
            <label>
              End Date:
              <input
                type="date"
                className="end_date_input"
                defaultValue={value.end_date}
              />
            </label>
            <label>
              Price:
              <input
                type="number"
                className="price-input"
                defaultValue={value.price}
              />
            </label>
            <button type="submit">Update</button>
          </form>
        </li>
      ))}
    </ul>
  }

  const addAvailability=(e)=>{
    const new_hotel = e.target.closest('.add-hotel-avail')
    axios.
    post('http://localhost:8000/hotels/add/'+hotel_id+'/availability/',
        {start_date: $(new_hotel).find('#startDate').val(),
        end_date: $(new_hotel).find('#endDate').val(),
        price: $(new_hotel).find('#price').val()},
        {headers: { Authorization: "Bearer " + token }}
    ).then(response=>{
        console.log(response)
        setCreateRes(response.status + " " + response.statusText)
    }).catch(err=>{
        console.log(err.response)
    })
  }

  const previousPageHandler=()=>{
    if(currentPage > 1){
        setCurrentPage(currentPage - 1)
    }
  }

  const nextPageHandler=()=>{
    if(currentPage < Math.ceil(avaiCounts / 5)){
        setCurrentPage(currentPage + 1)
    }
  }

  return (
    <div className="hotel-availability">
      <h2>Hotel Availability: </h2>
        { handleReturn() }
        <br/>
        <div className='add-hotel-avail'>
            <h2>Add New Availability: </h2>
            <label for='startDate'>Start Date</label>
            <input id='startDate' type='date'/>
            <label for='endDate'>End Date</label>
            <input id='endDate' type='date'/>
            <label for='price'>Price</label>
            <input id='price'/>
            <button onClick={addAvailability}>Add Availability</button>
            <p>{create_res}</p>
            <ul>
                <li><button onClick={previousPageHandler}>Previous Page: </button></li>
                <li>Current Page: {currentPage}</li>
                <li><button onClick={nextPageHandler}>Next Page: </button></li>
            </ul>
        </div>
    </div>
  );
}
